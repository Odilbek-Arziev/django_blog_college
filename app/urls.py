from django.urls import path
from .views import *
urlpatterns = [
    path('', home),
    path('post_detail/<int:pk>', post_detail, name='post_detail')
]
