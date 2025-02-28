from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission

class CustomUser(AbstractUser):
    # groups = models.ManyToManyField(
    #     Group,
    #     related_name="custom_user_groups",
    #     blank=True,
    # )
    # user_permissions = models.ManyToManyField(
    #     Permission,
    #     related_name="custom_user_permissions",
    #     blank=True,
    # )

    phone_no = models.CharField(max_length=15, blank=True, null=True)
    profile_pic = models.ImageField(upload_to='profile_pics/', default = 'profile_pics/default_pic.jpeg')
    bio = models.TextField(blank=True, null=True)
    location = models.TextField(default = "Enter your address")
    gc_coins = models.IntegerField(default=0)


# Create your models here.
