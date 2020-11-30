from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashWidget
from account.models import User


# 유저 생성 폼
class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label='비밀번호', widget=forms.PasswordInput)
    password2 = forms.CharField(label='비밀번호 확인', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['email', 'username']
        labels = {
            'email': 'E-mail',
            'username': '닉네임',
        }

    # username 검증
    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('이미 존재하는 사용자명 입니다.')
        return username

    # email 검증
    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('이미 존재하는 Email 입니다.')
        return email

    # password 검증
    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError('비밀번호가 일치하지 않습니다.')
        return password2

    # 저장
    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user

# 수정 폼
class UserChangeForm(forms.ModelForm):
    # 화면에 뿌려줄 읽기 전용 데이터(수정 할 수 없음)
    password = ReadOnlyPasswordHashWidget()
    class Meta:
        model = User
        fields = ['email', 'username', 'password', 'is_active', 'is_admin']


    def clean_password(self):
        return self.initial['password']


# 프로필 폼
class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email', 'username']
        labels = {
            'email': 'E-mail',
            'username': '닉네임',
        }