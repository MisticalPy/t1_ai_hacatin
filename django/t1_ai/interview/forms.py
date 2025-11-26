from django import forms

from .models import UserResume

class ResumePostForm(forms.ModelForm):
    class Meta:
        model = UserResume

        fields = ("about", )
        widgets = {
            "about": forms.Textarea(attrs={"class": "resume_textarea",
                                           "placeholder": "Напишите о себе...",
                                           "aria-label": "Напишите о себе"})
        }