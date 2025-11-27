from django.views.generic import TemplateView, ListView, DetailView
from django.shortcuts import render

from interview.models import Vacancy


# Create your views here.

class MainPageView(TemplateView):
    template_name = "pages/main.html"


class AboutPageView(TemplateView):
    template_name = "pages/about.html"


class VacanciesShowPageView(ListView):
    model = Vacancy
    template_name = "pages/vacancies.html"
    context_object_name = "vacancies"

