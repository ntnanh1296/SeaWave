# post_service/urls.py

from django.urls import path
from .views import (
    PostListCreateView, PostDetailView,
    LikeListView, LikeDetailView,
    CommentListCreateView, CommentDetailView
)

urlpatterns = [
    path('api/posts/', PostListCreateView.as_view(), name='post-list-create'),
    path('api/posts/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('api/posts/<int:post_id>/likes/', LikeListView.as_view(), name='like-list'),
    path('api/posts/<int:post_id>/likes/<int:pk>/', LikeDetailView.as_view(), name='like-detail'),
    path('api/posts/<int:post_id>/comments/', CommentListCreateView.as_view(), name='comment-list-create'),
    path('api/posts/comments/<int:pk>/', CommentDetailView.as_view(), name='comment-detail'),
]
