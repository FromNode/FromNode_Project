from django.contrib import admin
from django.urls import path
from . import views

app_name="file"
urlpatterns = [
    path('file_list/<int:project_id>', views.show_file_list, name="file_list"),
    # path('form_create_new_file/', views.form_create_new_file, name="form_create_new_file"),
    path('create_new_file/', views.create_new_file, name="create_new_file"),
    path('create_invite_url/<int:project_id>', views.create_invite_url, name="invite"),
]
