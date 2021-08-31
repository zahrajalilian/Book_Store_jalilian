# from django.db import models
#
# # Create your models here.
# from django.contrib.auth.base_user import BaseUserManager
# from django.db import models
# from django.contrib.auth.models import AbstractUser
# # Create your models here.
# from django_countries.fields import CountryField
# # Create your models here.
# from accounts.manager import CustomUserManager
#
#
# class Address(models.Model):
#     """
#        a model with many to many relationship with CustomUser
#        """
#
#     street = models.CharField(max_length=200)
#     street_2 = models.CharField(max_length=200, blank=True, null=True)
#     city = models.CharField(max_length=200)
#     state = models.CharField(max_length=200)
#     postal_code = models.CharField(max_length=100)
#     country = CountryField()
#
#     def __str__(self):
#         return f' {self.country},{self.state},{self.city}, {self.street} '
# #
#
#
# """
# our customed user model
#
# here we have 3 kind of user:
# customer
# staff
# admin
# """
#
#
# class CustomUser(AbstractUser):
#     EMAIL_FIELD = 'email'
#     USERNAME_FIELD = 'username'
#     REQUIRED_FIELDS = ['email']
#
#     company = models.CharField(max_length=200,null=True,blank=True)
#     address = models.ManyToManyField(Address)
#     phone = models.IntegerField(null=True, blank=True)
#     fax = models.IntegerField(null=True, blank=True)
#     device = models.CharField(max_length=200, null=True, blank=True)
#     objects = CustomUserManager()
#
#     def register(self):
#         self.save()
#
#     @staticmethod
#     def get_customer_by_email(email):
#         try:
#             return CustomUser.objects.get(email=email)
#         except:
#             return False
#
#     def isExists(self):
#         if CustomUser.objects.filter(email=self.email):
#             return True
#
#         return False
#
#     # def __str__(self):
#     #     return f'{self.first_name} {self.last_name}'
#
#     def __str__(self):
#         if self.username:
#             name = self.last_name + self.first_name
#         else:
#             name = self.device
#         return str(name)
#
#
# class CustomerProxy(CustomUser):
#     class Meta:
#         proxy = True
#
#
# class StaffProxy(CustomUser):
#     class Meta:
#         proxy = True
#
#
# class AdminProxy(CustomUser):
#     class Meta:
#         proxy = True
#
# ////////////////////////////////////////////////////////////////////
from django.db import models

# Create your models here.


from django.db import models

# Create your models here.
from django.contrib.auth.base_user import BaseUserManager
from django.db.models.signals import post_save
from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.
# from django_countries.fields import CountryField
# Create your models here.
# from accounts.manager import CustomUserManager
from accounts.manager import CustomUserManager


class Address(models.Model):
    """
       a model with many to many relationship with CustomUser
       """

    street = models.CharField(max_length=200)
    street_2 = models.CharField(max_length=200, blank=True, null=True)
    city = models.CharField(max_length=200)
    state = models.CharField(max_length=200)
    postal_code = models.CharField(max_length=100)
    # country = CountryField()

    def __str__(self):
        return f'{self.state},{self.city}, {self.street} '
#


"""
our customed user model 

here we have 3 kind of user:
customer
staff
admin
"""


class CustomUser(AbstractUser):
    # EMAIL_FIELD = 'email'
    # USERNAME_FIELD = 'email'
    # REQUIRED_FIELDS = ['username']
    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']
    email = models.EmailField(unique=True)
    device = models.CharField(max_length=200, null=True, blank=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    objects = CustomUserManager()

    def register(self):
        self.save()

    @staticmethod
    def get_customer_by_email(email):
        try:
            return CustomUser.objects.get(email=email)
        except:
            return False

    def isExists(self):
        if CustomUser.objects.filter(email=self.email):
            return True

        return False


    def __str__(self):
        if self.username:
            name = self.last_name + self.first_name
        else:
            name = self.device
        return str(name)


class CustomerProxy(CustomUser):
    class Meta:
        proxy = True
    is_staff = False
    is_superuser = False

class StaffProxy(CustomUser):
    class Meta:
        proxy = True
    is_staff = True
    is_superuser = False

class AdminProxy(CustomUser):
    class Meta:
        proxy           = True
    is_staff            = True
    is_superuser = True


class Profile(models.Model):
    user = models.OneToOneField(CustomUser,on_delete=models.CASCADE)
    company = models.CharField(max_length=200, null=True, blank=True)
    address = models.ForeignKey(Address, on_delete=models.DO_NOTHING, null=True, blank=True)
    phone = models.IntegerField(null=True, blank=True)
    fax = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.user.email


def save_profile_user(sender,**kwargs):
    if kwargs['created']:
        profile_user = Profile(user=kwargs['instance'])
        profile_user.save()


post_save.connect(save_profile_user,sender=CustomUser)
