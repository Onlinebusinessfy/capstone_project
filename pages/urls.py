from django.urls import path
from .views import home, about, forum, contact_view

urlpatterns = [
    path("", home, name="root"),
    path("home/", home, name="home"),
    path("about/", about, name="about"),
    path("forum/", forum, name="forum"),
    path("contact/", contact_view, name="contact"),
]