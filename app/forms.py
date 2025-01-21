from django import forms
from .models import Post, Comment


class PostForm(forms.ModelForm):
    title = forms.CharField(
        widget=forms.TextInput(attrs={"placeholder": "Название поста"}),
    )
    body = forms.CharField(widget=forms.Textarea(attrs={"placeholder": "Текст поста"}))

    class Meta:
        model = Post
        fields = ["title", "body", "image"]


class CommentForm(forms.ModelForm):
    body = forms.CharField(
        widget=forms.TextInput(
            attrs={"placeholder": "Введите ваш комментарий", "class": "input"}
        )
    )

    class Meta:
        model = Comment
        fields = ["body"]
