from django.contrib import admin
from .models import Post, Postcomments

# Register your models here.
admin.site.register(Post)
admin.site.register(Postcomments)
