from django.contrib import admin
from django.urls import path
from . import views
urlpatterns = [
    path('project_list/', views.show_project_list, name="show_project"),
    path('create_project/', views.create_project, name="create_project")
]
