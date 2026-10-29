from django.db import models

from apps.api.v1.core.models import BaseModel
from apps.api.v1.core.track.models import Track


class Playlist(BaseModel):
    # example
    name = models.CharField(
        max_length=125, 
        unique=True
    )
    tracks = models.ManyToManyField(
        Track,
        related_name='track',
        blank=True
    )