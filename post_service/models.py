# post_service/models.py

from django.db import models

class Post(models.Model):
    author = models.ForeignKey('user_service.CustomUser', on_delete=models.CASCADE)
    text = models.TextField()
    media = models.ImageField(upload_to='post_photos/', null=True, blank=True)
    media_url = models.URLField(blank=True)
    get_media_url = models.URLField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    like_count = models.IntegerField(default=0)

    def get_media_url(self):
        if self.media_url:
            return self.media_url.replace('gs://', 'https://firebasestorage.googleapis.com/v0/b/') + '?alt=media'
        return ''

    @property
    def like_count(self):
        return PostLike.objects.filter(post=self).count()

class PostLike(models.Model):
    user = models.ForeignKey('user_service.CustomUser', on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    
class Comment(models.Model):
    text = models.TextField()
    user = models.ForeignKey('user_service.CustomUser', on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True) 
    like_count = models.IntegerField(default=0)  

class CommentLike(models.Model):
    user = models.ForeignKey('user_service.CustomUser', on_delete=models.CASCADE, related_name='commentLikes')
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name='commentLikes')
    like_count = models.IntegerField(default=0)
