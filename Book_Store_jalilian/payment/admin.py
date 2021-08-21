"""
here we register our invoice and invoiceline
"""

from django.contrib import admin

# Register your models here.
from .models import Invoice,InvoiceLine,BasketDiscount,ProductDiscount
<<<<<<< HEAD

=======
>>>>>>> 440810b4aa0bc30c35a901515365524cbf32eca3


admin.site.register(InvoiceLine)
admin.site.register(BasketDiscount)
admin.site.register(ProductDiscount)
<<<<<<< HEAD

@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ['id','invoice_date','complete']
=======
>>>>>>> 440810b4aa0bc30c35a901515365524cbf32eca3

