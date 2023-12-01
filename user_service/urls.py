
from .views import UserListCreateView, UserDetailView, LoginAPIView
from django.urls import path


urlpatterns = [
    path('api/users/', UserListCreateView.as_view(), name='user-list-create'),
    path('api/users/<int:pk>/', UserDetailView.as_view(), name='user-detail'),
    path('api/users/login/', LoginAPIView.as_view(), name='user-login'),
] 

