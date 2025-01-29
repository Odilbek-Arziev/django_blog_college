from django.shortcuts import render, redirect
from .models import Post, Comment
from django.http import HttpResponse
from .forms import PostForm, CommentForm
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator


def home(request):
    posts = Post.objects.all()
    quantity = int(request.GET.get("quantity", 3))
    posts = posts[:quantity]

    return render(
        request, "home.html", {"posts": posts, "all_posts": Post.objects.all().count()}
    )


def post_detail(request, pk):
    post = Post.objects.get(pk=pk)
    form = CommentForm(request.POST or None)
    comments = Comment.objects.filter(post=post)
    comments = Paginator(comments, 3)
    page = request.GET.get("page")
    comments = comments.get_page(page)

    if form.is_valid():
        if request.user.is_anonymous:
            return redirect("users:login")

        instance = form.save(commit=False)
        instance.post = post
        instance.author = request.user
        instance.save()
        return redirect("app:post_detail", pk=post.pk)

    return render(
        request, "post.html", {"post": post, "form": form, "comments": comments}
    )


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


def comment_edit(request, pk):
    comment = Comment.objects.get(pk=pk)
    form = CommentForm(request.POST or None, instance=comment)

    if comment.author != request.user:
        return redirect("app:forbidden")

    if form.is_valid():
        instance = form.save(commit=False)
        instance.is_edited = True
        instance.save()

        return redirect("app:post_detail", pk=comment.post.pk)

    # post_edit.html отлично подойдет в качестве шаблонизатора редактирования
    return render(request, "post_edit.html", {"form": form})


def comment_delete(request, pk):
    comment = Comment.objects.get(pk=pk)

    if comment.author != request.user:
        return redirect("app:forbidden")

    if request.method == "POST":
        comment.delete()
        return redirect("app:post_detail", pk=comment.post.pk)

    return render(request, "comment_delete.html", {"comment": comment})


@login_required(login_url="users:login")
def comment_like(request, pk):
    comment = Comment.objects.get(pk=pk)
    user = request.user
    likes = comment.likes

    if user not in likes.all():
        likes.add(user)
        comment.dislikes.remove(user)
    elif user in likes.all():
        likes.remove(user)

    return redirect("app:post_detail", pk=comment.post.pk)


@login_required(login_url="users:login")
def comment_dislike(request, pk):
    comment = Comment.objects.get(pk=pk)
    user = request.user
    dislikes = comment.dislikes

    if user not in dislikes.all():
        dislikes.add(user)
        comment.likes.remove(user)
    elif user in dislikes.all():
        dislikes.remove(user)

    return redirect("app:post_detail", pk=comment.post.pk)
