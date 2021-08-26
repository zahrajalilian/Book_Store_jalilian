from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType

"""
codename='add/change/del/view' ==
name='description==can add / can delete'
content_type='which content this permission belongs to'
content_type==>get_for_model(model name)

"""
content_type = ContentType.objects.get_for_model()
permission = Permission.objects.create(codename='', name='', content_type='')
