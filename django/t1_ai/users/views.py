from django.urls import reverse_lazy
from django.views.generic.edit import FormView
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, TemplateView
from django.contrib.auth import login as auth_login, get_user_model
from .forms import UserRegisterForm, UserLoginForm


User = get_user_model()


# Create your views here.
class UserLoginView(LoginView):
    success_url = reverse_lazy("pages:vacancies")
    template_name = "users/auth.html"
    form_class = UserLoginForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["type"] = "login"   # вкладка входа активна
        context["login_form"] = context.pop("form")
        return context


class RegisterView(FormView):
    template_name = "users/auth.html"
    form_class = UserRegisterForm
    success_url = reverse_lazy("pages:vacancies")  # куда редирект после регистрации

    def form_valid(self, form):
        user = form.save()
        auth_login(self.request, user)
        messages.success(self.request, "Вы успешно зарегистрировались!")
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["type"] = "register"  # чтобы вкладка регистрации была активна
        context["register_form"] = context.pop("form")
        return context



class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = "users/profile.html"


