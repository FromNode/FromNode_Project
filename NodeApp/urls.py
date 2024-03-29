from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

from . import views

app_name = 'node'
urlpatterns = [
    # path('node_list/<int:file_Code>', views.CreateTree, name="node_list"),
    path('node_list/<str:proj_Code>', views.node_list, name="node_list"),
    path('node_detail/<str:node_Code>', views.node_detail, name="node_detail"),
    path('create_node/',views.create_node, name='create_node'),
    path('changeNodeInfo/', views.changeNodeInfo, name="changeNodeInfo"),
    path('download/<str:pk>',views.download_view,name='download'),
    path('node_comment_create/<node_Code>',
         views.node_comment_create, name="node_comment_create"),
    path('comment_mention/',views.mentionable_member_json, name='mentionable_member_json'),
    path('submit/', views.comment_submit, name="comment_submit"),
    path('load_comment/', views.load_comment, name="load_comment"),
    path('load_node_data/', views.load_node_data, name="load_node_data"),
    
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
