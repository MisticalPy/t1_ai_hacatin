from django.views.generic import TemplateView
from django.shortcuts import render

# Create your views here.


class ResumePageView(TemplateView):
    template_name = "inverview/resume.html"

