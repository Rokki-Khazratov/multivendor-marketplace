from django.contrib import admin

from apps.user.models import UserProfile
from .models import *

admin.site.register(UserProfile)