from django.urls import path
from .views import UserListCreateView, UserDetailView, LoginAPIView

urlpatterns = [
    path('api/users/', UserListCreateView.as_view(), name='user-list-create'),
    path('api/users/<int:pk>/', UserDetailView.as_view(), name='user-detail'),
    path('api/users/login/', LoginAPIView.as_view(), name='user-login'),
]
