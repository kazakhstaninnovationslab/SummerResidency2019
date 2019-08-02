from django.db import models
from django.contrib.auth.models import User

class UserProfileInfo(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    profile_pic = models.ImageField(upload_to='media', default="145849.jpg")

    @property
    def __str__(self):
        return self.user.username


# Create your models here.


