from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import(
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)
from .models import Post, Status, Postcomments
from django.urls import reverse_lazy, reverse
from .forms import PostForm, PostComment
from django.contrib.auth.decorators import login_required #function view
from django.contrib.auth.mixins import LoginRequiredMixin #class views
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseRedirect, HttpResponseForbidden
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
        post.disLikes.remove(request.user)

    return HttpResponseRedirect(reverse('post_detail', args=[str(pk)]))

def BlogPostDisLike(request, pk):
    post = get_object_or_404(Post, id=request.POST.get('blogpost_id'))
    if post.disLikes.filter(id=request.user.id).exists():
        post.disLikes.remove(request.user)
    else:
        post.disLikes.add(request.user)
        post.likes.remove(request.user)

    return HttpResponseRedirect(reverse('post_detail', args=[str(pk)]))

@login_required
def delete_comment(request, pk):
    comment = get_object_or_404(Postcomments, pk=pk)

    if request.user == comment.author or request.user.is_superuser:
        comment.delete()
        return redirect(request.META.get('HTTP_REFERER', 'post_list'))

    return HttpResponseForbidden("No tienes permiso para eliminar este comentario.")

class PostDetailView(DetailView):
    template_name="posts/detail.html"
    model=Post

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        post = get_object_or_404(Post, id=self.kwargs['pk'])
        # Likes section
        liked = False
        if post.likes.filter(id=self.request.user.id).exists():
            liked = True
        data['number_of_likes'] = post.number_of_likes()
        data['post_is_liked'] = liked

        # DisLikes section
        disliked = False

        if post.disLikes.filter(id=self.request.user.id).exists():
            disliked = True
        data['number_of_dislikes'] = post.number_of_dislikes()
        data['post_is_disliked'] = disliked

        # comments section
        comments_connected = Postcomments.objects.filter(
            blogpost_connected=self.get_object()).order_by('created_on')
        data['comments'] = comments_connected
        if self.request.user.is_authenticated:
            data['comment_form'] = PostComment(instance=self.request.user)

        return data
    
    def post(self, request, *args, **kwargs):
        new_comment = Postcomments(content=request.POST.get('content'),
                author=self.request.user,
                blogpost_connected=self.get_object()
            )
        new_comment.save()
        return self.get(self, request, *args, **kwargs)

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