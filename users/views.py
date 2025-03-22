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

    def get_queryset(self):
        search=self.request.GET.get('search')
        if search:
            # apply the filter
            results=Profile.objects.filter(name__contains=search)
            return results
        else:
            # no filter, return all
            return Profile.objects.all()

    def get_filtered_data(self, search):
        if search:
            print("Apllying filter")
            # apply the filter
            results=Profile.objects.filter(name__contains=search).order_by("created_at").reverse
            return results
        else:
            # no filter, return all
            return Profile.objects.all().order_by("created_at").reverse()

    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        search_text=self.request.GET.get('search')
        all_posts=self.get_filtered_data(search_text)
        context["profile_list"]=all_posts
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

        if profile.user != self.request.user:
            raise PermissionDenied("You are no the owner of this profile!")
        else:
            return profile