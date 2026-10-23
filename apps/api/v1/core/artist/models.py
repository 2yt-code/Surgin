from django.db import models


class Artist(models.Model):
    # example
    name = models.CharField(max_length=125)