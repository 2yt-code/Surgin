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