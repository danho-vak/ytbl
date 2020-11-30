from django.contrib import admin

# Register your models here.
from social.models import Post, Comment

admin.site.register(Post)
admin.site.register(Comment)
