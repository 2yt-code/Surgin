from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.api.v1.core.artist.models import Artist, CreditRole
from apps.api.v1.core.models import BaseModel
from apps.api.v1.core.track.models import Track


class Album(BaseModel):
    class AlbumType(models.TextChoices):
        ALBUM = 'album', _('Album')
        SINGLE = 'single', _('Single')
        COMPILATION = 'compilation', _('Compilation')

    name = models.CharField(
        _('name'),
        max_length=100
    )
    description = models.TextField(
        _('description'),
        max_length=300,
        null=True,
        blank=True
    )
    duration = models.DurationField(
        _('duration'),
        null=True,
        blank=True
    )
    cover = models.ImageField(
        _('cover'),
        upload_to='albums_cover/',
        null=True,
        blank=True
    )
    album_type = models.CharField(
        _('album type'),
        max_length=20,
        choices=AlbumType.choices,
        default=AlbumType.ALBUM
    )
    label = models.ForeignKey(
        'RecordLabel',
        on_delete=models.SET_NULL,
        related_name='albums',
        related_query_name='albums',
        null=True,
        blank=True
    ) 
    tracks = models.ManyToManyField(
        Track,
        verbose_name=_('tracks'),
        related_name='album',
        related_query_name='album',
    )   
    is_published = models.BooleanField(
        _('published'),
        default=True
    )

    class Meta:
        verbose_name = _('album')
        verbose_name_plural = _('albums')
        db_table = 'album'

    def __str__(self):
        return f'{self.name}'

class AlbumCredit(BaseModel):
    album = models.ForeignKey(
        Album,
        verbose_name=_('album'),
        on_delete=models.CASCADE,
        related_name='credits',
        related_query_name='credits'
    )
    artist = models.ForeignKey(
        Artist,
        verbose_name=_('artist'),
        on_delete=models.CASCADE,
        related_name='album_credits',
        related_query_name='album_credits'
    )
    role = models.ForeignKey(
        CreditRole,
        verbose_name=_('role'),
        on_delete=models.PROTECT,
        related_name='album_credits',
        related_query_name='album_credits'
    )

    class Meta:
        verbose_name = _('album credit')
        verbose_name_plural = _('album credits')
        db_table = 'album_credit'
        constraints = [
            models.UniqueConstraint(
                fields=['album', 'artist', 'role'],
                name='unique_album_credit'
            )
        ]

    def __str__(self):
        return f'{self.album} - {self.artist} - {self.role}'

class RecordLabel(models.Model):
    name = models.CharField(
        _('name'),
        max_length=255, 
        unique=True
    )

    class Meta:
        verbose_name = _('record label')
        verbose_name_plural = _('record labels')
        db_table = 'record_lable'
    
    def __str__(self):
        return f'{self.name}'
