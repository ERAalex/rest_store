from django.contrib import admin

from .models import UserAccount


@admin.register(UserAccount)
class UserAccountAdmin(admin.ModelAdmin):
    list_display = ['email', 'name', 'is_active', 'is_staff']

