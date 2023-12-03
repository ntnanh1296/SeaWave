from django.urls import path
from .views import FollowerListView, FollowingListView, FollowUserView

urlpatterns = [
    path('followers/', FollowerListView.as_view(), name='followers-list'),
    path('following/', FollowingListView.as_view(), name='following-list'),
    path('following/users/<int:user_id>/', FollowUserView.as_view(), name='follow-user'),
]
