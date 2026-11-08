from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.api.v1.core.artist.models import Artist, CreditRole
from apps.api.v1.core.models import BaseModel


class Track(BaseModel):
    title = models.CharField(
        _('title'),
        max_length=200,
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
    genres = models.ManyToManyField(
        'Genre',
        verbose_name=_('genres'),
        related_name='tracks',
        related_query_name='tracks',
        blank=True
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
        db_index=True,
        # null=True,
        # blank=True,
    )
    slug = models.SlugField(
        _('slug'),
        max_length=120,
        unique=True
    )

    class Meta:
        verbose_name = _('track')
        verbose_name_plural = _('tracks')
        db_table = 'track'

    def __str__(self):
        return f'{self.title}'

class TrackPreference(BaseModel):
    track = models.OneToOneField(
        Track,
        verbose_name=_('track'),
        on_delete=models.CASCADE,
        related_name='track',
        related_query_name='track'
    )
    users_disliked = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        verbose_name=_('users disliked'),
        related_name='users_disliked',
        related_query_name='users_disliked',
        blank=True
    )

    class Meta:
        verbose_name = _('track preference')
        verbose_name_plural = _('tracks preferences')
        db_table = 'track_preference'

    def __str__(self):
        return f'{self.track}'

class TrackCredit(BaseModel):
    track = models.ForeignKey(
        Track,
        verbose_name=_('track'),
        on_delete=models.CASCADE,
        related_name='credits',
        related_query_name='credits'
    )
    artist = models.ForeignKey(
        Artist,
        verbose_name=_('artist'),
        on_delete=models.PROTECT,
        related_name='track_credits',
        related_query_name='track_credits'
    )
    role = models.ForeignKey(
        CreditRole,
        verbose_name=_('role'),
        on_delete=models.PROTECT,
        related_name='track_credits',
        related_query_name='track_credits'
    )
    credited_as = models.DateField(
        _('credited')
    )

    class Meta:
        verbose_name = _('track credit')
        verbose_name_plural = _('track credits')
        db_table = 'track_credit'
        constraints = [
            models.UniqueConstraint(
                fields=['track', 'artist', 'role'],
                name='unique_track_artist_role'
            )
        ]

    def __str__(self):
        return f'{self.artist} - {self.track}'
    
class TrackRelease(BaseModel):
    class Status(models.TextChoices):
        DRAFT = 'draft', _('draft')
        SCHEDULED = 'scheduled', _('scheduled')
        PUBLISHED = 'published', _('published')
        TAKEN_DOWN = 'taken_down', _('taken down')

    track = models.OneToOneField(
        Track,
        verbose_name=_('track'),
        on_delete=models.CASCADE,
        related_name='release',
        related_query_name='release'
    )
    status = models.CharField(
        _('status'),
        max_length=20,
        choices=Status.choices,
        default=Status.DRAFT
    )
    release_date = models.DateTimeField(
        _('release date'),
        null=True,
        blank=True
    )
    
    class Meta:
        verbose_name = _('track release')
        verbose_name_plural = _('track releases')
        db_table = 'track_release'
        ordering = ['-created']

    def __str__(self):
        return f'{self.track.title} - {self.status}'

class Genre(BaseModel):
    name = models.CharField(
        _('name'),
        max_length=100,
        unique=True
    )
    slug = models.SlugField(
        _('slug'),
        max_length=120,
        unique=True
    )
    description = models.TextField(
        _('description'),
        max_length=500,
        blank=True
    )
    baner = models.ImageField(
        _('baner'),
        upload_to='genres_baner/',
        blank=True,
        null=True
    )
    parent = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        related_name='subgenres',
        blank=True,
        null=True
    )
    is_active = models.BooleanField(
        _('is active'),
        default=True
    )

    class Meta:
        verbose_name = _('genre')
        verbose_name_plural = _('genres')
        db_table = 'genre'

    def __str__(self):
        return f'{self.name}'