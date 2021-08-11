"""
here we register our invoice and invoiceline
"""

from django.contrib import admin

# Register your models here.
from .models import Invoice,InvoiceLine


admin.site.register(Invoice)
admin.site.register(InvoiceLine)

