from django.urls import path

from . import views

app_name = "pages"

urlpatterns = [
    path("", views.MainPageView.as_view(), name="index"),
    path("about/" , views.AboutPageView.as_view(), name="about"),
    path("vacancies/", views.VacanciesShowPageView.as_view(), name="vacancies"),
]


