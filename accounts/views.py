from django.views.generic import CreateView
from django.urls import reverse_lazy
from .forms import CustomUserCreationForm, PasswordForm
from django.core.mail import send_mail
from django.shortcuts import render

class SignUpView(CreateView):
    template_name = "registration/signup.html"
    form_class = CustomUserCreationForm
    success_url = reverse_lazy("login")