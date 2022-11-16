from datetime import datetime

from django.db import models

from django.contrib.auth.models import User


class Status(models.TextChoices):

    POST = 'PO', 'Post'
    NEWS = 'NE', 'News'


class Author(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_rate = models.IntegerField(default=0)
    full_name = models.CharField(max_length=255)

    def update_rating(self):
        self.author_rate = 0
        for post in Post.objects.filter(author=self.user):
            self.author_rate += post.post_rate * 3
            for comment in Comment.objects.filter(posts=post):
                self.author_rate += comment.comment_rate
        for comment in Comment.objects.filter(users=self.user):
            self.author_rate += comment.comment_rate
        self.save()


class Category(models.Model):

    name = models.CharField(max_length=255, unique=True)


class Post(models.Model):

    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    status = models.CharField(max_length=2, choices=Status.choices, default=Status.POST)
    time_post = models.DateTimeField(auto_now_add=True)
    categories = models.ManyToManyField(Category, through='PostCategory')
    headline = models.CharField(max_length=255)
    content = models.TextField()
    post_rate = models.IntegerField(default=0)

    def like_post(self, amount=1):
        self.post_rate += amount
        self.save()


    def dislike_post(self,amount=1):
        self.post_rate -= amount
        self.save()

class PostCategory(models.Model):

    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comment(models.Model):

    posts = models.ForeignKey(Post, on_delete=models.CASCADE)
    users = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    time_create = models.DateTimeField(auto_now_add=True)
    comment_rate = models.IntegerField(default=0)

    def like_comment(self, amount=1):
        self.comment_rate += amount
        self.save()

    def dislike_comment(self, amount=1):
        self.comment_rate -= amount
        self.save()
