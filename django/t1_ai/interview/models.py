import uuid

from django.db import models
from django.conf import settings

# Create your models here.
class Directions(models.TextChoices):
    BACKEND = "Backend", "Backend"
    FRONTEND = "Frontend", "Frontend"
    FULLSTACK = "Full Stack", "Full Stack"
    DATA_SCIENCE = "Data Science", "Data Science"


class ExperienceLevels(models.TextChoices):
    INTERN = "Новичок (0 лет опыта)", "Новичок (0 лет опыта)"
    JUNIOR = "Junior (1–3 года опыта)", "Junior (1–3 года опыта)"
    MIDDLE = "Middle (3–5 лет опыта)", "Middle (3–5 лет опыта)"
    SENIOR = "Senior (5+ лет опыта)", "Senior (5+ лет опыта)"
    LEAD = "Team Lead / Architect (7+ лет опыта)", "Team Lead / Architect (7+ лет опыта)"


class Task(models.Model):
    """Модель для представления задачей который будут на ИИ-собесе"""
    DIFFICULTY_CHOICES = ["1-й уровень", "2-уровень", "3-уровень"]
    DIFFICULTY_CHOICES = [(i, i) for i in DIFFICULTY_CHOICES]

    title = models.CharField(max_length=100, verbose_name="Название задачи")
    description = models.TextField(verbose_name="Описание / Условие")

    difficulty = models.CharField(
        max_length=25,
        choices=DIFFICULTY_CHOICES,
        default=DIFFICULTY_CHOICES[0][0],
        verbose_name="Сложность"
    )

    max_balls = models.IntegerField(
        default=1,
        verbose_name="Максимальное количество баллов"
    )

    # Пример эталлоного решения (для проверки ИИ)
    correct_answer = models.TextField(
        blank=True,
        verbose_name="Эталонное решение"
    )

    def __str__(self):
        return self.title

class Vacancy(models.Model):
    """Модель для представления вакансий"""
    title = models.CharField(max_length=75, verbose_name="Заголовок")

    direction = models.CharField(
        max_length=50,
        verbose_name="Направление",
        choices=Directions.choices,
        default=Directions.BACKEND,
    )

    experience = models.CharField(
        max_length=50,
        verbose_name="Опыт работы",
        choices=ExperienceLevels.choices,
        default=ExperienceLevels.INTERN,
    )

    is_remote = models.BooleanField(default=True, verbose_name="Удаленная работа")
    salary_from = models.IntegerField(default=0, verbose_name="Зарплата от")
    salary_to = models.IntegerField(default=0, verbose_name="Зарплата до")

    description = models.TextField(
        blank=True,
        null=True,
        verbose_name="Описание"
    )

    requirements = models.TextField(
        blank=True,
        verbose_name="Требования",
        help_text="Текстом, как в обычной вакансии"
    )

    hard_skills = models.JSONField(
        default=list,
        blank=True,
        verbose_name="Хард-навыки",
        help_text="Список навыков, напримео ['Python, 'Django', 'PostreSQL']"
    )

    total_questions = models.IntegerField(
        default=5,
        verbose_name="Количество вопросов"
    )

    tasks = models.ManyToManyField(
        "Task",
        blank=True,
        related_name="vacancies",
        verbose_name="Задачи для собеседования",
        help_text="Выбери задачи, которые будут предлагаться на ИИ-собеседвовании"
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Создано"
    )

    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Обновлено"
    )

    class Meta:
        verbose_name = "Вакансия"
        verbose_name_plural = "Вакансии"
        ordering = ["-created_at"]

    def __str__(self):
        return self.title

class Interview(models.Model):
    class Status(models.TextChoices):
        CREATED = "created", "Создана"
        ACTIVE_RESUME = "resume", "В процессе резюме"
        ACTIVE_QUESTION = "question", "В процессе собеседования"
        ACTIVE_TASKS = "tasks", "Процесс решения задач"
        ACTIVE_TASKS_FEEDBACK = "tasks_feedback", "Процесс разбора решения задач"
        FINISHED = "finished", "Завершена"

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    candidate = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="interview_sessions",
        verbose_name="Кандидат"
    )

    vacancy = models.ForeignKey(
        "Vacancy",
        on_delete=models.CASCADE,
        related_name="interview_sessions",
        verbose_name="Вакансия"
    )

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.CREATED,
        verbose_name="Статус"
    )

    answered_questions_count = models.IntegerField(
        default=0,
        verbose_name="Количество отвеченных вопросов"
    )

    score = models.FloatField(
        null=True,
        blank=True,
        verbose_name="Итоговый балл"
    )

    stop_reason = models.CharField(
        max_length=255,
        blank=True,
        verbose_name="Причина завершения"
    )

    started_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Начато"
    )

    finished_at= models.DateTimeField(
        null=True,
        blank=True,
        verbose_name="Закончено"
    )

    class Meta:
        verbose_name = "Сессия собеседования"
        verbose_name_plural = "Сессии собеседвоаний"
        ordering = ["-started_at"]

    def is_owner(self, user):
        return user.is_authenticated and user == self.candidate

    def finish(self, reason: str | None = None):
        self.status = self.Status.FINISHED
        self.stop_reason = reason or self.stop_reason
        self.save()


class InterviewQA(models.Model):
    """
    Одна пара ВОПРОС / ОТВЕТ внутри конкретной сессии.
    """

    session = models.ForeignKey(
        "Interview",
        on_delete=models.CASCADE,
        related_name="qas",
        verbose_name="Сессия собеседования"
    )

    # Вопрос, который задал ИИ (или система)
    question = models.TextField(
        verbose_name="Вопрос"
    )

    user_answer = models.TextField(
        verbose_name="Ответ пользователя"
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Время вопроса"
    )

    class Meta:
        verbose_name = "Вопрос-ответ собеседования"
        verbose_name_plural = "Вопросы-ответы собеседований"
        ordering = ["created_at"]


class UserResume(models.Model):
    session = models.OneToOneField(
        "Interview",
        on_delete=models.CASCADE,
        related_name="resume",
        verbose_name="Сессия собеседования"
    )

    about = models.TextField(
        max_length=255,
        verbose_name="О себе"
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )