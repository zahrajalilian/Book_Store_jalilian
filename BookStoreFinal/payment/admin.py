from django.contrib import admin

# Register your models here.
from django.contrib import admin

# Register your models here.

from .models import *


class ItemInLine(admin.TabularInline):
    model = ItemOrder
    readonly_fields = ['customer', 'product', 'quantity']


class OrderAdmin(admin.ModelAdmin):
    list_display = ['id','customer','email','l_name','address','paid','get_price']
    # inlines = [ItemInLine]

admin.site.register(Order,OrderAdmin)
admin.site.register(ItemOrder)
