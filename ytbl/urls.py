from django.urls import path
import ytbl.views

app_name = 'ytbl'

urlpatterns = [
    path('', ytbl.views.showMap, name='showMap'),
]