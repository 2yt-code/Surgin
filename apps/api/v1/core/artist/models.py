from django.db import models


class Artist(models.Model):
    # example
    name = models.CharField(max_length=125)

    def __str__(self) -> str:
        return f'{self.name}'