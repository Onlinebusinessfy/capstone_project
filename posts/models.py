from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User

# Create your models here.

class Post(models.Model):
    title=models.CharField(max_length=128)
    subtitle=models.CharField(max_length=256)
    author=models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE
    )
    body=models.TextField()
    image=models.ImageField(upload_to="upload/", blank=True, null=True)
    created_on=models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User, related_name='blogpost_like')
    disLikes = models.ManyToManyField(User, related_name='blogpost_dislike')

    def __str__(self):
        return f"{self.title} - {self.author}"
    
    def number_of_likes(self):
        return self.likes.count()
    
    def number_of_dislikes(self):
        return self.disLikes.count()
    
    @property
    def number_of_comments(self):
        return Postcomments.objects.filter(blogpost_connected=self).count()

class Postcomments(models.Model):
    blogpost_connected = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    content = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.author} on {self.blogpost_connected}"