import json
import uuid

from django.core.files.base import ContentFile
from django.core.files.storage import FileSystemStorage
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden, JsonResponse

from django.db.models import Case, When, Value, IntegerField
from .models import Vacancy, Interview, UserResume, InterviewQA, TaskSolution, Task
from .forms import ResumePostForm

# БИЗНЕС-ЛОГИКА
from services.prompt_generator import PromptGenerator
from services.speech import SpeechRecognizer
from services.ai_client import AIClient
from services.code_container import DockerContainer

# Create your views here.
@login_required
def start_interview(request, vacancy_id):
    vacancy = get_object_or_404(Vacancy, id=vacancy_id)

    interview = Interview.objects.create(
        candidate=request.user,
        vacancy=vacancy,
        status=Interview.Status.ACTIVE_RESUME,
    )

    return redirect("interview:resume", interview_id=interview.id)


@login_required
def interview_router(request, interview_id):
    interview = get_object_or_404(Interview, id=interview_id)

    if not interview.is_owner(request.user):
        return HttpResponseForbidden("Это не твой собес, братишка")

    match interview.status:
        case Interview.Status.ACTIVE_RESUME:
            return redirect("interview:resume", interview_id=interview.id)
        case Interview.Status.ACTIVE_QUESTION:
            return redirect("interview:questions", interview_id=interview.id)
        case Interview.Status.ACTIVE_TASKS:
            return redirect("interview:tasks", interview_id=interview.id)
        case Interview.Status.ACTIVE_TASKS_FEEDBACK:
            return redirect("interview:tasks_feedback", interview_id=interview.id)
        case Interview.Status.FINISHED:
            return redirect("interview:summary", interview_id=interview.id)


@login_required
def interview_resume(request, interview_id):
    interview = get_object_or_404(Interview, id=interview_id)

    if not interview.is_owner(request.user):
        return HttpResponseForbidden()

    if interview.status != interview.Status.ACTIVE_RESUME:
        return redirect("interview:router", interview_id=interview.id)

    if request.method == "POST":

        UserResume.objects.create(
            session=interview,
            about=request.POST.get("about")
        )

        interview.status = Interview.Status.ACTIVE_QUESTION
        interview.save()
        return redirect("interview:router", interview_id=interview.id)

    context = {
        "interview": interview,
        "vacancy": interview.vacancy,
        "form": ResumePostForm()
    }

    return render(request, "interview/resume.html", context)


@login_required
def interview_questions(request, interview_id):
    """Начинается самая душная часть всего проекта,
    логика ответов...
    но так как я круто расписал модели логику написать
    не составит большого труда...
    """
    interview = get_object_or_404(Interview, id=interview_id)

    if not interview.is_owner(request.user):
        return HttpResponseForbidden()

    if interview.status != interview.Status.ACTIVE_QUESTION:
        return redirect("interview:router", interview_id=interview.id)

    if request.method == "GET":
        return render(request, "interview/question.html")

    # Сборщик JSON ответа
    def make_response(message: str, is_stop: bool = False):
        return JsonResponse({
            "status": "ok",
            "data": {
                "message": message,
                "is_stop": is_stop,
            }
        })

    total_questions = interview.vacancy.total_questions

    # 1. Текущий открытый вопрос без ответа пользователя
    active_qa = interview.qas.filter(user_answer__isnull=True).last()
    asked_count = interview.qas.count()

    if asked_count == 0 and not active_qa:
        first_question = "Добрый день, я ваш ИИ-HR, расскажите о своём последнем проекте."

        active_qa = InterviewQA.objects.create(
            session=interview,
            question=first_question
        )

        return make_response(active_qa.question)

    # 2. Если пользователь не прислал голосовое сообщение
    file_obj = request.FILES["file"]
    if not file_obj:
        if active_qa:
            return make_response(active_qa.question)


    # 3. Распознавание ответа пользователя
    user_answer = SpeechRecognizer.recognize(file_obj.read())

    if not user_answer:
        return make_response("Извините, я не понял, что вы говорите. Попробуйте еще раз.")

    # 4. Запись ответа в активный вопрос
    if active_qa:
        active_qa.user_answer = user_answer
        active_qa.save()

    answered_count = interview.qas.filter(user_answer__isnull=False).count()

    # 5. Проверяем, не закончились ли вопросы
    if answered_count >= total_questions:
        interview.status = Interview.Status.ACTIVE_TASKS
        interview.save()

        return make_response(
            "Спасибо, вы закончили текущий этап собеседования, Переходим к следующему.",
            is_stop=True
        )

    # 6. Генерируем следующий вопрос от ИИ
    ai_question = AIClient.generate_question(
        PromptGenerator.generate_question(interview=interview),
    )

    InterviewQA.objects.create(
        session=interview,
        question=ai_question,
    )

    return make_response(ai_question)


