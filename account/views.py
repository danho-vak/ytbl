from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import login, logout, update_session_auth_hash
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib.auth.decorators import login_required

from account.forms import UserCreationForm, UserProfileForm
from account.models import User

# Create your views here.
def signUp(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, r'반가워요! 로그인해주세요 :)')
        else:
            messages.error(request, r'회원가입 실패..!')
        return redirect('account:signIn')

    form = UserCreationForm()
    return render(request, 'account/account_create.html', {'form':form})


def signIn(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        # AuthenticationForm은 유저가 존재하는지 검증하는 모델 폼임
        # parameter로 첫번째 request, 두번째는 브라우저 쿠키 또는 세션 유효성 검증을 원할시 request.method 객체를 또 넣어줌
        if form.is_valid():
            login(request, form.get_user())
            messages.success(request, request.user.username+r'님, 반가워요!')
            return redirect('ytbl:showMap')
        else:

            messages.error(request, r'로그인 실패!')
            return redirect('account:signIn')

    form = AuthenticationForm()
    return render(request, 'account/account_login.html', {'form':form})

@login_required
def logOut(request):
    logout(request)
    messages.success(request, r'로그아웃')
    return redirect('ytbl:showMap')


@login_required
def profile(request):
    item = get_object_or_404(User, pk=request.user.id)
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=item)
        if form.is_valid():
            user = form.save()

        return redirect('ytbl:showMap')

    form = UserProfileForm(instance=item)
    return render(request, 'account/account_profile.html', {'form':form})


@login_required
def changePassword(request):
    user = request.user
    if request.method == 'POST':
        form = PasswordChangeForm(user, request.POST)
        if form.is_valid():
            new_password = form.save()
            update_session_auth_hash(request, new_password)   # 비밀번호 변경 후 자동 로그인
            messages.success(request, r'비밀번호가 정상적으로 변경되었어요')
        else:
            messages.error(request, r'비밀번호를 아래 규칙에 맞게 변경해주세요')
        return redirect('ytbl:showMap')

    form = PasswordChangeForm(user)
    return render(request, 'account/account_password.html', {'form': form})


@login_required
def userDelete(requset):
    user = User.objects.get(email=requset.user.get_username())
    user.delete()
    return redirect('ytbl:showMap')