import json
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.core.serializers.json import DjangoJSONEncoder
from django.http import HttpResponse, Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Count

from social.forms import PostCreationForm, PostCommentCreationForm, PostReCommentCreationForm, PostUpdateForm
from social.models import Post, Comment
from account.models import User


# social의 모든 post를 가져오는 함수
def postList(request):
    post_all = Post.objects.all().annotate(comment_count=Count('comment_post')).select_related().order_by('-created_at')
    paginator = Paginator(post_all, 5)
    page = request.POST.get('page')
    try:
        post_items = paginator.get_page(page)
    except PageNotAnInteger:
        post_items = paginator.get_page(1)
    except EmptyPage:
        post_items = paginator.get_page(paginator.num_pages)

    return render(request, 'social/post_list.html', {'items':post_items})


# 무한 스크롤 ajax에 호출되는 함수
def postListAjax(request):
    post_all = Post.objects.all().annotate(comment_count=Count('comment_post')).select_related().order_by('-created_at')
    paginator = Paginator(post_all, 5)
    page = request.POST.get('page')

    if int(page) > paginator.num_pages:
        raise Http404  # page값이 paginator의 마지막 값 보다 크면 404를 보냄
    else:
        post_items = None
        try:
            post_items = paginator.get_page(page)
        except PageNotAnInteger:
            post_items = paginator.get_page(1)
        except EmptyPage:
            post_items = paginator.get_page(paginator.num_pages)

        return render(request, 'social/post_list_more.html', {'more_posts': post_items})


# post의 detail을 처리하는 함수
def postDetail(request, post_id):
    if post_id:
        post = get_object_or_404(Post, pk=post_id)
        comments = Comment.objects.filter(post=post)
        context = {
            'post':post,
            'comments':comments
        }
        return render(request, 'social/post_detail.html', context)
    else:
        return redirect('social:postList')

# social의 post를 생성하는 함수
@login_required
def postCreate(request):
    if request.method == 'POST':
        author = get_object_or_404(User, email=request.user.get_username())
        form = PostCreationForm(request.POST, request.FILES)
        if form.is_valid():
            new_item = form.save(commit=False)
            new_item.author = author
            new_item.save()
            messages.success(request, r'게시물 등록 완료!')
        else:
            messages.error(request, r'게시글 등록 실패 :(')
        return redirect('social:postList')

    form = PostCreationForm()
    return render(request, 'social/post_create.html', {'form':form})


# social에 게시된 post를 update하는 함수 (cotent만, image 수정은 구현 안함)
@login_required
def postUpdate(request):
    if request.method == 'POST':
        post = get_object_or_404(Post, pk=request.POST.get('post_id'))
        if request.user.get_username() == post.author.email:
            form = PostUpdateForm(request.POST, instance=post)

            if form.is_valid():
                new_item = form.save(commit=False)
                new_item.content = request.POST.get('content')
                new_item.save()

        return redirect('social:postList')


# social에 게시된 post를 delete하는 함수
@login_required
def postDelete(request):
    if request.GET.get('post_id') is not None:
        post = get_object_or_404(Post, pk=request.GET.get('post_id'))
        if request.user.get_username() == post.author.email or request.user.is_admin:
            post.images.delete()

            post.delete()
            messages.success(request, '성공적으로 삭제했어요.')

    return redirect('social:postList')


def getImageDetail(request):
    post_id = request.POST.get('post_id')
    if post_id is not None:
        post = get_object_or_404(Post, pk=post_id)
        return HttpResponse(json.dumps(post.images), content_type='application/json')


# list에서 특정 post의 가장 마지막 댓글 넘겨주는 함수 (ajax로 호출)
def getLastComment(request):
    last_comment = Comment.objects.filter(post=request.GET.get('post_id')).last()
    return render(request, 'social/comment_last.html', {'comment':last_comment})


# post에 댓글을 생성하는 함수
@login_required
def postCommentCreate(request, post_id):
    if request.method == 'POST' and post_id:
        form = PostCommentCreationForm(request.POST)
        if form.is_valid():
            new_item = form.save(commit=False)
            new_item.author = User.objects.get(email = request.user.get_username())
            new_item.post = Post.objects.get(pk=post_id)
            new_item.save()
            messages.success(request, r'댓글 작성 성공')
        else:
            messages.error(request, r'댓글 작성에 실패했어요')
    return redirect('social:postList')


@login_required
def postCommentDelete(request):
    comment_id = request.POST.get('comment_id')
    if request.method == 'POST' and comment_id:
        comment = Comment.objects.get(pk=comment_id)
        comment.delete()
    return redirect('social:postList')


# post에 좋아요 눌렀을 시 호출되는 함수 (ajax로 호출)
@login_required
def postLike(request):  # 좋아요 기능 비동기식으로 바꾸자
    user = User.objects.get(email=request.user.get_username())
    target_post = request.GET.get('post_id')
    post = Post.objects.get(pk=target_post)
    if user in post.like_users.all():  # 해당 글 좋아요누른 유저 중 있으면
        post.like_users.remove(user)
        post.likes -= 1
        post.save()
    else:
        post.like_users.add(user)
        post.likes += 1
        post.save()

    return HttpResponse(json.dumps(post.likes), content_type="application/json")

