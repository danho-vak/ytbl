from django import forms
from django.utils.translation import gettext_lazy as _
from social.models import Post, Comment

class PostCreationForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['content', 'images']
        labels = {
            'content':_('내용'),
        }
        exclude = ['author', 'likes', 'like_users']


class PostUpdateForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['content']
        exclude = ['author', 'likes', 'like_users', 'images']


class PostCommentCreationForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        labels = {
            'content': _('내용')
        }
        exclude = ['author', 'post']


class PostReCommentCreationForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        exclude = ['author', 'post', 'parent']

