from django.db import models
from django.utils.translation import gettext_lazy as _

# from apps.api.v1.core.artist.models import Artist
# from apps.api.v1.core.album.models import Album

# TODO
class Song(models.Model):
    title = models.CharField(max_length=200)
    # artist = models.ForeignKey(
    #     Artist,
    #     on_delete=models.CASCADE,
    #     related_name="songs"
    # )
    # album = models.ForeignKey(
    #     Album,
    #     on_delete=models.SET_NULL,
    #     null=True,
    #     blank=True,
    #     related_name="songs"
    # )
    cover = models.ImageField(
        upload_to="song_covers/",
        null=True,
        blank=True
    )
    audio_file = models.FileField(
        upload_to="songs/%Y/%m/%d/"
    )
    release_date = models.DateTimeField(auto_now_add=True)
    genre = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    play_count = models.PositiveBigIntegerField(default=0)
    like_count = models.PositiveBigIntegerField(default=0)
    is_published = models.BooleanField(default=True)
    duration = models.DurationField()
    updated_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _("song")
        verbose_name_plural = _("songs")
        db_table = 'song'