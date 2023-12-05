
from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager


default_avatar = '../media/avatar.png'
default_photo_cover = '../media/photo_cover.png'
class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    gender = models.CharField(max_length=10, blank=True, null=True)
    birthday = models.DateField(blank=True, null=True)
    bio = models.TextField(blank=True)
    avatar = models.ImageField(default=default_avatar)
    avatar_url = models.URLField(default=default_avatar)
    cover_photo = models.ImageField(default=default_photo_cover)
    cover_photo_url = models.URLField(default=default_photo_cover)



    groups = models.ManyToManyField(
        "auth.Group",
        related_name="customuser_set",
        related_query_name="customuser",
        blank=True,
        help_text="The groups this user belongs to. A user will get all permissions granted to each of their groups.",
    )
    user_permissions = models.ManyToManyField(
        "auth.Permission",
        related_name="customuser_set",
        related_query_name="customuser",
        blank=True,
        help_text="Specific permissions for this user.",
    )

    def __str__(self):
        return self.username