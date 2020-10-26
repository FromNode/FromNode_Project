from django.contrib import admin
from django.urls import path
from . import views
urlpatterns = [
    path('version_all/', views.version_all, name="version_all"),
    path('node_detail/', views.node_detail, name="node_detail"),
]