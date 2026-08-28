from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from device_tracker.models import Device


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

class FingerPrint(models.Model):
    device = models.OneToOneField(
        Device,
        verbose_name=_("device"),
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    key = models.CharField(
        _("fingerprint hash"),
        max_length=250
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