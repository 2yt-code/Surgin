from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.conf import settings


class Membership(AbstractUser):
    first_name = models.CharField(
        _("first name"), 
        max_length=150,
        help_text=_("Required first name. 150 characters")
    )
    last_name = models.CharField(
        _("last name"), 
        max_length=150, 
        help_text=_("Required last name. 150 characters")
    )
    email = models.EmailField(
        _("email address"),
        max_length=254,
        help_text=_("Required email. 254 characters")
    )
    password = models.CharField(
        _("password"), 
        max_length=128,
        help_text=_("Required password. 128 characters")
    )
    premium = models.BooleanField(default=False)

    def __str__(self):
        return self.username

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
    ip_address = models.GenericIPAddressField(_('ip address'))
    device_name = models.CharField(_('device name'), max_length=255)
    is_active = models.BooleanField(_('active'), default=True)
    last_seen = models.DateTimeField(_('last seen'), default=timezone.now)
    created_at = models.DateTimeField(_('created'), auto_now_add=True)

class FingerPrint(models.Model):
    device = models.OneToOneField(
        Device,
        on_delete=models.CASCADE,
        verbose_name=_('device'),
        null=True,
        blank=True
    )
    key = models.CharField(
        _("fingerprint hash"),
        max_length=64,
        unique=True
    )
    created_at = models.DateTimeField(
        _("created"), 
        auto_now_add=True
    )
    trust_score = models.IntegerField(
        _("trust level"), 
        default=50
    )
    last_verified_at = models.DateTimeField(
        auto_now_add=True
    )
    class Meta:
        verbose_name = _("fingerprint")
        verbose_name_plural = _("fingerprints")