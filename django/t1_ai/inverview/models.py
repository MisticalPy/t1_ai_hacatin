from django.db import models

# Create your models here.
class Vacancy(models.Model):
    DIRECTIONS = [
        ("Backend", "Backend"),
        ("Frontend", "Frontend"),
        ("Full Stack", "Full Stack"),
        ("Data Science", "Data Science"),
    ]

    EXPERIENCE_CHOICES = [
        ("Новичок (0 лет опыта)", "Новичок (0 лет опыта)"),
        ("Junior (1–3 года опыта)", "Junior (1–3 года опыта)"),
        ("Middle (3–5 лет опыта)", "Middle (3–5 лет опыта)"),
        ("Senior (5+ лет опыта)", "Senior (5+ лет опыта)"),
        ("Team Lead / Architect (7+ лет опыта)", "Team Lead / Architect (7+ лет опыта)"),
    ]

    title = models.CharField(max_length=75, verbose_name="Заголовок")
    direction = models.CharField(verbose_name="Направление", choices=DIRECTIONS, default="Backend")
    experience = models.CharField(verbose_name="Опыт работы", blank=True, choices=EXPERIENCE_CHOICES)
    is_remote = models.BooleanField(default=True)
    salary_from = models.IntegerField(default=0)
    salary_to = models.IntegerField(default=0)
    description = models.CharField(max_length=500, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Вакансия"
        verbose_name_plural = "Вакансии"



