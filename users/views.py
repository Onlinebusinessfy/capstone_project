from django.shortcuts import render
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
)
from .models import Profile
from .forms import ProfileForm
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied


# Create your views here.

class ProfileListView(ListView):
    template_name = "content/profile_list.html"
    model = Profile

    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        all_posts=Profile.objects.all()
        context["profile_list"]=all_posts.order_by("name").reverse()
        return context
    
class ProfileDetailView(DetailView):
    template_name="content/profile_detail.html"
    model=Profile

class ProfileCreateView(LoginRequiredMixin, CreateView):
    template_name="content/profile_create.html"
    model=Profile
    form_class=ProfileForm
    success_url=reverse_lazy("profile_list")

    def form_valid(self, form):
        form.instance.author=self.request.user
        return super().form_valid(form)
    
class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    template_name="content/profile_update.html"
    model=Profile
    form_class=ProfileForm
    success_url=reverse_lazy("profile_list")

    def get_object(self, queryset = None):
        profile=super().get_object(queryset)

        if profile.author != self.request.user:
            raise PermissionDenied("You are no the owner of this profile!")
        else:
            return profile