# post_service/models.py

from django.db import models

class Post(models.Model):
    text = models.TextField()
    photo = models.ImageField(upload_to='post_photos/', null=True, blank=True)
    author = models.ForeignKey('user_service.CustomUser', on_delete=models.CASCADE)
    time_create = models.DateTimeField(auto_now_add=True)
    time_update = models.DateTimeField(auto_now=True)

    @property
    def like_count(self):
        return Like.objects.filter(post=self).count()

class Like(models.Model):
    user = models.ForeignKey('user_service.CustomUser', on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    
class Comment(models.Model):
    text = models.TextField()
    user = models.ForeignKey('user_service.CustomUser', on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
