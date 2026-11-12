from django.contrib.auth import get_user_model
from rest_framework_simplejwt.token_blacklist.models import OutstandingToken, BlacklistedToken

from apps.api.v1.account.models import Device, FingerPrint
from apps.api.v1.core.artist.models import Artist, ArtistFollow
from apps.api.v1.core.playlist.models import Playlist


User = get_user_model()

def get_device(**kwargs):
    device = Device.objects.filter(**kwargs).first()
    return device

def create_user(**kwargs):
    try:
        obj = User.objects.create(**kwargs)
    except: return None
    return obj

def create_fingerprint(**kwargs):
    try:
        obj = FingerPrint.objects.create(**kwargs)
    except: return None
    return obj

def create_device(**kwargs):
    try:
        obj = Device.objects.create(**kwargs)
    except: return None
    return obj

def get_outstanding_token(**kwargs):
    obj = OutstandingToken.objects.filter(**kwargs)
    return obj

def get_or_create_blacklisted_token(**kwargs):
    obj = BlacklistedToken.objects.get_or_create(**kwargs)
    return obj

def get_fingerprint(**kwargs):
    obj = FingerPrint.objects.filter(**kwargs).first()
    return obj

def get_device(**kwargs):
    obj = Device.objects.filter(**kwargs).first()
    return obj

def get_user_all():
    obj = User.objects.all()
    return obj

def get_or_create_artist_follow(**kwargs):
    obj = ArtistFollow.objects.get_or_create(**kwargs)
    return obj

def create_playlist(**kwargs):
    try:
        obj = Playlist.objects.create(**kwargs)
    except: return None
    return obj

def get_artist(**kwargs):
    obj = Artist.objects.filter(**kwargs).first()
    return obj

def get_artist_follow(**kwargs):
    obj = ArtistFollow.objects.filter(**kwargs).first()
    return obj

def get_playlist(**kwargs):
    obj = Playlist.objects.filter(**kwargs).first()
    return obj