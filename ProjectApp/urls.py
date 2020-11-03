from django.contrib import admin
from django.urls import path
from . import views 
urlpatterns = [
    path('project_list/', views.show_project_list, name="project_list"),
    path('form_create_project/', views.form_create_project, name="form_create_project"),
    path('create_project/', views.create_project, name="create_project"),
    # path('logout/', views.logout, name="logout"),
]
