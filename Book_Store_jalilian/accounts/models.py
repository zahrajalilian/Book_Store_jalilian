from django.contrib.auth.base_user import BaseUserManager
from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.
from django_countries.fields import CountryField
# Create your models here.


class MyUserManager(BaseUserManager):
    def create_user(self, email, username, password=None):
        """
        Creates and saves a User with the given email, username
         and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            username=username,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_staff(self, email, username, password=None):
        """
        Creates and saves a staff with the given email, username
        and password.
        """
        user = self.create_user(
            email,
            password=password,
            username=username,
        )
        user.is_admin = False
        user.is_staff = True
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password=None):

            """
            Creates and saves a superuser with the given email, username
             and password.
            """
            user = self.create_user(
                email,
                password=password,
                username=username,
            )
            user.is_admin = True
            user.is_staff = True
            user.save(using=self._db)
            return user









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
    username = models.CharField(max_length=200,unique=True)
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    email = models.EmailField(unique=True)
    gender = models.CharField(verbose_name='gender', choices=GENDER_CHOICES, default='U', max_length=1)
    company = models.CharField(max_length=200,null=True,blank=True)
    address = models.ManyToManyField(Address)
    phone = models.IntegerField(null=True, blank=True)
    fax = models.IntegerField(null=True, blank=True)
    # objects = MyUserManager()

    def __str__(self):
        return f'{self.first_name} {self.last_name}'


class CustomerProxy(CustomUser):
    class Meta:
        proxy = True


class StaffProxy(CustomUser):
    class Meta:
        proxy = True
        # permissions=['']

class AdminProxy(CustomUser):
    class Meta:
        proxy = True



