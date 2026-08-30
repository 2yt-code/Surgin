from django.utils import timezone
from device_tracker.models import Device
import utils

from apps.v1.account.models import FingerPrint


def check_fingerprint(request):
    try:
        key = utils.fingerprint.scheme_key(request)
        
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