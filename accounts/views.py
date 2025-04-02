from django.views.generic import CreateView
from django.urls import reverse_lazy
from .forms import CustomUserCreationForm, PasswordForm
from django.core.mail import send_mail
from django.shortcuts import render

class SignUpView(CreateView):
    template_name = "registration/signup.html"
    form_class = CustomUserCreationForm
    success_url = reverse_lazy("login")

def reset_password_email(request):
    if request.method=="POST":
        form=PasswordForm(request.POST)
        if form.is_valid():
            print("Valid form")

            email=form.cleaned_data['email']

            send_mail(
                "Password Reset",
                email,
                [],
                html_message= f"""
                <h1>Password Reset Request</h1>
                <p>You requested a password reset. Click the link below to reset your password:</p>
                <a href="http://127.0.0.1:8000/reset-password-confirm/">Reset Password</a>
                <p>If you did not request this email, please ignore it.</p>
                """
            )

            return render(request, "registration/password_reset_form.html", {'form': PasswordForm(), "sent": 1})
        else:
            print("Invalid Form")
    else:
        form=PasswordForm()
    return render(request, "registration/password_reset_done.html", {'form': form, "sent": 0})