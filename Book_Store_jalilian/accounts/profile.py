from django.db import models
# from django.contrib.auth.models import User
from django.db.models.signals import post_save
# from django.core.signals import request_finished,
from .models import CustomUser
# Create your models here.
# from phone_field import PhoneField


class Profile(models.Model):
    user = models.OneToOneField(CustomUser,on_delete=models.CASCADE)   # برای نشان دادن پروفایل هر یوزر
    phone = models.IntegerField(max_length=15)
    address = models.CharField(max_length=300, null=True, blank=True)

    def str(self):
        return self.user.name

    def save_profile_user(sender,**kwargs):
        if kwargs['created']:
            profile_user = Profile(user=kwargs['instance'])
            profile_user.save()


    post_save.connect(save_profile_user,sender=CustomUser)