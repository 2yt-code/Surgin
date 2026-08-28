from django.utils import timezone
from device_tracker.utils import get_client_ip
from device_tracker.models import Device


def track_device(request, user, refresh_token=None):
    ip = get_client_ip(request)
    user_agent = request.META.get('HTTP_USER_AGENT', '')[:255]
    jti = refresh_token.get('jti') if refresh_token else None

    device = Device.objects.create(
        user=user,
        ip_address=ip,
        device_name=user_agent,
        refresh_token_jti=jti,
        last_seen=timezone.now(),
        is_active=True
    )
    
    return device