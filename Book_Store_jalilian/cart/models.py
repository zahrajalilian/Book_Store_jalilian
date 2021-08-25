from django.db import models

# Create your models here.
f

from accounts.models import CustomUser,Address
from book.models import Book
# Create your models here.
from django.forms import ModelForm


class Cart(models.Model):

        """
       a model for cart
       customer == which user our cart belongs to
       product == which product in our cart
       quantity == how many of each product
       our status ==> complete or not
        """

        class Meta:
            verbose_name = 'سبد خرید'
            verbose_name_plural = 'سبد خرید'

        customer = models.ForeignKey(CustomUser, verbose_name='مشتری',
                                        on_delete=models.CASCADE, related_name='customer')
        # address = models.ForeignKey(Address, verbose_name='ادرس', related_name='address',
        #                             on_delete=models.CASCADE)
        product = models.ForeignKey(Book,on_delete=models.CASCADE,verbose_name='محصول')
        quantity = models.PositiveIntegerField(default=1)
        complete = models.BooleanField(default=False, verbose_name='تکمیل خرید')

        def __str__(self):
            return self.customer.last_name
        #
        # def placeOrder(self):
        #     self.save()
        #
        # @staticmethod
        # def get_orders_by_customer(customer_id):
        #     return Cart.objects.filter(customer=customer_id).order_by('-date')


class CartForm(ModelForm):
    """
    a form for out django
    showing quantity to our users in book detail
    """
    class Meta:
        model = Cart
        fields = ['quantity']