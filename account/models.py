from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser

# Create your models here.


# Custom User Model을 만들기 위해서는 다음 클래스(BaseUserManager, AbstractBaseUser)를 구현해야함
# 이때 BaseUserManager는 유저를 생성할 때 사용하는 헬퍼(Helper)클래스이며, 실제 모델은
# AbstractBaseUser을 상속받아 생성하는 클래스임

class UserManager(BaseUserManager):
    # UserManager는 아래와 같은 함수를 정의해야 함
    # create_user(*username_field*, password=None, **other_fields)
    # create_superuser(*username_field*, password, **other_fields)
    # 지금은 username을 email로 사용할 예정이므로 수정하여 적용함

    def create_user(self, email, username, password=None):
        if not email:
            raise ValueError('User must have an email address')

        user = self.model(
            email = self.normalize_email(email),
            username = username
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password):
        user = self.create_user(
            email = self.normalize_email(email),
            username = username,
            password = password
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    email = models.EmailField(
        verbose_name='email',
        max_length=255,
        unique=True,
    )
    username = models.CharField(
        verbose_name='username',
        max_length=100,
        unique=True,
    )

    created_at = models.DateTimeField(auto_now_add=True)

    # is_active, is_admin은 필수 필드
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = UserManager() # Helper클래스를 사용하도록 설정

    USERNAME_FIELD = 'email' # username 필드를 username으로 설정 // 20.10.31 이전 버전 : email로 사용하겠다고 설정
    REQUIRED_FIELDS = ['username']

    # Custom User Model을 기본 유저 모델로 사용하기 위해서 구현해야 하는 부분
    def __str__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin
