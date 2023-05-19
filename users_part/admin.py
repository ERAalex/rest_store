from django.contrib import admin

from .models import UserAccount, ContactUser


@admin.register(UserAccount)
class UserAccountAdmin(admin.ModelAdmin):
    list_display = ['email', 'name', 'is_active', 'is_staff']

@admin.register(ContactUser)
class ContactUserAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'city', 'street']

