from django.contrib import admin
from django.urls import path, include
from ProjectApp import views
from FileApp import views
from NodeApp import views
from UserApp import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('MainApp.urls')),
    path('project/', include('ProjectApp.urls')),
    path('file/',include('FileApp.urls')),
    path('node/', include('NodeApp.urls')),
    path('user/', include('UserApp.urls')),
]