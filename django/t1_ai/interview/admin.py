from django.contrib import admin
from .models import Task, TestCase, Vacancy, Interview


class TestCaseInline(admin.TabularInline):
    model = TestCase
    extra = 1


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ("title", "difficulty", "max_balls")
    inlines = [TestCaseInline]


@admin.register(Interview)
class InterviewAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "candidate",
        "vacancy",
        "colored_status",   # красиво статус показываем
        "score",
        "started_at",
        "finished_at",
    )

    list_filter = (
        "status",
        "vacancy",
        "started_at",
        "finished_at",
    )

    search_fields = (
        "id",
        "candidate__username",
        "vacancy__title",
        "stop_reason",
    )

    readonly_fields = (
        "id",
        "started_at",
        "finished_at",
    )

    # В админке можно изменить статус и причину завершения
    fieldsets = (
        ("Основная информация", {
            "fields": ("candidate", "vacancy", "status", "score")
        }),
        ("Завершение", {
            "fields": ("stop_reason", "finished_at"),
        }),
        ("Системные", {
            "fields": ("id", "started_at"),
        }),
    )

    actions = ["finish_interview"]

    def finish_interview(self, request, queryset):
        """Экшен для завершения собесов из админки."""
        updated = queryset.update(status=Interview.Status.FINISHED)
        self.message_user(request, f"Завершено {updated} собеседований.")
    finish_interview.short_description = "Завершить выбранные собеседования"

    # Красивый статус с цветами в админке
    def colored_status(self, obj):
        colors = {
            "created": "gray",
            "resume": "blue",
            "question": "orange",
            "tasks": "purple",
            "tasks_feedback": "darkorange",
            "finished": "green",
        }
        color = colors.get(obj.status, "black")
        return f'<b style="color:{color}">{obj.get_status_display()}</b>'
    colored_status.allow_tags = True
    colored_status.short_description = "Статус (цвет)"


@admin.register(Vacancy)
class VacancyAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "direction",
        "experience",
        "is_remote",
        "salary_range",
        "total_questions",
        "tasks_count",
        "created_at",
        "updated_at",
    )

    list_filter = (
        "direction",
        "experience",
        "is_remote",
        "created_at",
    )

    search_fields = (
        "title",
        "description",
        "requirements",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
    )

    filter_horizontal = ("tasks",)

    fieldsets = (
        ("Основное", {
            "fields": (
                "title",
                "direction",
                "experience",
                "is_remote",
            )
        }),
        ("Деньги", {
            "fields": (
                "salary_from",
                "salary_to",
            )
        }),
        ("Контент вакансии", {
            "fields": (
                "description",
                "requirements",
                "hard_skills",
            )
        }),
        ("Настройки собеса", {
            "fields": (
                "total_questions",
                "tasks",
            )
        }),
        ("Системное", {
            "fields": (
                "created_at",
                "updated_at",
            )
        }),
    )

    def salary_range(self, obj):
        if not obj.salary_from and not obj.salary_to:
            return "Не указана"
        return f"{obj.salary_from} – {obj.salary_to}"
    salary_range.short_description = "Вилка ЗП"

    def tasks_count(self, obj):
        return obj.tasks.count()
    tasks_count.short_description = "Кол-во задач"