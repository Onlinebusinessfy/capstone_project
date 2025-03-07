from django.db import models
from django.contrib.auth import get_user_model

# Create your models here.
class Status(models.Model):
    name=models.CharField(max_length=128)
    description=models.CharField(max_length=256)

    def __str__(self):
        return self.name

class Post(models.Model):
    title=models.CharField(max_length=128)
    subtitle=models.CharField(max_length=256)
    author=models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE
    )
    body=models.TextField()
    image=models.ImageField(upload_to="upload/")
    created_on=models.DateTimeField(auto_now_add=True)
    status=models.ForeignKey(
        Status,
        null=True,
        default=None,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return f"{self.title} - {self.author}"