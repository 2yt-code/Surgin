from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.api.v1.core.models import BaseModel


class Artist(BaseModel):
    class ArtistType(models.TextChoices):
        INDIVIDUAL = 'individual', _('Individual')
        GROUP = 'group', _('Group')

    name = models.CharField(
        _('name'),
        max_length=25
    )
    bio = models.TextField(
        _('bio'),
        max_length=300,
        null=True,
        blank=True
    )
    avatar = models.ImageField(
        _('avatar'),
        upload_to='artists_avatar/',
        null=True,
        blank=True
    )
    cover = models.ImageField(
        _('cover'),
        upload_to='artists_cover/',
        null=True,
        blank=True
    )
    popularity = models.PositiveSmallIntegerField(
        _('popularity'),
        default=0
    )
    verified = models.BooleanField(
        _('verified'),
        default=False
    )
    slug = models.SlugField(
        _('slug'),
        max_length=120,
        unique=True
    )
    artist_type = models.CharField(
        _('artist type'),
        max_length=10,
        choices=ArtistType.choices,
        default=ArtistType.INDIVIDUAL
    )
    
    class Meta:
        verbose_name = _('artist')
        verbose_name_plural = _('artists')
        db_table = 'artist'

    def __str__(self):
        return f'{self.name}'

class ArtistMembership(BaseModel):
    class Role(models.TextChoices):
        OWNER = 'owner', _('Owner')
        MANAGER = 'manager', _('Manager')
        EDITOR = 'editor', _('Editor')

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=_('user'),
        on_delete=models.CASCADE,
        related_name='artist_memberships',
        related_query_name='artist_memberships',
    )
    artist = models.ForeignKey(
        Artist,
        verbose_name=_('artist'),
        on_delete=models.CASCADE,
        related_name='memberships',
        related_query_name='memberships'
    )
    role = models.CharField(
        _('role'),
        max_length=20,
        choices=Role.choices,
        default=Role.EDITOR
    )

    class Meta:
        verbose_name = _('artist membership')
        verbose_name_plural = _('artist memberships')
        db_table = 'artist_membership'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'artist'],
                name='unique_artist_membership'
            )
        ]

    def __str__(self):
        return f'{self.artist} - {self.user} - {self.role}'

class ArtistGroupMember(BaseModel):
    group = models.ForeignKey(
        Artist,
        verbose_name=_('group'),
        on_delete=models.CASCADE,
        related_name='group_members',
        related_query_name='group_members',
    )
    member = models.ForeignKey(
        Artist,
        verbose_name=_('member'),
        on_delete=models.CASCADE,
        related_name='group_memberships',
        related_query_name='group_memberships',
    )
    joined_at = models.DateField(
        _('joined'),
        null=True,
        blank=True
    )
    left_at = models.DateField(
        _('left'),
        null=True,
        blank=True
    )

    class Meta:
        verbose_name = _('artist group member')
        verbose_name_plural = _('artist group members')
        db_table = 'artist_group_member'
        constraints = [
            models.UniqueConstraint(
                fields=['group', 'member'],
                name='unique_artist_group_member'
            )
        ]

    def __str__(self):
        return f'{self.group} - {self.member}'

class ArtistFollow(BaseModel):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=_('user'),
        on_delete=models.CASCADE,
        related_name='following',
        related_query_name='following'
    )
    artist = models.ForeignKey(
        Artist,
        verbose_name=_('artist'),
        on_delete=models.CASCADE,
        related_name='followers',
        related_query_name='followers'
    )

    class Meta:
        verbose_name = _('artist follow')
        verbose_name_plural = _('artist follows')
        db_table = 'artist_follow'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'artist'],
                name='unique_artist_follow'
            )
        ]

    def __str__(self):
        return f'{self.user}'


class CreditRole(BaseModel):
    name = models.CharField(
        _('name'),
        max_length=100,
        unique=True
    )
    description = models.TextField(
        _('description'),
        blank=True
    )

    class Meta:
        verbose_name = _('credit role')
        verbose_name_plural = _('credit roles')
        db_table = 'credit_role'
        ordering = ['name']

    def __str__(self):
        return f'{self.name}'