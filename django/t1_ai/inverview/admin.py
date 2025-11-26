from django.contrib import admin
from .models import Vacancy

# Register your models here.

@admin.register(Vacancy)
class VacancyAdmin(admin.ModelAdmin):
    list_display = ("title", "direction", "experience", "salary_from", "created_at")
    list_display_links = ("title",)
    ordering = ("-created_at",)
    search_fields = ("title",)



