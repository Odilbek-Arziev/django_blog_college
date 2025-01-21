from django.db import models
from django.contrib.auth.models import User


class Post(models.Model):
    title = models.CharField(max_length=255)
    body = models.TextField()
    author = models.ForeignKey(
        User, null=True, blank=True, on_delete=models.CASCADE, default=1
    )
    date_added = models.DateField(auto_now_add=True)
    image = models.ImageField(default="default.png", blank=True)
    likes = models.ManyToManyField(User, related_name="likes")
    dislikes = models.ManyToManyField(User, related_name="dislikes")


    def __str__(self):
        return self.title

    def snippet(self):
        return self.body[:20].strip()

class Comment(models.Model):
    body = models.TextField()
    date_added = models.DateField(auto_now_add=True)
    is_edited = models.BooleanField(default=False)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.body
