"""
import here
"""
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser, Address

"""
here we register our models
"""

admin.site.register(Address)


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ['email', 'username', 'is_admin', 'is_staff', 'is_customer']
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('address', 'is_customer',)}),
    )


admin.site.register(CustomUser, CustomUserAdmin)
