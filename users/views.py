from django.shortcuts import render
from django.views.generic import ListView
from .models import Profile


# Create your views here.

class ProfileListView(ListView):
    template_name = "content/profile_list.html"
    model = Profile

    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        all_posts=Post.objects.all()
        context["post_list"]=all_posts.order_by("created_on").reverse()
        return context