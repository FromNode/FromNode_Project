from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
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
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root = settings.STATIC_ROOT)