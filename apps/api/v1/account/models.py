from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from django_countries.fields import CountryField

from apps.api.v1.core.artist.models import Artist
from apps.api.v1.core.playlist.models import Playlist
from apps.api.v1.core.track.models import Track


class Membership(AbstractUser):
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
        help_text=_('Required email. 254 characters')
    )
    password = models.CharField(
        _('password'), 
        max_length=128,
        help_text=_('Required password. 128 characters'),
        null=True,
        blank=True
    )
    # playlists = models.ManyToManyField(
    #     Playlist,
    #     verbose_name=_('playlists'),
    #     related_name='preferences',
    # )
    language = CountryField(
        help_text=_('Required language. Select your country')
    ) 
    premium = models.BooleanField(default=False)
    following = None
    followers = None

    class Meta:
        verbose_name = _('membership')
        verbose_name_plural = _('memberships')
        db_table = 'membership'

class Device(models.Model):
    uuid = models.CharField(
        _('uuid'),
        max_length=32,
        unique=True
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE,
        verbose_name=_('user')
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
    created_at = models.DateTimeField(
        _('created'), 
        auto_now_add=True
    )
    ip_address = models.GenericIPAddressField(_('ip address'))

    class Meta:
        verbose_name = _('device')
        verbose_name_plural = _('devices')
        db_table = 'device'

class FingerPrint(models.Model):
    device = models.OneToOneField(
        Device,
        on_delete=models.CASCADE,
        verbose_name=_('device'),
        null=True,
        blank=True
    )
    key = models.CharField(
        _('fingerprint hash'),
        max_length=64,
        unique=True
    )
    created_at = models.DateTimeField(
        _('created'), 
        auto_now_add=True
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

class UserPreferences(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name=('user'),    
    )
    artists_favorite = models.ManyToManyField(
        Artist,
        verbose_name=_('artists favorite'),
        related_name='preferences',
    )
    tracks_favorite = models.ManyToManyField(
        Track,
        verbose_name=_('tracks favorite'),
        related_name='preferences',
    )
    # genre_favorite = models.JSONField(
    #     _('genre favorite'),
    #     max_length=50,
    #     null=True,
    #     blank=True
    # )

    class Meta:
        verbose_name = _('preference')
        verbose_name_plural = _('preferences')
        db_table = 'user_preferences'
