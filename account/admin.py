from django.contrib import admin
from .models import *
from django.contrib.auth.admin import UserAdmin


@admin.register(ShopUser)
class ShopUserAdmin(admin.ModelAdmin):
    ordering = ['phone']
    list_display = ['phone', 'first_name', 'last_name', 'is_staff', 'is_active']
    fieldsets = UserAdmin.fieldsets + (
        ('None', {'fields': ('address',)}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('None', {'fields': ('address',)}),
    )

