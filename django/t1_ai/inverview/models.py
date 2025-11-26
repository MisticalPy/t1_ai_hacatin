from django.db import models

# Create your models here.
class Vacancy(models.Model):
    DIRECTIONS = [
        ("backend", "Backend"),
        ("frontend", "Frontend"),
        ("fullstack", "Full Stack"),
        ("datascience", "Data Science"),
    ]

    EXPERIENCE_CHOICES = [
        ("no_exp", "Новичок (0 лет опыта)"),
        ("junior", "Junior (1–3 года опыта)"),
        ("middle", "Middle (3–5 лет опыта)"),
        ("senior", "Senior (5+ лет опыта)"),
        ("lead", "Team Lead / Architect (7+ лет опыта)"),
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



