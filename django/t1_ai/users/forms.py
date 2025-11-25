from django import forms
from django.contrib.auth import get_user_model

from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.db.models.fields import EmailField

User = get_user_model()

class UserRegisterForm(UserCreationForm):

    phone = forms.CharField(
        label="Телефон",
        widget=forms.TextInput(attrs={
            'placeholder': '8 (952) 017-69-75',
            'class': 'input-field',
            'id': 'loginPhone',
            'type': 'tel',
        })
    )
    email = forms.EmailField(
        label="Email",
        widget=forms.EmailInput(attrs={
            'class': 'input-wrapper',
            'type': 'email',
            'name': 'register-email',
            'id': 'registerEmail',
            'placeholder': 'Email',
        })
    )
    password1 = forms.CharField(
        label="Пароль",
        widget=forms.PasswordInput(attrs={
            'class': 'input-field',
            'name': 'register-password',
            'id': 'registerPassword',
            'placeholder': 'Password',
            'required': 'required'
        })
    )

    password2 = forms.CharField(
        label="Подтверждение пароля",
        widget=forms.PasswordInput(attrs={
            'class': 'input-field',
            'name': 'register-password2',
            'id': 'registerPassword2',
            'placeholder': 'Repeat password',
            'required': 'required'
        })
    )

    class Meta:
        model = User
        fields = ("email", "phone")

    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = self.cleaned_data["email"]
        user.email = self.cleaned_data["email"]
        user.phone = self.cleaned_data["phone"]

        user.set_password(self.cleaned_data["password1"])

        if commit:
            user.save()

        return user

class UserLoginForm(AuthenticationForm):
    username = forms.CharField(
        label="Email",
        widget=forms.EmailInput(attrs={
            "class": "input-field",
            "placeholder": "Email",
            "id": "loginEmail",
            "required": "required"
        })
    )

    password = forms.CharField(
        label="Пароль",
        widget=forms.PasswordInput(attrs={
            "class": "input-field",
            "placeholder": "Password",
            "id": "loginPassword",
            "required": "required"
        })
    )

    def clean(self):
        return super().clean()
