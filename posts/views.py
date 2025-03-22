from django.shortcuts import render, get_object_or_404
from django.views.generic import(
    ListView,
    DetailView,
    CreateView,
    UpdateView,
)
from .models import Post, Status
from django.urls import reverse_lazy, reverse
from .forms import PostForm
from django.contrib.auth.decorators import login_required #function view
from django.contrib.auth.mixins import LoginRequiredMixin #class views
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseRedirect
from django.db.models import Count

# Create your views here.
class PostListView(ListView):
    template_name="posts/list.html"
    model=Post
    
    def get_filtered_data(self, search):
        posts = Post.objects.annotate(number_of_likes=Count("likes")).order_by("created_on").reverse()
        if search:
            # apply the filter
            results = posts.filter(title__contains=search)
            return results
        else:
            # no filter, return all
            return posts
        
    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        search_text = self.request.GET.get('search')
        all_posts= self.get_filtered_data(search_text)
        context["post_list"]=all_posts
        return context
    

def BlogPostLike(request, pk):
    post = get_object_or_404(Post, id=request.POST.get('blogpost_id'))
    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
    else:
        post.likes.add(request.user)

    return HttpResponseRedirect(reverse('post_detail', args=[str(pk)]))

class PostDetailView(DetailView):
    template_name="posts/detail.html"
    model=Post

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)

        likes_connected = get_object_or_404(Post, id=self.kwargs['pk'])
        liked = False
        if likes_connected.likes.filter(id=self.request.user.id).exists():
            liked = True
        data['number_of_likes'] = likes_connected.number_of_likes()
        data['post_is_liked'] = liked
        return data

class PostCreateView(LoginRequiredMixin, CreateView):
    template_name="posts/create.html"
    model=Post
    form_class=PostForm
    success_url=reverse_lazy("post_list")

    def form_valid(self, form):
        # the record is saved here
        form.instance.author=self.request.user #set the logged user
        return super().form_valid(form) #continue with the save process

class PostUpdateView(LoginRequiredMixin, UpdateView):
    template_name="posts/update.html"
    model=Post
    form_class=PostForm
    success_url=reverse_lazy("post_list")

    def get_object(self, queryset = None):
        post = super().get_object(queryset)

        if post.author != self.request.user:
            raise PermissionDenied("You don't have permission to modify this record!")
        else:
            return post