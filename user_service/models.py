
from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager

default_avatar = "../media/avatar.png"
default_photo_cover = "../media/photo_cover.png" 
default_avatar_url = 'https://firebasestorage.googleapis.com/v0/b/seawave-d58e4.appspot.com/o/avatar%2Favatar.png?alt=media&token=d042bdf1-e683-4ebc-8d74-1bc8a4fa27a8'
default_photo_cover_url = 'https://firebasestorage.googleapis.com/v0/b/seawave-d58e4.appspot.com/o/cover_photo%2Fphoto_cover.png?alt=media&token=1d034dad-bd80-47e0-8e2a-2e7537bded38'
class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    gender = models.CharField(max_length=10, blank=True, null=True)
    birthday = models.DateField(blank=True, null=True)
    bio = models.TextField(blank=True)
    avatar = models.ImageField(default=default_avatar)
    avatar_url = models.URLField(default=default_avatar_url)
    cover_photo = models.ImageField(default=default_photo_cover)
    cover_photo_url = models.URLField(default=default_photo_cover_url)



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