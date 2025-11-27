from django.urls import path
from . import views

app_name = "interview"

urlpatterns = [
    # Старт собеса по вакансии
    path("start/<int:vacancy_id>/", views.start_interview, name="start"),

    # роутер по статусу
    path("<uuid:interview_id>/", views.interview_router, name="router"),
    #
    # конкретные этапы собеседования
    path("<uuid:interview_id>/resume/", views.interview_resume, name="resume"),
    path("<uuid:interview_id>/questions/", views.interview_questions, name="questions"),
    path("<uuid:interview_id>/tasks/", views.interview_tasks, name="tasks"),
    # path("<uuid:interview_id>/tasks/feedback/", views.interview_tasks_feedback, name="tasks_feedback"),
    # path("<uuid:interview_id>/summary/", views.interview_summary, name="summary"),
]
