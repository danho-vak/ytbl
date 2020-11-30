import os

from django.db import models
from account.models import User
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill
# Create your models here.

class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.CharField(max_length=300, null=False)
    images = models.ImageField(blank=True, null=True, upload_to='social_images')
    likes = models.PositiveIntegerField(default=0)
    like_users = models.ManyToManyField(User, related_name='like_posts', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.content


class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comment_author')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comment_post')
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)
    content = models.CharField(max_length=200, null=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.content

    class Meta:
        db_table = 'post_comment'