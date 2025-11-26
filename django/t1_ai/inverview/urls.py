from django.urls import path

from . import views

app_name = "inverview"

urlpatterns = [
    path("resume/<int:vacancy_id>", views.ResumePageView.as_view(), name="resume"),
]

