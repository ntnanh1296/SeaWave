# post_service/serializers.py

from rest_framework import serializers
from .models import Post, PostLike, Comment, CommentLike

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'
        read_only_fields = ['author']

    # def to_representation(self, instance):
    #     data = super().to_representation(instance)
    #     data['like_
    # count'] = instance.like_count
    #     return data

class PostLikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostLike
        fields = '__all__'
        # read_only_fields = ['user', 'post', 'created_at']

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'
        # read_only_fields = ['user', 'post']
class CommentLikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommentLike
        fields = '__all__'
