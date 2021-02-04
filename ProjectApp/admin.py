from django.contrib import admin
from .models import Projects, proj_with_user

admin.site.register(Projects)
admin.site.register(proj_with_user)