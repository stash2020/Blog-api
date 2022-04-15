import os
from django.conf import settings
from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import Post, Comment, Like

User = get_user_model()

class PostCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = [
            "title",            
            "body"            
        ]

    def validate_title(self, value):
        if len(value) > 100:
            return serializers.ValidationError("Max title length is 100 characters")
        return value

    def validate_body(self, value):
        if len(value) > 1000:
            return serializers.ValidationError("Max post length is 1000 characters")
        return value

   

class PostListSerializer(serializers.ModelSerializer):
    #url = serializers.SerializerMethodField()
    comments = serializers.SerializerMethodField(read_only=True)
    likes = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Post
        fields = [
            "id",   
            #"url",         
            "title",
            "author",            
            "comments",
            "likes",
        ]

    def get_comments(self, obj):
        qs = Comment.objects.filter(parent=obj).count()
        return qs

    def get_likes(self, obj):
        qs = Like.objects.filter(parent=obj).count()
        return qs

    '''
    def get_url(self, obj):
        return obj.get_api_url()
    '''

class PostDetailSerializer(serializers.ModelSerializer):
    id = serializers.SerializerMethodField(read_only=True)
    author = serializers.PrimaryKeyRelatedField(read_only=True)
    comments = serializers.SerializerMethodField(read_only=True)
    likes = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Post
        fields = [
            "id",     
            "title",            
            "body",
            "author",            
            "created_at",
            "updated_at",
            "comments",
            "likes",
        ]

    def get_id(self, obj):
        return obj.id

    def get_comments(self, obj):
        qs = Comment.objects.filter(parent=obj)
        try:
            serializer = CommentSerializer(qs, many=True)
        except Exception as e:
            print(e)
        return serializer.data

    def get_likes(self, obj):
        qs = Like.objects.filter(parent=obj)
        try:
            serializer = LikeSerializer(qs, many=True)
        except Exception as e:
            print(e)
        return serializer.data


class CommentSerializer(serializers.ModelSerializer):
    comment_id = serializers.IntegerField(source = 'id')

    class Meta:
        model = Comment
        fields = [
            "id",
            "comment_id",
            "parent",
            "author",
            "body",
            "created_at",
            "updated_at",
        ]

class CommentCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = [
            "body",
        ]


class LikeSerializer(serializers.ModelSerializer):
    like_id = serializers.IntegerField(source = 'id')

    class Meta:
        model = Like
        fields = [
            "id",     
            "like_id",
            "parent",
            "author",   
            "created_at",            
        ]

class LikeCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ''
