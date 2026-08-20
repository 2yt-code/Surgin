import hmac
import hashlib
from django.conf import settings

def create(value):
    return hmac.new(
        settings.SECRET_KEY.encode(),
        value.encode(),
        hashlib.sha256
    ).hexdigest()

def compare(value, db_value):
    fingerprint = hmac.new(
        settings.SECRET_KEY.encode(),
        value.encode(),
        hashlib.sha256
    ).hexdigest()

    if hmac.compare_digest(fingerprint, db_value):
        return True
    else:
        return False