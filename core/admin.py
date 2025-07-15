from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

# manaague user via admin panel change later please
admin.site.register(User, UserAdmin)