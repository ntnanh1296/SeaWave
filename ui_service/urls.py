from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('posts/create/', views.create_post, name='create-post'),
    path('posts/<int:pk>/', views.PostDetailView.as_view(), name='post-detail'),
    path('posts/<int:pk>/edit/', views.edit_post, name='edit-post'),
    path('posts/<int:pk>/delete/', views.delete_post, name='delete-post'),
    path('posts/<int:pk>/comments/', views.create_comment, name='create-comment'),
    path('comments/<int:pk>/edit/', views.edit_comment, name='edit-comment'),
    path('comments/<int:pk>/delete/', views.delete_comment, name='delete-comment'),
    path('comments/<int:pk>/', views.CommentDetailView.as_view(), name='comment-detail'),
    path('posts/<int:pk>/like/', views.like_post, name='like-post'),
    path('comments/<int:pk>/like/', views.like_comment, name='like-comment'),
    path('users/<str:username>/', views.user_detail, name='user-profile'),
    path('users/<str:username>/posts/', views.UserPostList.as_view(), name='user-post-list'),
    path('users/follow/<str:username>/', views.follow_unfollow_user, name='follow-unfollow-user'),
    path('users/<str:username>/update/', views.update_profile, name='update-profile'),
    path('posts/<int:post_id>/share/', views.share_post, name='share-post'),
    path('posts/<int:post_id>/get_comments/', views.get_comments, name='get-comments'),
    path('chat/<int:recipient_id>/<int:sender_id>/', views.ChatView.as_view(), name='chat'),
]

