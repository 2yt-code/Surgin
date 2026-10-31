from django.conf import settings
from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

from apps.api.v1.core.album.models import Album
from apps.api.v1.core.artist.models import Artist
from apps.api.v1.core.models import BaseModel


class Track(BaseModel):
    title = models.CharField(
        _('title'),
        max_length=200,
        db_index=True 
    )
    artist = models.ForeignKey(
        Artist, 
        verbose_name=_('artist'),
        related_name='artist',
        related_query_name='artist',
        on_delete=models.CASCADE,
        db_index=True
    )
    cover = models.ImageField(
        _('cover'),
        upload_to='track_covers/',
        null=True,
        blank=True
    )
    audio_file = models.FileField(
        _('audio file'),
        upload_to='tracks/%Y/%m/%d/'
    )
    album = models.ForeignKey(
        Album,
        verbose_name=_('album'),
        related_name='album',
        related_query_name='album',
        on_delete=models.SET_NULL,
        db_index=True,
        null=True,
        blank=True
    )
    genre = models.CharField(
        _('genre'),
        max_length=100,
        db_index=True
    )
    description = models.TextField(
        _('description'),
        blank=True,
        null=True
    )
    play_count = models.PositiveBigIntegerField(
        _('play count'),
        default=0,
        db_index=True
    )
    is_published = models.BooleanField(
        _('published'),
        default=True
    )
    is_explicit = models.BooleanField(
        _('explicit'),
        default=False
    )
    duration = models.DurationField(
        _('duration'),
        db_index=True
    )

    class Meta:
        verbose_name = _('track')
        verbose_name_plural = _('track')
        db_table = 'track'

class TrackPreference(BaseModel):
    track = models.OneToOneField(
        Track,
        verbose_name=_('track'),
        related_name='track',
        related_query_name='track',
        on_delete=models.CASCADE
    )
    users_liked = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        verbose_name=_('users liked'),
        related_name='users_liked',
        related_query_name='users_liked',
        blank=True
    )
    users_disliked = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        verbose_name=_('users disliked'),
        related_name='users_disliked',
        related_query_name='users_disliked',
        blank=True
    )
    users_playlist_added = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        verbose_name=_('users playlist added'),
        related_name='users_playlist_added',
        related_query_name='users_playlist_added',
        blank=True
    )

    class Meta:
        verbose_name = _('track preference')
        verbose_name_plural = _('tracks preference')
        db_table = 'track_preference'