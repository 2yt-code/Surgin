from django.utils import timezone

from apps.v1.account.models import FingerPrint
import utils


ACCESS_TOKEN_MAX_AGE = 20 * 60
REFRESH_TOKEN_MAX_AGE = 7 * 24 * 60 * 60

def get_user_agent(request):
    return request.META.get('HTTP_USER_AGENT', '')

def get_uuid(request):
    return request.COOKIES.get('device_uuid')

def get_refresh_token(request):
    return request.COOKIES.get('refresh_token')

def get_access_token(request):
    return request.COOKIES.get('access_token')

def clear_auth_cookie(response):
    response.delete_cookie('access_token')
    response.delete_cookie('refresh_token')
    response.delete_cookie('device_uuid')

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0].strip()
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def set_access_token(response, access_token):
    response.set_cookie(
        key='access_token',
        value=str(access_token),
        max_age=ACCESS_TOKEN_MAX_AGE,
        httponly=False,
        samesite='Lax',
        path='/',
    )

def set_auth_cookies(response, access_token, refresh_token, device):
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
        key="device_uuid",
        value=str(device.uuid),
        httponly=True,
        secure=True,
        samesite="Lax",
        path="/",
    )

def login_account(request, *args, **kwargs):
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

    fingerprint_model.save(update_fields=["last_verified_at"])
    device_model.save()

    return True

def check_fingerprint(request, *args, **kwargs):
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