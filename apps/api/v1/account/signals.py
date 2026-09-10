from django.utils import timezone
from rest_framework.request import Request
from rest_framework.response import Response

from apps.api.v1.account.models import Device, FingerPrint
import utils


ACCESS_TOKEN_MAX_AGE = 20 * 60
REFRESH_TOKEN_MAX_AGE = 7 * 24 * 60 * 60

def get_user_agent(request: Request):
    return request.META.get('HTTP_USER_AGENT', '')

def get_uuid(request: Request):
    return request.COOKIES.get('device_uuid')

def get_refresh_token(request: Request):
    return request.COOKIES.get('refresh_token')

def get_access_token(request: Request):
    return request.COOKIES.get('access_token')

def clear_auth_cookie(response: Response):
    response.delete_cookie('access_token')
    response.delete_cookie('refresh_token')
    response.delete_cookie('device_uuid')

def get_client_ip(request: Request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0].strip()
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def set_access_token(response: Response, access_token: str):
    response.set_cookie(
        key='access_token',
        value=str(access_token),
        max_age=ACCESS_TOKEN_MAX_AGE,
        httponly=False,
        samesite='Lax',
        path='/',
    )

def set_auth_cookies(
        response: Response, 
        access_token: str, 
        refresh_token: str, 
        device: Device
):
    response.set_cookie(
        key='access_token',
        value=str(access_token),
        max_age=ACCESS_TOKEN_MAX_AGE,
        httponly=False,
        samesite='Lax',
        path='/',
    )
    response.set_cookie(
        key='refresh_token',
        value=str(refresh_token),
        max_age=REFRESH_TOKEN_MAX_AGE,
        httponly=True,
        samesite='Lax',
        path='/',
    )
    response.set_cookie(
        key='device_uuid',
        value=str(device.uuid),
        httponly=True,
        secure=True,
        samesite='Lax',
        path='/',
    )

def login_account(request: Request, *args, **kwargs):
    try:
        uuid = kwargs.get('uuid')
        key = utils.fingerprint.scheme_key(request)
        fingerprint_model = FingerPrint.objects.get(
            device__uuid=uuid,
            key=key
        )
    except FingerPrint.DoesNotExist:
        return False
    
    fingerprint_model.last_verified_at = timezone.now()

    device_model = fingerprint_model.device
    device_model.last_seen = timezone.now()
    if not device_model.is_active: return False
    if not (
        get_client_ip(request) == device_model.ip_address or 
        fingerprint_model.trust_score >=50
    ): return False

    try:
        user = kwargs.get('user')
        user.last_login = timezone.now()
        user.save()
    except: 
        return False
        
    fingerprint_model.save(update_fields=["last_verified_at"])
    device_model.save()

    return True

def check_fingerprint(request: Request, *args, **kwargs):
    try:
        uuid = kwargs.get('uuid')
        key = utils.fingerprint.scheme_key(request)
        fingerprint_model = FingerPrint.objects.get(
            device__uuid=uuid,
            key=key
        )
    except FingerPrint.DoesNotExist:
        return False
    
    fingerprint_model.last_verified_at = timezone.now()

    device_model = fingerprint_model.device
    device_model.last_seen = timezone.now()
    if (
        get_client_ip(request) == device_model.ip_address or 
        fingerprint_model.trust_score >=50
    ): fingerprint_model.trust_score += 1
    if not device_model.is_active: return False

    fingerprint_model.save(update_fields=["last_verified_at"])
    device_model.save(update_fields=["last_seen"])

    return True