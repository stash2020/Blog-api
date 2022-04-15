from django.urls import path
from .views import (
    CreatePostAPIView,
    ListPostAPIView,
    DetailPostAPIView,
    CreateCommentAPIView,
    ListCommentAPIView,
    DetailCommentAPIView,
    ListLikeAPIView,
    CreateLikeAPIView,
    DetailLikeAPIView,
)

app_name = "posts"

urlpatterns = [
    path("", ListPostAPIView.as_view(), name="list_post"),
    path("create/", CreatePostAPIView.as_view(), name="create_post"),
    path("<int:id>/", DetailPostAPIView.as_view(), name="post_detail"),
    path('<int:id>/comment/', ListCommentAPIView.as_view(), name="list_comment"),
    path(
        '<int:id>/comment/create/',
        CreateCommentAPIView.as_view(),
        name="create_comment",
    ),
    path(
        "<int:id>/comment/<int:comment_id>/",
        DetailCommentAPIView.as_view(),
        name="comment_detail",
    ),
    path('<int:id>/like/', ListLikeAPIView.as_view(), name="list_like"),
    path('<int:id>/like/create/', CreateLikeAPIView.as_view(), name="create_like",),
    path("<int:id>/like/<int:like_id>/", DetailLikeAPIView.as_view(), name="like_detail",),
]

