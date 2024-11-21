from rest_framework import serializers
from .models import CustomUser, Post, Comment, Like

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id', 'username', 'email', 'bio', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = CustomUser.objects.create_user(**validated_data)
        return user


class PostSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    
    class Meta:
        model = Post
        fields = ('id', 'user', 'content', 'created_at', 'updated_at')

class CommentSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    post = serializers.ReadOnlyField(source='post.id')
    
    class Meta:
        model = Comment
        fields = ('id', 'user', 'post', 'content', 'created_at', 'updated_at')

class LikeSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    post = serializers.ReadOnlyField(source='post.id')
    
    class Meta:
        model = Like
        fields = ('id', 'user', 'post', 'created_at', 'updated_at')
