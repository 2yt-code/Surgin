from django.utils import timezone
from django.db import transaction
from django.core.mail import send_mail
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _
from django_rest_passwordreset.signals import reset_password_token_created
from rest_framework.request import Request
from rest_framework.response import Response
import uuid

from apps.api.v1.account.models import Device, FingerPrint
from apps.api.v1.account.paginations import UserPagination
import utils


ACCESS_TOKEN_MAX_AGE = 20 * 60
REFRESH_TOKEN_MAX_AGE_DEVICE_UUID = 7 * 24 * 60 * 60

def get_user_agent(request: Request):
    return request.META.get('HTTP_USER_AGENT', '')

def get_device_id(request: Request):
    device_id = request.COOKIES.get('device_id')
    if device_id:
        return uuid.UUID(str(device_id))
    else: return None

def check_id_format(id: str):
    try:
        id = uuid.UUID(id)
    except: return None
    return id

def get_refresh_token(request: Request):
    return request.COOKIES.get('refresh_token')

def get_access_token(request: Request):
    return request.COOKIES.get('access_token')

def clear_auth_cookie(response: Response):
    response.delete_cookie('access_token')
    response.delete_cookie('refresh_token')
    response.delete_cookie('device_id')

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
        max_age=REFRESH_TOKEN_MAX_AGE_DEVICE_UUID,
        httponly=True,
        samesite='Lax',
        path='/',
    )
    response.set_cookie(
        key='device_id',
        value=str(device.pk),
        max_age=REFRESH_TOKEN_MAX_AGE_DEVICE_UUID,
        httponly=True,
        secure=True,
        samesite='Lax',
        path='/',
    )

@transaction.atomic
def login_account(request: Request, *args, **kwargs):
    try:
        device_id = kwargs.get('device_id')
        key = utils.fingerprint.scheme_key(request)
        fingerprint_model = FingerPrint.objects.get(
            device__pk=device_id,
            key=key
        )
    
        fingerprint_model.last_verified_at = timezone.now()

        device_model = fingerprint_model.device
        device_model.last_seen = timezone.now()
        if not device_model.is_active: raise
        if not (
            get_client_ip(request) == device_model.ip_address or 
            fingerprint_model.trust_score >=50
        ): raise
        fingerprint_model.trust_score += 1

        user = kwargs.get('user')
        user.last_login = timezone.now()
        user.save(update_fields=['last_login'])

        fingerprint_model.save(update_fields=[
            'last_verified_at',
            'trust_score'
        ])
        device_model.save(update_fields=['last_seen'])

        return True
    except:
        if fingerprint_model:
            fingerprint_model.trust_score -= 1
            fingerprint_model.save(update_fields=['trust_score'])
        return False

@transaction.atomic
def check_fingerprint(request: Request, *args, **kwargs):
    try:
        device_id = kwargs.get('device_id')
        key = utils.fingerprint.scheme_key(request)
        fingerprint_model = FingerPrint.objects.get(
            device__pk=device_id,
            key=key
        )    
        fingerprint_model.last_verified_at = timezone.now()

        device_model = fingerprint_model.device
        device_model.last_seen = timezone.now()
        if not device_model.is_active: raise
        if (
            get_client_ip(request) == device_model.ip_address or 
            fingerprint_model.trust_score >=50
        ): fingerprint_model.trust_score += 1

        fingerprint_model.save(update_fields=[
            'last_verified_at', 
            'trust_score'
        ])
        device_model.save(update_fields=['last_seen'])

        return True
    except:
        if fingerprint_model:
            fingerprint_model.trust_score -= 1
            fingerprint_model.save(update_fields=['trust_score'])
        return False

# TODO
@receiver(reset_password_token_created)
def password_reset_token_created(
    sender,
    instance,
    reset_password_token,
    *args,
    **kwargs,
):
    user = reset_password_token.user

    send_mail(
        subject=_('Reset Password'),
        message=_(f'Your token for reset password: {reset_password_token.key}'),
        from_email=None,
        recipient_list=[user.email],
    )

def create_paginator(
        queryset, 
        request: Request, 
        view
):
    paginator = UserPagination()
    page = paginator.paginate_queryset(
            queryset=queryset, 
            request=request, 
            view=view
        )
    return page
