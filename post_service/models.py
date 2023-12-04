# post_service/models.py

from django.db import models

class Post(models.Model):
    text = models.TextField()
    media = models.ImageField(upload_to='post_photos/', null=True, blank=True)
    media_url = models.URLField(blank=True)
    author = models.ForeignKey('user_service.CustomUser', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    like_count = models.IntegerField(default=0)

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
