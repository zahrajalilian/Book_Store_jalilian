from django.db import models


from accounts.models import CustomUser
"""
a model for orders = invoice
"""


class Invoice(models.Model):
    customer = models.ForeignKey(CustomUser, on_delete=models.DO_NOTHING, related_name='invoices')
    invoice_date = models.DateTimeField()
    billing_address = models.CharField(max_length=70, blank=True, null=True)
    billing_city = models.CharField(max_length=40, blank=True, null=True)
    billing_state = models.CharField(max_length=40, blank=True, null=True)
    billing_country = models.CharField(max_length=40, blank=True, null=True)
    billing_postal_code = models.CharField(max_length=10, blank=True, null=True)
    total = models.BigIntegerField()

    def __str__(self):
        return self.customer


"""
a model for order detail
"""


class InvoiceLine(models.Model):
    invoice = models.ForeignKey(Invoice, on_delete=models.PROTECT)
    book = models.ForeignKey('book.Book', on_delete=models.DO_NOTHING)
    unit_price = models.IntegerField()
    quantity = models.IntegerField()

    def __str__(self):
        return self.invoice
