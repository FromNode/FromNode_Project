from django.contrib import admin
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('version_all/', views.version_all, name="version_all"),
    path('node_detail/', views.node_detail, name="node_detail"),
    path('upload/', views.Upload, name="upload"),
]
if settings.DEBUG :
    urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)