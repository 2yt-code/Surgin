from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from django_countries.fields import CountryField

from apps.api.v1.core.artist.models import Artist
from apps.api.v1.core.models import BaseModel
from apps.api.v1.core.track.models import Genre, Track, TrackPreference


class Membership(BaseModel, AbstractUser):
    first_name = models.CharField(
        _('first name'), 
        max_length=150,
        help_text=_('Required first name. 150 characters')
    )
    last_name = models.CharField(
        _('last name'), 
        max_length=150, 
        help_text=_('Required last name. 150 characters')
    )
    email = models.EmailField(
        _('email address'),
        max_length=254,
        help_text=_('Required email. 254 characters'),
        unique=True
    )
    password = models.CharField(
        _('password'), 
        max_length=128,
        help_text=_('Required password. 128 characters'),
        null=True,
        blank=True
    )
    liked_songs = models.ManyToManyField(
        TrackPreference,
        verbose_name=_('liked songs'),
        related_name='user_liked',
        related_query_name='user_liked',
        blank=True
    )
    language = CountryField(
        verbose_name=_('language'),
        help_text=_('Required language. Select your country'),
        blank=True
    )
    premium = models.BooleanField(
        _('premium'), 
        default=False
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    class Meta:
        verbose_name = _('membership')
        verbose_name_plural = _('memberships')
        db_table = 'membership'

    def __str__(self):
        return f'{self.username}'

class Device(BaseModel):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE,
        verbose_name=_('user'),
        db_index=True
    )
    device_name = models.CharField(
        _('device name'), 
        max_length=512
    )
    is_active = models.BooleanField(
        _('active'), 
        default=True
    )
    last_seen = models.DateTimeField(
        _('last seen'), 
        default=timezone.now
    )
    ip_address = models.GenericIPAddressField(
        _('ip address')
    )

    class Meta:
        verbose_name = _('device')
        verbose_name_plural = _('devices')
        db_table = 'device'

    def __str__(self):
        return f'{self.user} - {self.device_name}'

class FingerPrint(BaseModel):
    device = models.OneToOneField(
        Device,
        on_delete=models.CASCADE,
        verbose_name=_('device'),
        db_index=True,
    )
    key = models.CharField(
        _('fingerprint hash'),
        max_length=64,
        unique=True,
        db_index=True
    )
    trust_score = models.IntegerField(
        _('trust level'), 
        default=50
    )
    last_verified_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        verbose_name = _('fingerprint')
        verbose_name_plural = _('fingerprints')
        db_table = 'fingerprint'

    def __str__(self):
        return f'{self.device.user} - {self.device.device_name}'

class UserPreferences(BaseModel):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name=('user'),    
    )
    artists_favorite = models.ManyToManyField(
        Artist,
        verbose_name=_('artists favorite'),
        related_name='artist_lovers',
        related_query_name='artist_lovers',
        blank=True
    )
    tracks_favorite = models.ManyToManyField(
        Track,
        verbose_name=_('tracks favorite'),
        related_name='track_lovers',
        related_query_name='track_lovers',
        blank=True
    )
    genre_favorite = models.ManyToManyField(
        Genre,
        verbose_name=_('genre favorite'),
        related_name='user_genre_favorite',
        related_query_name='user_genre_favorite',
        blank=True
    )

    class Meta:
        verbose_name = _('user preference')
        verbose_name_plural = _('user preferences')
        db_table = 'user_preferences'

    def __str__(self):
        return f'{self.user}'