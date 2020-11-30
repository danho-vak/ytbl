from django.db import models
from django.conf import settings
import os
from account.models import User

class Board(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100, null=False)
    content = models.TextField(null=False)
    images = models.ImageField(blank=True, upload_to='board_images', null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='board_comment_author')
    board = models.ForeignKey(Board, on_delete=models.CASCADE)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)
    content = models.CharField(max_length=200, null=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.content

    class Meta:
        db_table = 'board_comment'