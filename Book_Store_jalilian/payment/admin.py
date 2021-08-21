"""
here we register our invoice and invoiceline
"""

from django.contrib import admin

# Register your models here.
from .models import Invoice,InvoiceLine,BasketDiscount,ProductDiscount



admin.site.register(InvoiceLine)
admin.site.register(BasketDiscount)
admin.site.register(ProductDiscount)

@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ['id','invoice_date','complete']

