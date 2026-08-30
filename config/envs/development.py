from .common import *
from datetime import timedelta
from django.utils.translation import gettext_lazy as _

# Base Settings
INSTALLED_APPS = [
    'daphne',
    'drf_spectacular'
] + INSTALLED_APPS

# Database Settings
AUTH_USER_MODEL = 'account.Membership'

# internationalization Settings
LOCALE_PATHS = [
    BASE_DIR / 'locale'
]

LANGUAGES = [
    ('en', _('English')),
    ('fa', _('Persian'))
]

# Documentation Settings
SPECTACULAR_SETTINGS = {
    'TITLE': 'Surgin',
    'DESCRIPTION': _('A robust web-based music streaming'),
    'VERSION': '1.0.0',
    'SERVE_INCLUDE_SCHEMA': False,
}

# RestFramework Settings
REST_FRAMEWORK = {
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'apps.v1.account.auth.CustomJWTAuthentication',
    ],
    'DEFAULT_THROTTLE_RATES': {
        'user': '1/minute'
    }
}

# JWT Settings
SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=20),
    "REFRESH_TOKEN_LIFETIME": timedelta(weeks=1),
    
    "TOKEN_OBTAIN_SERIALIZER": "apps.v1.account.serializers.frontend.CustomTokenObtainPairSerializer",
    "TOKEN_REFRESH_SERIALIZER": "apps.v1.account.serializers.frontend.CustomTokenRefreshSerializer",
}