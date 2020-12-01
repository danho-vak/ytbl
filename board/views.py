from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Count

from board.forms import BoardCreationForm, CommentCreationForm, ReCommentCreationForm
from board.models import Board, Comment
from account.models import User


# Create your views here.
# Board CRUD
def boardList(request):
    board_item = Board.objects.all().annotate(comment_count=Count('comment')).select_related().order_by('-created_at')
    paginator = Paginator(board_item, 10)
    page = request.GET.get('page')
    items = paginator.get_page(page)
    return render(request, 'board/board_list.html', {'items':items})


def boardDetail(request, board_id):
    if board_id is not None:
        # 상세페이지 데이터
        item = get_object_or_404(Board, pk=board_id)
        comments = Comment.objects.filter(board=item).all()

        # 상세페이지안에 뿌려줄 list 정보
        board_item = Board.objects.all().annotate(comment_count=Count('comment')).select_related().order_by('-created_at')
        paginator = Paginator(board_item, 10)
        page = request.GET.get('page')
        items = paginator.get_page(page)

        context = {
            'item':item,
            'comments':comments,
            'list_items':items,
        }

        return render(request, 'board/board_detail.html', context)


@ login_required
def boardCreate(request):
    if request.method == 'POST':
        author = get_object_or_404(User, email=request.user.get_username())

        form = BoardCreationForm(request.POST, request.FILES)
        if form.is_valid():
            new_item = form.save(commit=False)
            new_item.author = author
            new_item.save()
            messages.success(request, r'게시글 작성 완료!')
        else:
            messages.error(request, r'게시글 작성에 실패했어요')
        return redirect('board:boardList')

    form = BoardCreationForm()
    return render(request, 'board/board_create.html', {'form': form})


@login_required
def boardDelete(request, board_id):
    if board_id is not None:
        item = get_object_or_404(Board, pk=board_id)
        if request.user.get_username() == item.author.email or request.user.is_admin:
            item.images.delete() # 서버에 저장된 image 삭제
            item.delete()
            messages.success(request, r'정상적으로 삭제되었습니다.')
            return redirect('board:boardList')
    return redirect('board:boardDetail', board_id=board_id)


@login_required
def boardUpdate(request, board_id):
    if request.method == 'POST' and board_id is not None:
        item = get_object_or_404(Board, pk=board_id)
        if request.user.get_username() == item.author.email:
            form = BoardCreationForm(request.POST, request.FILES, instance=item)

            if form.is_valid():
                form = form.save(commit=False)
                if item.images is not None:  # 기존 board object에 이미지가 있으면
                    item.images.delete() # 기존 이미지 삭제

                item.save()
                messages.success(request, r'게시글을 수정했어요')
            else:
                messages.error(request, r'수정에 실패했어요')
            return redirect('board:boardDetail', board_id=board_id)

    item = get_object_or_404(Board, pk=board_id)
    form = BoardCreationForm(instance=item)
    return render(request, 'board/board_update.html', {'form':form})


# ------------------------------------------------------------------------------------------------------

# Comment CD
@login_required
def boardCommentCreate(request, board_id):
    if request.method == 'POST' and board_id is not None:
        form = CommentCreationForm(request.POST)
        if form.is_valid():
            new_item = form.save(commit=False)
            new_item.author = get_object_or_404(User, email=request.user.get_username())
            new_item.board = get_object_or_404(Board, pk=board_id)
            new_item.save()
            messages.success(request, r'댓글 작성 성공')
        else:
            messages.error(request, r'댓글 작성에 실패했어요')
    return redirect('board:boardDetail', board_id=board_id)


@login_required
def boardCommentDelete(request, board_id, comment_id):
    if (board_id is not None) and (comment_id is not None):
        item = get_object_or_404(Comment, pk=comment_id)
        if request.user.get_username() == item.author.email or request.user.is_admin:
            item.delete()
            messages.success(request, r'댓글을 성공적으로 삭제했어요')

    return redirect('board:boardDetail', board_id=board_id)


@login_required
def boardReCommentCreate(request, board_id, parent_id):
    if request.method == 'POST' and board_id and parent_id is not None:
        re_comment = ReCommentCreationForm(request.POST)
        if re_comment.is_valid():
            new_item = re_comment.save(commit=False)
            new_item.author = User.objects.get(email=request.user.get_username())
            new_item.board = Board.objects.get(pk=board_id)
            new_item.parent = Comment.objects.get(pk=parent_id)
            new_item.save()
            messages.success(request, r'댓글 작성 성공')
        else:
            messages.error(request, r'댓글 작성에 실패했어요')

    return redirect('board:boardDetail', board_id=board_id)
