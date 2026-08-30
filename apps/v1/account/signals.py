from django.utils import timezone
from device_tracker.models import Device
import utils

from apps.v1.account.models import FingerPrint


def check_fingerprint(request):
    try:
        device_info = utils.device_info.get(
            request,
            request.META.get('HTTP_USER_AGENT')
        )

        user_agent = device_info.get('user_agent')
        browser = device_info.get('browser')
        platform = device_info.get('platform')
        device_type = device_info.get('device_type')
        key = utils.fingerprint.create(f'{user_agent}:{browser}:{platform}:{device_type}')

        fingerprint = FingerPrint.objects.filter(key=key).first()
        if fingerprint:
            fingerprint.last_verified_at = timezone.now()
        else: raise

        device = Device.objects.get(pk=fingerprint.pk)
        if device:
            if request.META.get('REMOTE_ADDR') == device.ip_address or fingerprint.trust_score >=50: 
                fingerprint.trust_score += 1
            else: raise

            if not device.is_active: raise
            device.last_seen = timezone.now()
        else: raise

        fingerprint.save()
        device.save()

        return True
    except:
        return False