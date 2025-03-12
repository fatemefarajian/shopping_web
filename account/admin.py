from django.contrib import admin
from .models import *
from django.contrib.auth.admin import UserAdmin
from .forms import ShopUserCreationForm, ShopUserChangeForm


@admin.register(ShopUser)
class ShopUserAdmin(UserAdmin):
    ordering = ['phone']

    add_form = ShopUserCreationForm
    form = ShopUserChangeForm
    model = ShopUser

    list_display = ['phone', 'first_name', 'last_name', 'is_active', 'is_staff']

    fieldsets = (
        (None, {'fields': ('phone', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name', 'address')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important Dates', {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (None, {'fields': ('phone', 'password1', 'password2')}),
        ('Personal Info', {'fields': ('first_name', 'last_name', 'address')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important Dates', {'fields': ('last_login', 'date_joined')}),
    )
