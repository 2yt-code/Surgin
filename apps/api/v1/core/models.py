from django.db import models

from apps.api.v1.core.artist.models import Artist


class Song(models.Model):
    title = models.CharField(max_length=200)
    artist = models.ForeignKey(
        Artist,
        on_delete=models.CASCADE,
        related_name="songs"
    )
    album = models.ForeignKey(
        #Album,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="songs"
    )
    cover = models.ImageField(
        upload_to="song_covers/",
        null=True,
        blank=True
    )
    audio_file = models.FileField(
        upload_to="songs/%Y/%m/%d/"
    )
    genre = models.CharField(
        max_length=100,
        blank=True
    )
    release_date = models.DateTimeField(auto_now_add=True)
    description = models.TextField(blank=True)
    play_count = models.PositiveBigIntegerField(default=0)
    like_count = models.PositiveBigIntegerField(default=0)
    is_published = models.BooleanField(default=True)
    duration = models.DurationField()
    updated_at = models.DateTimeField()