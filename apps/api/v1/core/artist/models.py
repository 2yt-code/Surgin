from django.db import models

from apps.api.v1.core.models import BaseModel


class Artist(BaseModel):
    # example
    name = models.CharField(max_length=125)

    def __str__(self) -> str:
        return f'{self.name}'