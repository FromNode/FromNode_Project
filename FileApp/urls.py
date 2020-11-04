from django.contrib import admin
from django.urls import path
from . import views

app_name="file"
urlpatterns = [
    # 프로젝트 번호를 추후에 부여해야함
    path('upload/', views.show_upload, name="upload"),
    path('form_create_new_file/', views.form_create_new_file, name="form_create_new_file"),
    path('create_new_file/', views.create_new_file, name="create_new_file"),
]
