from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden, JsonResponse

from .models import Vacancy, Interview, UserResume
from .forms import ResumePostForm

# БИЗНЕС-ЛОГИКА
from services.prompt_generator import PromptGenerator
from services.speech import SpeechRecognizer

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
    interview = get_object_or_404(Interview, id=interview_id)

    if not interview.is_owner(request.user):
        return HttpResponseForbidden()

    if interview.status != interview.Status.ACTIVE_QUESTION:
        return redirect("interview:router", interview_id=interview.id)

    if request.method == "POST":
        file_obj = request.FILES.get("file")
        user_answer = SpeechRecognizer.recognize(file_obj.read())
        print(user_answer)

        json_object = {
            "status": "ok",
            "data": {
                "message": "",
                "is_stop": False,
            }
        }
        # Кол-во вопросов всего
        total_count_questions = interview.vacancy.total_questions
        cur_question = interview.answered_questions_count

        if cur_question >= total_count_questions:
            interview.status = Interview.Status.ACTIVE_QUESTION
            interview.save()

            return JsonResponse(json_object)

        if cur_question == 0:
            json_object["data"]["message"] = "Добрый день, вы проходите онлайн собеседование будьте предельно честны."
            return JsonResponse(json_object)

    return render(request, "interview/question.html")
