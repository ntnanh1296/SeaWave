# post_service/models.py

from django.db import models

class Post(models.Model):
    author = models.ForeignKey('user_service.CustomUser', on_delete=models.CASCADE)
    text = models.TextField()
    media = models.ImageField( null=True, blank=True)
    media_url = models.URLField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    like_count = models.IntegerField(default=0)
    share_count = models.IntegerField(default=0)
    comment_count = models.IntegerField(default=0)

class PostLike(models.Model):
    user = models.ForeignKey('user_service.CustomUser', on_delete=models.CASCADE, related_name='postLikes')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='postLikes')
    created_at = models.DateTimeField(auto_now_add=True)
    
class Comment(models.Model):
    text = models.TextField()
    user = models.ForeignKey('user_service.CustomUser', on_delete=models.CASCADE, related_name='comments')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    created_at = models.DateTimeField(auto_now_add=True) 
    like_count = models.IntegerField(default=0)  

class CommentLike(models.Model):
    user = models.ForeignKey('user_service.CustomUser', on_delete=models.CASCADE, related_name='commentLikes')
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name='commentLikes')
    created_at = models.DateTimeField(auto_now_add=True)