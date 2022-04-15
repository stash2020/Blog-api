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
)

#from .pagination import PostLimitOffsetPagination
from .models import Post, Comment
#from .permissions import IsOwnerOrReadOnly, IsOwner
#from .mixins import MultipleFieldLookupMixin
from .serializers import (
    PostCreateUpdateSerializer,
    PostListSerializer,
    PostDetailSerializer,
    CommentSerializer,
    CommentCreateUpdateSerializer,
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
            return Response(serializer.data, status=200)
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
    #permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]


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
            return Response(serializer.data, status=200)
        else:
            return Response({"errors": serializer.errors}, status=400)


class ListCommentAPIView(APIView):
    """
    get:
        Returns the list of comments on a particular post
    """

    #permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request, id):
        post = Post.objects.get(id=id)        
        comments = Comment.objects.filter(parent=post)
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data, status=200)


class MultipleFieldLookupMixin:
    """
    Mixin to filter comments based on slug and id
    """

    def get_object(self):     
        #logging.basicConfig(level=logging.INFO) 
        logging.info(">>>>>>>>>>>>>>>>")  
        queryset = self.get_queryset()  # Get the base queryset
        queryset = self.filter_queryset(queryset)  # Apply any filter backends
        filter = {}
        # for field in self.lookup_fields:
        #     if self.kwargs[field]: # Ignore empty fields.
        #         filter[field] = self.kwargs[field]
        parent_id = Post.objects.get(id=self.kwargs["id"]).id
        logging.info(parent_id)
        filter["parent"] = parent_id
        logging.info(self.kwargs["comment_id"])
        filter["id"] = self.kwargs["comment_id"]
        obj = get_object_or_404(queryset, **filter)  # Lookup the object
        self.check_object_permissions(self.request, obj)
        logging.info(">>>>>>>>>>>>>>>>")  
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

    #permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    queryset = Comment.objects.all()    
    lookup_fields = ["parent", "id"]
    serializer_class = CommentCreateUpdateSerializer
