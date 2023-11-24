from django.contrib import admin
from .models import Category, Popup
from django.contrib.auth.admin import UserAdmin

admin.site.register(Category)
admin.site.register(Popup)