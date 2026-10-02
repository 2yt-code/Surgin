from config.envs.common import DEVELOPMENT_MODE

if not DEVELOPMENT_MODE:
    urlpatterns = []

if DEVELOPMENT_MODE:
    from django.urls import path
    from drf_spectacular.views import (
        SpectacularAPIView, 
        SpectacularRedocView, 
        SpectacularSwaggerView
    )

    doc_patterns = [
        path('schema/', SpectacularAPIView.as_view(), name='schema'),
        path(
            'schema/swagger-ui/', 
            SpectacularSwaggerView.as_view(
                url_name='schema', 
            ), name='swagger-ui'
        ),
        path(
            'schema/redoc/', 
            SpectacularRedocView.as_view(
                url_name='schema', 
            ), name='redoc'
        ),
    ]

    urlpatterns = [] + doc_patterns