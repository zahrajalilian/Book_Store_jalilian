# Generated by Django 3.2.6 on 2021-09-02 16:11

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0011_auto_20210902_2009'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='address',
            name='user',
        ),
        migrations.AddField(
            model_name='address',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]