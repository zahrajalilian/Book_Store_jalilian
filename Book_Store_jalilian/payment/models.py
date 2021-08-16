from django.db import models

from django.utils import timezone

from accounts.models import CustomUser
from book.models import *


class BasketDiscount(models.Model):

    class Meta:
        verbose_name = 'تخفیف کددار'
        verbose_name_plural = 'تخفیف های کددار'

    DISCOUNT_CHOICES = [('C', 'مقداری'), ('P', 'درصدی')]
    status = models.CharField(choices=DISCOUNT_CHOICES, default='C', max_length=5)
    percent_discount = models.IntegerField(verbose_name='مقدار تخفیف درصدی', blank=True, null=True)
    cash_discount = models.IntegerField(verbose_name='مقدار تخفیف نقدی', blank=True, null=True)
    code_discount = models.CharField(verbose_name='کد تخفیف', max_length=100, blank=True, null=True)
    validate_date = models.DateTimeField(verbose_name='تاریخ اعمال کد تخفیف', )
    expire_date = models.DateTimeField(verbose_name='تاریخ اعتبار کد تخفیف', )
    active = models.BooleanField('وضعیت تخفیف', default=False)

    def _str_(self):
        return f'The deadline of discount  {self.id} is {self.expire_date}'

    def active_status(self):
        if self.expire_date < timezone.now():
            self.active = False
            self.save()

    def discount_apply(self):
        if self.validate_date == timezone.now():
            self.active = True
            self.save()


class ProductDiscount(models.Model):
    """
    discount in book
    """
    class Meta:
        verbose_name = 'تخفیف نقدی'
        verbose_name_plural = 'تخفیف های نقدی'

    DISCOUNT_CHOICES = [('C', 'مقدار'), ('P', 'درصدی')]
    status = models.CharField(choices=DISCOUNT_CHOICES, default='C', max_length=4)
    title = models.CharField('نام تخفیف نقدی', max_length=100, unique=True)
    cash_discount = models.IntegerField(verbose_name='مقدار تخفیف نقدی',blank=True,null=True )
    percent_discount = models.IntegerField(verbose_name='مقدار تخفیف درصدی', blank=True,null=True)
    max_purchase = models.DecimalField(verbose_name='سقف خرید', max_digits=10, decimal_places=4,blank=True,null=True)
    validate_date = models.DateTimeField(verbose_name='تاریخ اعمال تخفیف', )
    expire_date = models.DateTimeField(verbose_name='تاریخ اعتبار تخفیف', )
    active = models.BooleanField('وضعیت تخفیف', default=False)
    book = models.ForeignKey(Book, on_delete=models.CASCADE,verbose_name='کتاب')

    def _str_(self):
        return f'{self.title}'

    def status_active(self):
        if self.expire_date < timezone.now():
            self.active = False
            self.save()

    def discount_apply(self):
        if self.validate_date == timezone.now():
            self.active = True
            self.save()


class Invoice(models.Model):
    """
    a model for orders
    """

    class Meta:
        verbose_name = 'سفارش'
        verbose_name_plural = 'سفارش های  کاربران'

    customer = models.ForeignKey(CustomUser, verbose_name='مشتری', related_name='invoices',
                                 on_delete=models.CASCADE, )
    invoice_date = models.DateTimeField(verbose_name='زمان ایجاد سفارش', auto_now_add=True)
    discount_code = models.ForeignKey(BasketDiscount, on_delete=models.CASCADE, verbose_name='تخفیف کدی',
                                      max_length=100, blank=True, null=True)
    total_price = models.IntegerField(default=0,verbose_name='قیمت کل')
    total_discount = models.IntegerField(default=0,verbose_name='تخفیف کل')

    def __str__(self):
        return self.customer.last_name


class InvoiceLine(models.Model):
    """
    a model for order detail
    """

    class Meta:
        verbose_name = 'ایتم سفارش'
        verbose_name_plural = 'ایتم های سفارش'

    invoice = models.ForeignKey(Invoice, on_delete=models.PROTECT,verbose_name='سبد خرید')
    book = models.ForeignKey(Book, on_delete=models.DO_NOTHING, verbose_name='محصول')
    # price = models.IntegerField(default=0,verbose_name='قیمت محصول')
    quantity = models.IntegerField(verbose_name='تعداد',default=0)

    def __str__(self):
        return self.invoice.customer.last_name

    def book_price(self):
        return self.book.price

