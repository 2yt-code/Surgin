from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _


class Membership(AbstractUser):
    first_name = models.CharField(
        _("first name"), 
        max_length=150,
        help_text=_('Required first name. 150 characters')
    )
    last_name = models.CharField(
        _("last name"), 
        max_length=150, 
        help_text=_('Required last name. 150 characters')
    )
    email = models.EmailField(
        _("email address"), 
        help_text=_('Required email. 254 characters')
    )
    password = models.CharField(
        _("password"), 
        max_length=128,
        help_text=_('Required password. 128 characters')
    )
    premium = models.BooleanField(default=False)

    def __str__(self):
        return self.username

class FingerPrint(models.Model):
    ip_address = models.GenericIPAddressField(_("ip address"))
    user_agent = models.TextField(_("user agent"))
    created_at = models.DateTimeField(_("created"), auto_now_add=True)
    trust_level = models.IntegerField(_("trust level"), default=0)
    user_id = models.IntegerField()

    class Meta:
        verbose_name = _("fingerprint")
        verbose_name_plural = _("fingerprints")