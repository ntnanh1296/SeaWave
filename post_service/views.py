# post_service/views.py

from rest_framework import generics, permissions, status
from rest_framework.response import Response
from django.conf import settings
from .models import Post, Like, Comment
from .serializers import PostSerializer, LikeSerializer, CommentSerializer
from .utils import get_redis_connection
from user_service.models import CustomUser 
from django.shortcuts import get_object_or_404

class PostListCreateView(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def perform_create(self, serializer):
        author=self.request.user
        serializer.save(author=author)
        # Update Redis mapping for user-posts
        redis_conn = get_redis_connection()
        redis_conn.sadd(f'user_posts:{self.request.user.id}', serializer.instance.id)

class PostDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]

    def update(self, request, *args, **kwargs):
        post = self.get_object()

        # Check if the user making the request is the author of the post
        if request.user != post.author:
            print("Anh was here if")
            return Response({'detail': 'You do not have permission to perform this action.'}, status=status.HTTP_403_FORBIDDEN)

        print("Anh was here")
        serializer = self.get_serializer(post, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        # Update Redis mapping for user-posts
        redis_conn = get_redis_connection()
        redis_conn.sadd(f'user_posts:{request.user.id}', serializer.instance.id)

        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        post = self.get_object()

        # Check if the user making the request is the author of the post
        if request.user != post.author:
            print("Anh was here if")
            return Response({'detail': 'You do not have permission to perform this action.'}, status=status.HTTP_403_FORBIDDEN)


        print("Anh was here")
        # Remove from Redis mapping for user-posts
        redis_conn = get_redis_connection()
        redis_conn.srem(f'user_posts:{post.author.id}', post.id)

        post.delete()

        return Response({'detail': 'Post deleted successfully.'}, status=status.HTTP_204_NO_CONTENT)

class LikeListView(generics.ListCreateAPIView):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
        # Update Redis mapping for post-likes
        redis_conn = get_redis_connection()
        redis_conn.sadd(f'post_likes:{serializer.instance.post.id}', serializer.instance.id)

class LikeDetailView(generics.RetrieveDestroyAPIView):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_destroy(self, instance):
        # Remove from Redis mapping for post-likes
        redis_conn = get_redis_connection()
        redis_conn.srem(f'post_likes:{instance.post.id}', instance.id)
        instance.delete()

class CommentListCreateView(generics.ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
        # Update Redis mapping for post-comments
        redis_conn = get_redis_connection()
        redis_conn.sadd(f'post_comments:{serializer.instance.post.id}', serializer.instance.id)

class CommentDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_update(self, serializer):
        serializer.save()
        # Update Redis mapping for post-comments
        redis_conn = get_redis_connection()
        redis_conn.sadd(f'post_comments:{serializer.instance.post.id}', serializer.instance.id)

    def perform_destroy(self, instance):
        # Remove from Redis mapping for post-comments
        redis_conn = get_redis_connection()
        redis_conn.srem(f'post_comments:{instance.post.id}', instance.id)
        instance.delete()
