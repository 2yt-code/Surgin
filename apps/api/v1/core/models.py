from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
import uuid


class BaseModel(models.Model):
    id = models.UUIDField(
        primary_key=True,
        editable=False,
        default=uuid.uuid4
    )
    updated = models.DateTimeField(
        _('updated'),
        auto_now=True,
        null=True,
        blank=True
    )
    created = models.DateTimeField(
        _('created'),
        default=timezone.now,
        editable=False
    )

    class Meta:
        abstract = True