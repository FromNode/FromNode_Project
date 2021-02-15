from django.contrib import admin
from .models import Profile

# Register your models here.
class ProfileAdmin(admin.ModelAdmin):
    list_display=(
        'user',
        'nickname',
        'profile_image',
        'user_color'
    )

admin.site.register(Profile,ProfileAdmin)