from typing import Tuple, Optional
from rest_framework.request import Request
from rest_framework_simplejwt.authentication import JWTAuthentication, AuthUser
from rest_framework_simplejwt.tokens import Token

from apps.api.v1.account.services import (
    check_fingerprint, 
    get_access_token, 
    get_device_id
)


class CustomJWTAuthentication(JWTAuthentication):
    def authenticate(self, request: Request) -> Optional[Tuple[AuthUser, Token]]:
        access_token = get_access_token(request)
        validated_token = self.get_validated_token(access_token)

        fingerprint = check_fingerprint(request, device_id=get_device_id(request))
        if not fingerprint:
            return None        

        return self.get_user(validated_token), validated_token
