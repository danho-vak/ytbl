from django.urls import path
import social.views

app_name = 'social'

urlpatterns = [
    path('', social.views.postList, name='postList'),
    path('<int:post_id>/', social.views.postDetail, name='postDetail'),
    path('more/', social.views.postListAjax, name='postListAjax'),
    path('create/', social.views.postCreate, name='postCreate'),
    path('update/', social.views.postUpdate, name='postUpdate'),
    path('delete/', social.views.postDelete, name='postDelete'),
    path('like/', social.views.postLike, name='postLike'),

    path('<int:post_id>/comment/create/', social.views.postCommentCreate, name='postCommentCreate'),
    path('comment/last/', social.views.getLastComment, name='getLastComment'),
    path('comment/delete/', social.views.postCommentDelete, name='commentDelete'),
]