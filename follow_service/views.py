from rest_framework import generics, permissions
from .models import Follower
from .serializers import FollowerSerializer
from django.shortcuts import get_object_or_404
from user_service.models import CustomUser
from rest_framework.response import Response
from rest_framework import status

class FollowerListView(generics.ListAPIView):
    serializer_class = FollowerSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Follower.objects.filter(user=self.request.user)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        followers_count = queryset.count()
        serializer = self.serializer_class(queryset, many=True)
        return Response({'count': followers_count, 'followers': serializer.data})

class FollowingListView(generics.ListAPIView):
    serializer_class = FollowerSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Follower.objects.filter(follower=self.request.user)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        following_count = queryset.count()
        serializer = self.serializer_class(queryset, many=True)
        return Response({'count': following_count, 'following': serializer.data})

class FollowUserView(generics.GenericAPIView):
    serializer_class = FollowerSerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user_id = self.kwargs.get('user_id')
        user_to_follow = get_object_or_404(CustomUser, id=user_id)

        # Check if the user is already being followed
        if Follower.objects.filter(user=user_to_follow, follower=request.user).exists():
            # Unfollow the user
            Follower.objects.filter(user=user_to_follow, follower=request.user).delete()
            return Response({'detail': 'User unfollowed successfully.'}, status=status.HTTP_204_NO_CONTENT)
        else:
            # Follow the user
            serializer = self.get_serializer(data={'user': user_to_follow.id, 'follower': request.user.id})
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response({'detail': 'User followed successfully.'}, status=status.HTTP_201_CREATED)
