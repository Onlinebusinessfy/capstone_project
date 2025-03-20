from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Profile(models.Model):
    picture = models.ImageField(upload_to="profile_pic/", blank=True, null=True)
    phone_number = models.CharField(max_length=25)
    street = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    zip_code = models.CharField(max_length=10)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="profile")