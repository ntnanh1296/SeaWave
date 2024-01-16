# in your app's admin.py

from django.contrib import admin
from user_service.models import CustomUser
from post_service.models import Post, Comment, PostLike, CommentLike

admin.site.register(CustomUser)
admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(PostLike)
admin.site.register(CommentLike)
