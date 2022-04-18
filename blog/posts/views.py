import logging

from django.shortcuts import render, redirect, get_object_or_404
from rest_framework.permissions import (
    IsAuthenticated,
    IsAuthenticatedOrReadOnly,
    AllowAny,
)
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import (
    CreateAPIView,
    DestroyAPIView,
    ListAPIView,
    UpdateAPIView,
    RetrieveAPIView,
    RetrieveUpdateAPIView,
    RetrieveUpdateDestroyAPIView,
    RetrieveDestroyAPIView,
)

#from rest_framework.pagination import PostLimitOffsetPagination
from .models import Post, Comment, Like
from .permissions import IsOwnerOrReadOnly, IsOwner
#from .mixins import MultipleFieldLookupMixin
from .serializers import (
    PostCreateUpdateSerializer,
    PostListSerializer,
    PostDetailSerializer,
    CommentSerializer,
    CommentCreateUpdateSerializer,
    LikeSerializer,
    LikeCreateUpdateSerializer,
)

# Create your views here.
class CreatePostAPIView(APIView):
    """
    post:
        Creates a new post instance. Returns created post data

        parameters: [title, body]
    """

    queryset = Post.objects.all()
    serializer_class = PostCreateUpdateSerializer
    permission_classes = [
        IsAuthenticated,
    ]

    def post(self, request, *args, **kwargs):
        serializer = PostCreateUpdateSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(author=request.user)
            return Response(serializer.data, status=201)
        else:
            return Response({"errors": serializer.errors}, status=400)


class ListPostAPIView(ListAPIView):
    """
    get:
        Returns a list of all existing posts
    """

    queryset = Post.objects.all()
    serializer_class = PostListSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    #pagination_class = PostLimitOffsetPagination


class DetailPostAPIView(RetrieveUpdateDestroyAPIView):
    """
    get:
        Returns the details of a post instance. Searches post using id field.

    put:
        Updates an existing post. Returns updated post data

        parameters: [title, body]

    delete:
        Delete an existing post

        parameters = [id]
    """

    queryset = Post.objects.all()
    lookup_field = "id"
    serializer_class = PostDetailSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]


class CreateCommentAPIView(APIView):
    """
    post:
        Create a comment instnace. Returns created comment data

        parameters: [id, body]

    """

    serializer_class = CommentCreateUpdateSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, id, *args, **kwargs):
        post = get_object_or_404(Post, id=id)
        serializer = CommentCreateUpdateSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(author=request.user, parent=post)
            return Response(serializer.data, status=201)
        else:
            return Response({"errors": serializer.errors}, status=400)


class ListCommentAPIView(APIView):
    """
    get:
        Returns the list of comments on a particular post
    """

    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request, id):
        post = Post.objects.get(id=id)        
        comments = Comment.objects.filter(parent=post)
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data, status=200)


class MultipleFieldLookupMixin:
    """
    Mixin to filter comments based on [post id] and [comment id]
    """

    def get_object(self):             
        queryset = self.get_queryset()  # Get the base queryset        
        queryset = self.filter_queryset(queryset)  # Apply any filter backends        
        filter = {}
        
        for field in self.lookup_fields:
            try:
                filter[field] = self.kwargs[field]
            except:
                pass

        filter["parent"] = self.kwargs["id"]
        filter["id"] = self.kwargs["id_2"]
        
        obj = get_object_or_404(queryset, **filter)  # Lookup the object
        self.check_object_permissions(self.request, obj)        
        return obj


class DetailCommentAPIView(MultipleFieldLookupMixin, RetrieveUpdateDestroyAPIView):
    """
    get:
        Returns the details of a comment instance. Searches comment using comment id and post id in the url.

    put:
        Updates an existing comment. Returns updated comment data

        parameters: [parent, author, body]

    delete:
        Delete an existing comment

        parameters: [parent, author, body]
    """

    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    queryset = Comment.objects.all()        
    lookup_fields = ("id", "parent_id")    
    serializer_class = CommentCreateUpdateSerializer


class CreateLikeAPIView(APIView):
    """
    post:
        Create a like instnace. Returns created like data

        parameters: [id]

    """

    serializer_class = LikeCreateUpdateSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, id, *args, **kwargs):
        post = get_object_or_404(Post, id=id)
        likes = Like.objects.filter(parent=post, author=request.user.id)        
        if likes.exists():            
            return Response({"status": "error", "message": "user already liked this post."}, status=400)
        
        serializer = LikeCreateUpdateSerializer(data=request.data)        
        if serializer.is_valid(raise_exception=True):            
            serializer.save(author=request.user, parent=post)
            return Response(serializer.data, status=201)
        else:
            return Response({"errors": serializer.errors}, status=400)

class ListLikeAPIView(APIView): 
    """
    get:
        Returns the list of like on a particular post
    """

    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request, id):
        post = Post.objects.get(id=id)        
        likes = Like.objects.filter(parent=post)
        serializer = LikeSerializer(likes, many=True)
        return Response(serializer.data, status=200)

class DetailLikeAPIView(MultipleFieldLookupMixin, RetrieveDestroyAPIView):
    """
    get:
        Returns the details of a like instance. Searches like using like id and post id in the url.
    
    delete:
        Delete an existing like

        parameters: [parent, author]
    """
    
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    queryset = Like.objects.all()        
    lookup_fields = ("id", "parent_id")
    serializer_class = LikeCreateUpdateSerializer
    