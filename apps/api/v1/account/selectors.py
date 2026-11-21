from django.contrib.auth import get_user_model
from rest_framework_simplejwt.token_blacklist.models import OutstandingToken, BlacklistedToken

from apps.api.v1.account.models import Device, FingerPrint
from apps.api.v1.core.album.models import Album
from apps.api.v1.core.artist.models import Artist, ArtistFollow
from apps.api.v1.core.playlist.models import Playlist
from apps.api.v1.core.track.models import TrackCredit


User = get_user_model()

def get_device(**kwargs):
    try:
        obj = Device.objects.get(**kwargs)
    except Device.DoesNotExist:
        return None
    return obj

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
    try:
        obj = OutstandingToken.objects.get(**kwargs)
    except OutstandingToken.DoesNotExist:
        return None
    return obj

def get_or_create_blacklisted_token(**kwargs):
    obj = BlacklistedToken.objects.get_or_create(**kwargs)
    return obj

def get_fingerprint(**kwargs):
    try:
        obj = FingerPrint.objects.get(**kwargs)
    except FingerPrint.DoesNotExist:
        return None
    return obj

def get_device(**kwargs):
    try:
        obj = Device.objects.get(**kwargs)
    except Device.DoesNotExist:
        return None
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
    try:
        obj = Artist.objects.get(**kwargs)
    except Artist.DoesNotExist:
        return None
    return obj

def get_artist_follow(**kwargs):
    try:
        obj = ArtistFollow.objects.get(**kwargs)
    except ArtistFollow.DoesNotExist:
        return None
    return obj

def get_playlist(**kwargs):
    try:
        obj = Playlist.objects.get(**kwargs)
    except Playlist.DoesNotExist:
        return None
    return obj

def get_user(**kwargs):
    try:
        obj = User.objects.get(**kwargs)
    except User.DoesNotExist:
        return None
    return obj

def get_track_credit_by_filter_method(**kwargs):
    obj = TrackCredit.objects.filter(**kwargs)
    return obj

def get_album_by_filter_method(**kwargs):
    obj = Album.objects.filter(**kwargs)
    return obj