from django.views.generic import TemplateView
from django.shortcuts import render


# Create your views here.

class MainPageView(TemplateView):
    template_name = "pages/main.html"


class AboutPageView(TemplateView):
    template_name = "pages/about.html"


class VacanciesShowPageView(TemplateView):
    template_name = "pages/vacancies.html"

