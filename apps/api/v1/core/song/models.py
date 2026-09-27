from django.db import models
from django.utils.translation import gettext_lazy as _
from uuid import uuid4

# from apps.api.v1.core.artist.models import Artist
# from apps.api.v1.core.album.models import Album

class SongQuerySet(models.QuerySet):
    def published(self):
        return self.filter(is_published=True)

    def latest(self, limit=50):
        return self.published().order_by('-release_date')[:limit]

    def most_liked(self, limit=50):
        return self.published().order_by('-like_count')[:limit]

    def most_played(self, limit=50):
        return self.published().order_by('-play_count')[:limit]

    def popular(self, limit=50):
        return self.published().order_by(
            '-like_count',
            '-play_count'
        )[:limit]

# TODO
class Song(models.Model):
    uuid = models.CharField(
        _('uuid'),
        max_length=32,
        unique=True,
        default=uuid4().hex
    )
    cover = models.ImageField(
        _('cover'),
        upload_to='song_covers/',
        null=True,
        blank=True
    )
    audio_file = models.FileField(
        _('audio file'),
        upload_to='songs/%Y/%m/%d/'
    )
    title = models.CharField(
        _('title'),
        max_length=200
    )
    release_date = models.DateTimeField(
        _('release date'),
        auto_now_add=True
    )
    genre = models.CharField(
        _('genre'),
        max_length=100
    )
    description = models.TextField(
        _('description'),
        blank=True
    )
    play_count = models.PositiveBigIntegerField(
        _('play count'),
        default=0
    )
    like_count = models.PositiveBigIntegerField(
        _('like count'),
        default=0
    )
    is_published = models.BooleanField(
        _('is published'),
        default=True
    )
    updated_at = models.DateTimeField(
        _('updated at'),
        auto_now_add=True
    )
    duration = models.DurationField(_('duration'))
    objects = SongQuerySet.as_manager()

    class Meta:
        verbose_name = _('song')
        verbose_name_plural = _('songs')
        db_table = 'song'