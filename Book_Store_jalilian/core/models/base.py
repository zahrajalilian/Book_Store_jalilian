from django.db import models
from django.utils.translation import ungettext_lazy as _
class BaseModel(models.Model):
    is_active = models.BooleanField(
        default=True,
        verbose_name=_("Active status"),
        db_index=True,
        help_text=_(
        "Designates whether this item should be treated as active. "
        "Unselected this instead of deleting."
        ),
    )
    # A timestamp representing when this object was created.
    created_time = models.DateTimeField(
        verbose_name=_("Creation On"), auto_now_add=True
    )
    # A timestamp reprensenting when this object was last updated.
    updated_time = models.DateTimeField(
        verbose_name=_("Modified On"), auto_now=True, db_index=True
    )
    objects = models.Manager()

    class Meta:
        abstract = True


#  this is a base model
# dont creat in db
# is commen in all models
#