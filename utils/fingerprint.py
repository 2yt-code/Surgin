import hmac
import hashlib
from django.conf import settings

from apps.v1.account.models import FingerPrint
import utils


def scheme_key(request):
    device_info = utils.device.get_device_info(
        request,
        request.META.get('HTTP_USER_AGENT')
    )

    user_agent = device_info.get('user_agent')
    browser = device_info.get('browser')
    platform = device_info.get('platform')
    device_type = device_info.get('device_type')
    key = create_hash(f'{user_agent}:{browser}:{platform}:{device_type}')

    return key
    
def create_hash(user_agent: str):
    return hmac.new(
        settings.SECRET_KEY.encode(),
        user_agent.encode(),
        hashlib.sha256
    ).hexdigest()

def compare_hash(user_agent: str, review: str):
    fingerprint = hmac.new(
        settings.SECRET_KEY.encode(),
        user_agent.encode(),
        hashlib.sha256
    ).hexdigest()

    if hmac.compare_digest(fingerprint, review):
        return True
    else:
        return False