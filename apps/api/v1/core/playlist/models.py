from django.db import models


class Playlist(models.Model):
    # example
    name = models.CharField(max_length=125)