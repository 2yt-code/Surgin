from typing import Tuple, Optional
from rest_framework.request import Request
from rest_framework_simplejwt.authentication import JWTAuthentication, AuthUser
from rest_framework_simplejwt.tokens import Token

from apps.v1.account.signals import check_fingerprint

class CustomJWTAuthentication(JWTAuthentication):
    def authenticate(self, request: Request) -> Optional[Tuple[AuthUser, Token]]:
        header = self.get_header(request)
        if header is None:
            return None

        raw_token = self.get_raw_token(header)
        if raw_token is None:
            return None

        validated_token = self.get_validated_token(raw_token)

        fingerprint = check_fingerprint(request)
        if fingerprint:
            pass
        else: return None         

        return self.get_user(validated_token), validated_token
