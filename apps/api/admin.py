from django.contrib import admin

from apps.user.models import UserProfile
from .models import *

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['id', 'user']


admin.site.register(UserProfile, UserProfileAdmin)