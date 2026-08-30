import hmac
import hashlib
from django.conf import settings

import utils


def scheme_key(request):
    device_info = utils.device_info.get(
        request,
        request.META.get('HTTP_USER_AGENT')
    )

    user_agent = device_info.get('user_agent')
    browser = device_info.get('browser')
    platform = device_info.get('platform')
    device_type = device_info.get('device_type')
    key = create(f'{user_agent}:{browser}:{platform}:{device_type}')

    return key
    
def create(user_agent: str):
    return hmac.new(
        settings.SECRET_KEY.encode(),
        user_agent.encode(),
        hashlib.sha256
    ).hexdigest()

def compare(user_agent: str, review: str):
    fingerprint = hmac.new(
        settings.SECRET_KEY.encode(),
        user_agent.encode(),
        hashlib.sha256
    ).hexdigest()

    if hmac.compare_digest(fingerprint, review):
        return True
    else:
        return False