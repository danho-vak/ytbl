from django.urls import path
import account.views

app_name = 'account'

urlpatterns = [
    path('signUp/', account.views.signUp, name='signUp'),
    path('signIn/', account.views.signIn, name='signIn'),
    path('logOut/', account.views.logOut, name='logOut'),
    path('profile/', account.views.profile, name='profile'),
    path('password/', account.views.changePassword, name='password'),
    path('withdrawal/', account.views.userDelete, name='userDelete')
]