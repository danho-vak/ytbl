from django.urls import path
import board.views

app_name = 'board'

urlpatterns =[
    # posts
    path('', board.views.boardList, name='boardList'),
    path('create/', board.views.boardCreate, name='boardCreate'),
    path('<int:board_id>/', board.views.boardDetail, name='boardDetail'),
    path('<int:board_id>/delete', board.views.boardDelete, name='boardDelete'),
    path('<int:board_id>/update/', board.views.boardUpdate, name='boardUpdate'),

    # comments
    path('<int:board_id>/comment/create/', board.views.boardCommentCreate, name='boardCommentCreate'),
    path('<int:board_id>/comment/<int:comment_id>/delete/', board.views.boardCommentDelete, name='boardCommentDelete'),
    path('<int:board_id>/comment/<int:parent_id>/reCreate/', board.views.boardReCommentCreate, name='boardReCommentCreate'),
]