from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    picture = models.ImageField(upload_to="profile_pic/", blank=True, null=True)
    name = models.CharField(max_length=250, blank=True, null=True)
    phone_number = models.CharField(max_length=25, blank=True, null=True)
    city = models.CharField(max_length=255, blank=True, null=True)
    state = models.CharField(max_length=255, blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="profile")
    description = models.TextField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} - {self.user.username}"
