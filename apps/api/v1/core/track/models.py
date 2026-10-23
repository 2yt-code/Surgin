from django.db import models


class Track(models.Model):
    # example
    name = models.CharField(max_length=125)