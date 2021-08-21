"""
import here
""
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .forms import CustomUserCreationForm, CustomUserChangeForm
# from .models import CustomUser,Address,
from .models import *

admin.site.register(Address)


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ['email', 'username','id']
    fieldsets = UserAdmin.fieldsets + (

    (None, {'fields': ('address',)}),
    )


admin.site.register(CustomUser, CustomUserAdmin)


@admin.register(CustomerProxy)
class CustomerAdmin(admin.ModelAdmin):
    def get_queryset(self, request):
        return CustomUser.objects.filter(is_staff=False,is_superuser=False)
    list_display = ['email','username']

@admin.register(StaffProxy)
class StaffAdmin(admin.ModelAdmin):
    def get_queryset(self, request):
        return CustomUser.objects.filter(is_staff=True,is_superuser=False)

    list_display = ['email', 'username']

@admin.register(AdminProxy)
class AdminAdmin(admin.ModelAdmin):
    def get_queryset(self, request):
        return CustomUser.objects.filter(is_staff=True,is_superuser=True)

    list_display = ['email', 'username']"

