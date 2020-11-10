from django.contrib import admin
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
app_name = 'node'
urlpatterns = [
    path('version_all/<int:file_Code>', views.version_all, name="version_all"),
    path('node_detail/<str:node_Code>', views.node_detail, name="node_detail"),
    path('create_node/<str:node_Code>',views.create_node, name= 'create_node'),
    path('upload/', views.Upload, name="upload"),
]
if settings.DEBUG :
    urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)