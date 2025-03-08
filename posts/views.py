from django.shortcuts import render
from django.views.generic import(
    ListView,
    DetailView,
    CreateView,
)
from .models import Post, Status
from django.urls import reverse_lazy
from .forms import PostForm
from django.contrib.auth.decorators import login_required #function view
from django.contrib.auth.mixins import LoginRequiredMixin #class views

# Create your views here.
class PostListView(ListView):
    template_name="posts/list.html"
    model=Post

    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        all_posts=Post.objects.all()
        context["post_list"]=all_posts.order_by("created_on").reverse()
        return context
    
class PostDetailView(DetailView):
    template_name="posts/detail.html"
    model=Post

class PostCreateView(LoginRequiredMixin, CreateView):
    template_name="posts/create.html"
    model=Post
    form_class=PostForm
    success_url=reverse_lazy("post_list")

    def form_valid(self, form):
        # the record is saved here
        form.instance.author=self.request.user #set the logged user
        return super().form_valid(form) #continue with the save process