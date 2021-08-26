

from django.contrib.auth.base_user import BaseUserManager

from django.db import models


from django.contrib.auth.base_user import BaseUserManager
from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

from django_countries.fields import CountryField
# Create your models here.







class Address(models.Model):
    """
       a model with many to many relationship with CustomUser
       """

    street = models.CharField(max_length=200)
    street_2 = models.CharField(max_length=200, blank=True, null=True)
    city = models.CharField(max_length=200)
    state = models.CharField(max_length=200)
    postal_code = models.CharField(max_length=100)
    country = CountryField()

    def __str__(self):
        return f' {self.country},{self.state},{self.city}, {self.street} '
#


"""
our customed user model 

here we have 3 kind of user:
customer
staff
admin
"""


class CustomUser(AbstractUser):



    GENDER_CHOICES = [('M', 'Male'), ('F', 'Female'), ('U', 'Unknown')]
    username = models.CharField(max_length=200)
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    email = models.EmailField(unique=True)
    gender = models.CharField(verbose_name='gender', choices=GENDER_CHOICES, default='U', max_length=1)
    company = models.CharField(max_length=200,null=True,blank=True)
    address = models.ManyToManyField(Address)
    phone = models.IntegerField(null=True, blank=True)
    fax = models.IntegerField(null=True, blank=True)

    # objects = MyUserManager()
    # USERNAME_FIELD = 'email'
    # REQUIRED_FIELDS = []


    def register(self):
        self.save()

    @staticmethod
    def get_customer_by_email(email):
        try:
            return CustomUser.objects.get(email=email)
        except:
            return False

    def isExists(self):
        if CustomUser.objects.filter(email = self.email):
            return True

        return False

    def __str__(self):
        return f'{self.first_name} {self.last_name}'


class CustomerProxy(CustomUser):
    class Meta:
        proxy = True


class StaffProxy(CustomUser):
    class Meta:
        proxy = True


class AdminProxy(CustomUser):
    class Meta:
        proxy = True

