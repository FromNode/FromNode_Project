from django.contrib import admin
from django.urls import path
from . import views
app_name = 'user'
urlpatterns = [
    path('signup/',views.signup,name='signup'),
    path('login/',views.login,name='login'),
    path('mypage/',views.mypage,name='mypage'),
    path('logout/',views.logout,name='logout'),
]
