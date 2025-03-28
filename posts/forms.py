from django import forms
from .models import Post, Postcomments

class PostForm(forms.ModelForm):
    class Meta:
        model=Post
        fields=['title', 'subtitle', 'body', 'image', 'status']

class PostComment(forms.ModelForm):
    class Meta:
        model = Postcomments
        fields = ['content']