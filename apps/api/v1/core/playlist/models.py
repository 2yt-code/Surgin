from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.api.v1.core.album.models import Album
from apps.api.v1.core.models import BaseModel
from apps.api.v1.core.track.models import Track


class Playlist(BaseModel):
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name=_('owner'),
        related_name='owned_playlists',
        related_query_name='owned_playlists'
    )
    collaborators = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        verbose_name=_('collaborators'),
        related_name='collaborative_playlists',
        related_query_name='collaborative_playlists',
        blank=True
    )
    name = models.CharField(
        _('name'),
        max_length=50, 
        unique=True
    )
    description = models.TextField(
        _('description'),
        max_length=300,
        null=True,
        blank=True
    )
    baner = models.ImageField(
        _('baner'),
        upload_to='playlists_baner/',
        null=True,
        blank=True
    )
    is_public = models.BooleanField(
        _('private'),
        default=False
    )
    tracks = models.ManyToManyField(
        Track,
        verbose_name=_('tracks'),
        related_name='user_playlist_tracks',
        related_query_name='playlist_tracks',
        blank=True
    )
    albums = models.ManyToManyField(
        Album,
        verbose_name=_('albums'),
        related_name='user_playlist_tracks',
        related_query_name='playlist_albums',
        blank=True
    )

    class Meta:
        verbose_name = _('playlist')
        verbose_name_plural = _('playlist')
        db_table = 'playlist'

    def __str__(self):
        return f'{self.name} - {self.owner}'

class PlaylistFolder(BaseModel):
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name=_('owner'),
        related_name='owned_playlist_folders',
        related_query_name='owned_playlist_folders'
    )
    name = models.CharField(
        _('name'),
        max_length=50, 
        unique=True
    )
    description = models.TextField(
        _('description'),
        max_length=300,
        null=True,
        blank=True
    )
    baner = models.ImageField(
        _('baner'),
        upload_to='folders_baner/',
        null=True,
        blank=True
    )
    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        verbose_name=_('parent'),
        related_name='subfolders',
        related_query_name='subfolders',
        null=True,
        blank=True
    )
    playlists = models.ManyToManyField(
        Playlist,
        verbose_name=_('playlists'),
        related_name='folders',
        related_query_name='folders',
        blank=True
    )

    class Meta:
        verbose_name = _('playlist folder')
        verbose_name_plural = _('playlist folders')
        db_table = 'playlist_folder'

    def __str__(self):
        return f'{self.name} - {self.owner}'