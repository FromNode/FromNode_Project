from django.contrib import admin
from django.urls import path
from . import views

app_name = 'project'
urlpatterns = [
    path('project_list/', views.show_project_list, name="project_list"),
    path('project_detail/', views.show_project_detail, name="project_detail"),
    path('project_checkcode/',views.project_checkcode, name='project_checkcode'),
    path('project_create',views.project_create,name='project_create'),
    path('project_likeornot/<str:project_Code>',views.likeornot,name='project_likeornot'),

    # path('form_create_project/', views.form_create_project, name="form_create_project"),
    # path('create_project/', views.create_project, name="create_project"),
]
