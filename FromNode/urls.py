from django.contrib import admin
from django.urls import path, include
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('MainApp.urls')),
    path('node/', include('NodeApp.urls')),
    path('project/', include('ProjectApp.urls')),
    path('user/', include('UserApp.urls')),
]