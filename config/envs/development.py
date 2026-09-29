from .common import *
from django.utils.translation import gettext_lazy as _


# Base settings
INSTALLED_APPS = [
    'daphne',
    'drf_spectacular'
] + INSTALLED_APPS

# Documentation settings
SPECTACULAR_SETTINGS = {
    'TITLE': 'Surgin',
    'DESCRIPTION': _('A robust web-based music streaming'),
    'VERSION': '1.0.0',
    'SERVE_INCLUDE_SCHEMA': False,
}