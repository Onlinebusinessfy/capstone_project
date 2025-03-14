from django.shortcuts import render
from .forms import ContactForm
from django.core.mail import send_mail
from django.template.loader import render_to_string

# Create your views here.
def home(request):
    return render(request, 'pages/home.html')

def about(request):
    return render(request, 'pages/about.html')

def forum(request):
    return render(request, 'pages/forum.html')

def contact_view(request):
    if request.method=="POST":
        form=ContactForm(request.POST)
        if form.is_valid():
            print("Valid form")

            email=form.cleaned_data['email']
            message=form.cleaned_data['message']

            message_body=render_to_string("content/email.html", request.POST)

            send_mail(
                "Portfolio email",
                message,
                email,
                ['lloyd777999@gmail.com'],
                html_message=message_body
            )
        else:
            print("Invalid form")

    else:
        #show the page
        form=ContactForm()

    return render(request, "pages/contact.html", {'form': form})