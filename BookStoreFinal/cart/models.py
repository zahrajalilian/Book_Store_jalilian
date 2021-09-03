from django.db import models

# Create your models here.
from django.db import models

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
                                        on_delete=models.SET_NULL, related_name='customer', null=True, blank=True)
        # address = models.ForeignKey(Address, verbose_name='ادرس', related_name='address',
        #                             on_delete=models.CASCADE)
        product = models.ForeignKey(Book,on_delete=models.CASCADE,verbose_name='محصول')
        quantity = models.PositiveIntegerField(default=1)
        complete = models.BooleanField(default=False, verbose_name='تکمیل خرید')

        def __str__(self):
            if self.customer.username:
                name = self.customer
            else:
                name = self.customer.device
            return str(name)



class CartForm(ModelForm):
    """
    a form for out django
    showing quantity to our users in book detail
    """
    class Meta:
        model = Cart
        fields = ['quantity']