from django.urls import path
from .views import *


urlpatterns = [
    path("", home, name="home"),
    path("post_detail/<int:pk>", post_detail, name="post_detail"),
    path("post_create/", post_create, name="post_create"),
    path("post_delete/<int:pk>", post_delete, name="post_delete"),
    path("post_edit/<int:pk>", post_edit, name="post_edit"),
    path("forbidden/", forbidden, name="forbidden"),
    path("not_found/", not_found, name="not_found"),
    path("post_like/<int:pk>", post_like, name="post_like"),
    path("post_dislike/<int:pk>", post_dislike, name="post_dislike"),
    path("comment_edit/<int:pk>", comment_edit, name="comment_edit"),
    path("comment_delete/<int:pk>", comment_delete, name="comment_delete"),
    path('comment_like/<int:pk>', comment_like, name='comment_like'),
    path('comment_dislike/<int:pk>', comment_dislike, name='comment_dislike'),
]
