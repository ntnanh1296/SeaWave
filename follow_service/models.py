from django.db import models
from user_service.models import CustomUser

class Follower(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='followers')
    follower = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='following')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['user', 'follower']
