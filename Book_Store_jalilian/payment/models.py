from django.db import models

from django.utils import timezone
<<<<<<< HEAD
from django.utils.datetime_safe import datetime

from accounts.models import CustomUser, Address
from book.models import *
# from django.contrib.auth.models import User




class Discount(models.Model):
    """

    a base model for our other discount models
    """
    DISCOUNT_CHOICES = [('C', 'مقداری'), ('P', 'درصدی')]
    status = models.CharField(choices=DISCOUNT_CHOICES, default='C', max_length=5)
    cash_discount = models.IntegerField(verbose_name='مقدار تخفیف نقدی', blank=True, null=True)
    percent_discount = models.IntegerField(verbose_name='مقدار تخفیف درصدی', blank=True, null=True)
=======

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
>>>>>>> 440810b4aa0bc30c35a901515365524cbf32eca3
    validate_date = models.DateTimeField(verbose_name='تاریخ اعمال کد تخفیف', )
    expire_date = models.DateTimeField(verbose_name='تاریخ اعتبار کد تخفیف', )
    active = models.BooleanField('وضعیت تخفیف', default=False)

<<<<<<< HEAD
    class Meta:
        abstract = True
=======
    def _str_(self):
        return f'The deadline of discount  {self.id} is {self.expire_date}'
>>>>>>> 440810b4aa0bc30c35a901515365524cbf32eca3

    def active_status(self):
        if self.expire_date < timezone.now():
            self.active = False
            self.save()

    def discount_apply(self):
        if self.validate_date == timezone.now():
            self.active = True
            self.save()


<<<<<<< HEAD
class BasketDiscount(Discount):
    class Meta:
        verbose_name = 'تخفیف کددار'
        verbose_name_plural = 'تخفیف های کددار'

    code_discount = models.CharField(verbose_name='کد تخفیف', max_length=100, blank=True, null=True)

    def _str_(self):
        return f'The deadline of discount  {self.id} is {self.expire_date}'


class ProductDiscount(Discount):
    """
    discount in book
    """

=======
class ProductDiscount(models.Model):
    """
    discount in book
    """
>>>>>>> 440810b4aa0bc30c35a901515365524cbf32eca3
    class Meta:
        verbose_name = 'تخفیف نقدی'
        verbose_name_plural = 'تخفیف های نقدی'

<<<<<<< HEAD
    title = models.CharField('نام تخفیف نقدی', max_length=100, unique=True)
    max_purchase = models.DecimalField(verbose_name='سقف خرید', max_digits=10, decimal_places=4, blank=True, null=True)
    book = models.ForeignKey(Book, on_delete=models.CASCADE, verbose_name='کتاب')

    def _str_(self):
        return f'{self.title}'
=======
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
>>>>>>> 440810b4aa0bc30c35a901515365524cbf32eca3


class Invoice(models.Model):
    """
    a model for orders
    """
<<<<<<< HEAD

    class Meta:
        verbose_name = 'سفارش'
        verbose_name_plural = 'سفارش های  کاربران'

    customer = models.OneToOneField(CustomUser, verbose_name='مشتری',
                                on_delete=models.CASCADE, related_name='customer')
    address = models.ForeignKey(Address, verbose_name='ادرس', related_name='address',
                                on_delete=models.CASCADE )
    invoice_date = models.DateTimeField(verbose_name='زمان ایجاد سفارش', auto_now_add=True)
    discount_code = models.ForeignKey(BasketDiscount, on_delete=models.CASCADE, verbose_name='تخفیف کدی',
                                      max_length=100, blank=True, null=True)
    total_price = models.IntegerField(default=0, verbose_name='قیمت کل')
    total_discount = models.IntegerField(default=0, verbose_name='تخفیف کل')
    quantity = models.IntegerField(default=1)
    complete = models.BooleanField(default=False, verbose_name='تکمیل خرید')
    date = models.DateField(default=datetime.today)

    def __str__(self):
        return self.customer.last_name

    def placeOrder(self):
        self.save()

    @staticmethod
    def get_orders_by_customer(customer_id):
        return Invoice.objects.filter(customer=customer_id).order_by('-date')

    #
    # @property
    # def get_cart_total(self):
    #     orderitems = self.objects.all()
    #     total = sum([book.get_total for book in orderitems])
    #     return total
    # @property
    # def get_cart_items(self):
    #     orderitems = self.objects.all()
    #     total = sum([book.quantity for book in orderitems])
    #     return total
=======

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
>>>>>>> 440810b4aa0bc30c35a901515365524cbf32eca3

    # def get_total(self):
    #     total = 0
    #     for order_item in self.book.all():
    #         total += order_item.get_final_price()
    #     if self.discount_code:
    #         total -= self.discount_code.amount
    #     return total
    #

class InvoiceLine(models.Model):
    """
    a model for order detail
    """

    class Meta:
        verbose_name = 'ایتم سفارش'
        verbose_name_plural = 'ایتم های سفارش'

<<<<<<< HEAD
    invoice = models.ForeignKey(Invoice, on_delete=models.PROTECT, verbose_name='سبد خرید')
    book = models.ForeignKey(Book, on_delete=models.DO_NOTHING, verbose_name='محصول')
    quantity = models.IntegerField(verbose_name='تعداد', default=0)
=======
    invoice = models.ForeignKey(Invoice, on_delete=models.PROTECT,verbose_name='سبد خرید')
    book = models.ForeignKey(Book, on_delete=models.DO_NOTHING, verbose_name='محصول')
    # price = models.IntegerField(default=0,verbose_name='قیمت محصول')
    quantity = models.IntegerField(verbose_name='تعداد',default=0)
>>>>>>> 440810b4aa0bc30c35a901515365524cbf32eca3

    def __str__(self):
        return self.invoice.customer.last_name

<<<<<<< HEAD

    def get_total_item_price(self):
        total = self.book.price * self.quantity
        return total

    def get_total_discount_item_price(self):
        return self.quantity * self.book.discount_price

    def get_amount_saved(self):
        return self.get_total_item_price() - self.get_total_discount_item_price()

    def get_final_price(self):
        if self.book.discount_price:
            return self.get_total_discount_item_price()
        return self.get_total_item_price()
=======
    def book_price(self):
        return self.book.price

>>>>>>> 440810b4aa0bc30c35a901515365524cbf32eca3
