from django.db import models

from apps.api.v1.core.models import BaseModel


class Track(BaseModel):
    # example
    name = models.CharField(max_length=125)