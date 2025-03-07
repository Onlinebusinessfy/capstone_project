from django.urls import path
from .views import home, about, forum

urlpatterns = [
    path("", home, name="root"),
    path("home/", home, name="home"),
    path("about/", about, name="about"),
    path("forum/", forum, name="forum"),
]