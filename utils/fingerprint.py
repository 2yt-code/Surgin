import hmac
import hashlib
from django.conf import settings

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