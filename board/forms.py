from django import forms
from django.utils.translation import gettext_lazy as _
from board.models import Board, Comment

class BoardCreationForm(forms.ModelForm):
    class Meta:
        model = Board
        fields = ['title', 'content']
        labels = {
            'title':_('제목'),
            'content':_('내용'),
        }
        exclude = ['author', 'images']


class CommentCreationForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        labels = {
            'content': _('내용')
        }
        exclude = ['author', 'board']


class ReCommentCreationForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        exclude = ['author', 'board', 'parent']