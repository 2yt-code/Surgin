from typing import Tuple, Optional
from rest_framework.request import Request
from rest_framework_simplejwt.authentication import JWTAuthentication, AuthUser
from rest_framework_simplejwt.tokens import Token

from apps.v1.account.signals import (
    check_fingerprint, 
    get_access_token, 
    get_uuid
)


class CustomJWTAuthentication(JWTAuthentication):
    def authenticate(self, request: Request) -> Optional[Tuple[AuthUser, Token]]:
        access_token = get_access_token(request)
        validated_token = self.get_validated_token(access_token)

        fingerprint = check_fingerprint(request, uuid=get_uuid(request))
        if not fingerprint:
            return None        

        return self.get_user(validated_token), validated_token