@login_required
def interview_tasks(request, interview_id):
    interview = get_object_or_404(Interview, id=interview_id)

    if not interview.is_owner(request.user):
        return HttpResponseForbidden()

    if interview.status != Interview.Status.ACTIVE_TASKS:
        return redirect("interview:router", interview_id=interview.id)

    used_tasks = TaskSolution.objects.filter(interview=interview).values_list("task_id", flat=True)
    active_tasks = Task.objects.exclude(id__in=used_tasks)

    if not active_tasks:
        interview.finish(reason="Все задачи решены")
        return redirect("interview:router", interview_id=interview.id)

    # сортировка
    sorted_tasks = active_tasks.annotate(
        sort_order=Case(
            When(difficulty="1-ый уровень", then=Value(0)),
            When(difficulty="2-ой уровень", then=Value(1)),
            When(difficulty="3-ий уровень", then=Value(2)),
            output_field=IntegerField()
        )
    ).order_by("sort_order")

    cur_task = sorted_tasks[0]

    # -------------------- GET --------------------
    if request.method != "POST":
        return render(request, "interview/tasks.html", {
            "task": cur_task,
            "testcases": cur_task.test_cases.all()
        })

    # -------------------- POST: RUN TASK --------------------
    try:
        code = json.loads(request.body.decode("utf-8"))["code"]
    except json.JSONDecodeError:
        return JsonResponse({"status": "error", "message": "invalid json"}, status=400)

    # сохраняем код
    file_id = str(uuid.uuid4())[:8]
    fs = FileSystemStorage(location="media/code_submits")
    saved_path = fs.save(f"{file_id}.py", ContentFile(code))

    # СОЗДАЁМ TaskSolution
    solution = TaskSolution.objects.create(
        interview=interview,
        task=cur_task,
        answer=code,
        status=TaskSolution.Status.RUNNING,
    )

    passed = 0
    failed = 0

    # ------------------ ГОНЯЕМ ВСЕ TEST CASES ------------------
    for test in cur_task.test_cases.all():

        runner = DockerContainer(
            code_path=fs.path(saved_path),
            timeout=cur_task.time_limit,
            input_data=test.input_data
        )
        ok, status_code, logs = runner.run()
        print(ok, status_code, logs)

        # Результат ДАЛ ОТВЕТ
        if ok:
            # Убираем \n и пробелы
            expected = test.output_data.strip()
            got = logs.strip()

            if expected == got:
                passed += 1
            else:
                failed += 1
        else:
            failed += 1

    # ---- ОБНОВЛЯЕМ SOLUTION ----
    solution.passed_tests = passed
    solution.failed_tests = failed
    solution.status = (
        TaskSolution.Status.DONE if failed == 0 else TaskSolution.Status.ERROR
    )

    # начисляем баллы (можешь формулу любую вставить)
    solution.score = passed / (passed + failed) * cur_task.max_balls
    solution.save()

    # ---- ОТДАДИМ JSON ----
    return JsonResponse({
        "status": "ok",
        "passed": passed,
        "failed": failed,
        "score": solution.score,
    })


@login_required
def interview_summary(request, interview_id):
    interview = get_object_or_404(Interview, id=interview_id)

    if not interview.is_owner(request.user):
        return HttpResponseForbidden()

    if interview.status != Interview.Status.FINISHED:
        return redirect("interview:router", interview_id=interview.id)










