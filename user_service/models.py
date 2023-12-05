
from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    gender = models.CharField(max_length=10, blank=True, null=True)
    birthday = models.DateField(blank=True, null=True)
    bio = models.TextField(blank=True)
   
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