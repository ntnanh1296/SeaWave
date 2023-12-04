from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('posts/', views.PostList.as_view(), name='post-list'),
    path('posts/create/', views.create_post, name='create-post'),
    path('posts/<int:pk>/', views.PostDetailView.as_view(), name='post-detail'),
    
]

#
#  urlpatterns = [
#     path('', views.home, name='home'),
#     path('posts/', views.PostList.as_view(), name='post-list'),
#     path('posts/create/', views.create_post, name='create-post'),
#     path('posts/<int:pk>/', views.PostDetailView.as_view(), name='post-detail'),
#     path('posts/<int:pk>/edit/', views.edit_post, name='edit-post'),
#     path('posts/<int:pk>/delete/', views.delete_post, name='delete-post'),
#     path('posts/<int:pk>/comments/', views.create_comment, name='create-comment'),
#     path('comments/<int:pk>/edit/', views.edit_comment, name='edit-comment'),
#     path('comments/<int:pk>/delete/', views.delete_comment, name='delete-comment'),
#     path('api/posts/<int:pk>/like/', views.like_post, name='like-post'),
#     path('comments/<int:pk>/like/', views.like_comment, name='like-comment'),
#     path('users/<str:username>/', views.UserProfileView.as_view(), name='user-profile'),
#     path('users/<str:username>/posts/', views.UserPostList.as_view(), name='user-post-list'),
#     path('register/', views.register, name='register'),
#     path('login/', views.user_login, name='login'),
#     path('logout/', views.user_logout, name='logout'),
# ]
#     # API URLs
#     # path('api/posts/', views.PostViewSet.as_view({'get': 'list', 'post': 'create'}), name='api-post-list'),
#     # path('api/posts/<int:pk>/', views.PostViewSet.as_view({'get': 'retrieve', 'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'}), name='api-post-detail'),
#     # path('api/comments/', views.CommentViewSet.as_view({'get': 'list', 'post': 'create'}), name='api-comment-list'),
#     # path('api/comments/<int:pk>/', views.CommentViewSet.as_view({'get': 'retrieve', 'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'}), name='api-comment-detail'),
#     # path('api/post-likes/', views.PostLikeViewSet.as_view({'get': 'list', 'post': 'create'}), name='api-post-like-list'),
#     # path('api/post-likes/<int:pk>/', views.PostLikeViewSet.as_view({'get': 'retrieve', 'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'}), name='api-post-like-detail'),
#     # path('api/comment-likes/', views.CommentLikeViewSet.as_view({'get': 'list', 'post': 'create'}), name='api-comment-like-list'),
#     # path('api/comment-likes/<int:pk>/', views.CommentLikeViewSet.as_view({'get': 'retrieve', 'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'}), name='api-comment-like-detail'),
#     # path('api/user-profiles/', views.UserProfileViewSet.as_view({'get': 'list', 'post': 'create'}), name='api-user-profile-list'),
#     # path('api/user-profiles/<int:pk>/', views.UserProfileViewSet.as_view({'get': 'retrieve', 'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'}), name='api-user-profile-detail'),
# ]