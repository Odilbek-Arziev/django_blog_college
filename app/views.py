from django.shortcuts import render, redirect
from .models import Post
from django.http import HttpResponse
from .forms import PostForm
from django.contrib.auth.decorators import login_required


def home(request):
    posts = Post.objects.all()
    return render(request, "home.html", {"posts": posts})


def post_detail(request, pk):
    post = Post.objects.get(pk=pk)
    return render(request, "post.html", {"post": post})


@login_required(login_url="users:login")
def post_create(request):
    if request.method == "POST":

        form = PostForm(request.POST, request.FILES)

        if form.is_valid():
            instance = form.save(commit=False)
            instance.author = request.user
            instance.save()

            return redirect("app:home")
    else:
        form = PostForm()

    return render(request, "post_create.html", {"form": form})


@login_required(login_url="users:login")
def post_delete(request, pk):
    post = Post.objects.get(pk=pk)

    if post.author != request.user:
        return redirect("app:forbidden")

    if request.method == "POST":
        post.delete()
        return redirect("app:home")

    return render(request, "post_delete.html", {"post": post})


@login_required(login_url="users:login")
def post_edit(request, pk):
    post = Post.objects.get(pk=pk)

    if post.author != request.user:
        return redirect("app:forbidden")

    if request.method == "POST":
        form = PostForm(request.POST, request.FILES, instance=post)
        form.save()
        return redirect("app:post_detail", pk=post.pk)
    else:
        form = PostForm(instance=post)

    return render(request, "post_edit.html", {"form": form})


def forbidden(request):
    return render(request, "forbidden.html")


def not_found(request):
    return render(request, "404.html")


@login_required(login_url="users:login")
def post_like(request, pk):
    post_data = Post.objects.get(pk=pk)
    user = request.user

    if user not in post_data.likes.all():
        post_data.likes.add(user)
        post_data.dislikes.remove(user)
    elif user in post_data.likes.all():
        post_data.likes.remove(user)

    return redirect("app:post_detail", pk=post_data.pk)


@login_required(login_url="users:login")
def post_dislike(request, pk):
    post_data = Post.objects.get(pk=pk)
    user = request.user

    if user not in post_data.dislikes.all():
        post_data.dislikes.add(user)
        post_data.likes.remove(user)
    elif user in post_data.dislikes.all():
        post_data.dislikes.remove(user)

    return redirect("app:post_detail", pk=post_data.pk)
