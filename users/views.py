from django.shortcuts import render
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)
from .models import Profile
from .forms import ProfileForm
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect
from django.http import HttpResponseRedirect, HttpResponseForbidden

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
    context_object_name = 'profile'

class ProfileCreateView(LoginRequiredMixin, CreateView):
    template_name="content/profile_create.html"
    model=Profile
    form_class=ProfileForm
    success_url=reverse_lazy("profile_list")

    def form_valid(self, form):
        form.instance.user = self.request.user
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
        
@login_required
def delete_profile(request, pk):
    profile = get_object_or_404(Profile, pk=pk)

    if request.user == profile.user or request.user.is_superuser:
        profile.delete()
        return redirect('profile_list')

    return HttpResponseForbidden("You can't delete this profile.")