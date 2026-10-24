from django.db import models
import uuid


class BaseModel(models.Model):
    id = models.UUIDField(
        primary_key=True,
        editable=False,
        default=uuid.uuid4()
    )

    class Meta:
        abstract = True