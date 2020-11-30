from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from account.forms import UserChangeForm, UserCreationForm
from account.models import User

# Register your models here.
class UserAdmin(BaseUserAdmin):
    # 관리자 화면의 사용자 추가, 변경 폼을 account.forms에 있는 폼으로 설정
    form = UserChangeForm
    add_form = UserCreationForm
    readonly_fields = ('created_at',) # DateTimeField에 auto_now_add 옵션이 true일 경우 이렇게 설정해 줘야 출력 가능

    # 관리자 화면에서 어떻게 표현할 지 설정
    list_display = ('email', 'username', 'created_at', 'is_admin', 'is_active')
    list_filter = ('is_admin', 'is_active')
    fieldsets = (
        (None, {'fields':('email', 'username', 'password', 'created_at')}),
        ('Permissions', {'fields': ('is_admin', 'is_active')}),
    )

    add_fieldsets = (
        (None, {'classes':('wide',),
                'fields':('email', 'username', 'password1', 'password2')}
         ),
    )
    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ()


# 직접 생성한 Costum User Manager와 관리자 폼을 사용하도록 등록
admin.site.register(User, UserAdmin)
# 장고에서 기본적으로 제공하는 Group은 사용하지 않도록 설정
admin.site.unregister(Group)
