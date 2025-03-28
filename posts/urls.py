from django.urls import path
from .views import(
    PostListView,
    PostDetailView,
    PostCreateView,
    PostUpdateView,
    BlogPostLike,
)

urlpatterns = [
    path('', PostListView.as_view(), name="post_list"),
    path('<int:pk>/', PostDetailView.as_view(), name="post_detail"),
    path('create/', PostCreateView.as_view(), name="post_create"),
    path('update/<int:pk>/', PostUpdateView.as_view(), name="post_update"),
    path('blogpost-like/<int:pk>/', BlogPostLike, name="blogpost_like"),
]