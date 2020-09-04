from django.contrib import admin
from django.urls import path
from . import views
urlpatterns = [
    path('project/', views.show_project_detail, name="project_detail"),
    # 프로젝트 번호를 추후에 부여해야함
    path('upload/', views.show_upload, name="upload"),
]
