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

    def post(self, request, *args, **kwargs):
        post_id = self.kwargs.get('post_id')
        print(post_id)
        user = request.user

        existing_like = Like.objects.filter(post=post_id, user=user).first()

        if existing_like:

            redis_conn = get_redis_connection()
            redis_conn.srem(f'post_likes:{post_id}', existing_like.id)
            existing_like.delete()

            post = Post.objects.get(id=post_id)
            post.save()
            return Response({'detail': 'Post unliked successfully.'}, status=status.HTTP_204_NO_CONTENT)
        else:
            post = get_object_or_404(Post, pk=post_id)
            serializer = self.get_serializer(data={'post': post.id, 'user': user.id})
            serializer.is_valid(raise_exception=True)
            serializer.save()
            redis_conn = get_redis_connection()
            redis_conn.sadd(f'post_likes:{post_id}', serializer.instance.id)
            post = Post.objects.get(id=post_id)
            post.save()
            
            return Response({'detail': 'Post liked successfully.'}, status=status.HTTP_201_CREATED)

class LikeDetailView(generics.RetrieveDestroyAPIView):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer
    permission_classes = [permissions.IsAuthenticated]

class CommentListCreateView(generics.ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        post_id = self.kwargs.get('post_id')
        user = request.user
        text = request.data.get('text')

        serializer = self.get_serializer(data={'text': text, 'user': user.id, 'post': post_id})
        serializer.is_valid(raise_exception=True)
        serializer.save()

        redis_conn = get_redis_connection()
        redis_conn.sadd(f'post_comments:{post_id}', serializer.instance.id)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

class CommentDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def put(self, request, *args, **kwargs):
        # Get user from request and post_id from URL
        user = self.request.user
        post_id = self.kwargs.get('post_id')

        instance = self.get_object()
        request.data['user'] = user.id
        request.data['post'] = post_id

        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        # Update Redis mapping for post-comments
        redis_conn = get_redis_connection()
        redis_conn.sadd(f'post_comments:{post_id}', serializer.instance.id)

        return Response(serializer.data)

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()

        # Remove from Redis mapping for post-comments
        redis_conn = get_redis_connection()
        redis_conn.srem(f'post_comments:{instance.post.id}', instance.id)

        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

