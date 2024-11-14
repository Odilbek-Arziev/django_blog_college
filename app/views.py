from django.shortcuts import render
from .models import Post
from django.http import HttpResponse


def home(request):
    posts = Post.objects.all()
    return render(request, "home.html", {"posts": posts})
