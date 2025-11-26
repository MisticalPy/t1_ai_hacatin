from django.urls import path

from django.contrib.auth.views import LogoutView
from . import views

app_name = "pages"

urlpatterns = [
    path("", views.MainPageView.as_view(), name="index"),
    path("about/" , views.AboutPageView.as_view(), name="about"),
    path("vacancies/", views.VacanciesShowPageView.as_view(), name="vacancies"),
]


