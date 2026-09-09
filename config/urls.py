from django.contrib import admin
from django.urls import path, include
from django.conf.urls.i18n import i18n_patterns
from drf_spectacular.views import (
    SpectacularAPIView, 
    SpectacularRedocView, 
    SpectacularSwaggerView
)


i18n_urls = [
    path('i18n/', include('django.conf.urls.i18n'))
]

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

urlpatterns = [] + i18n_urls + doc_patterns
urlpatterns += i18n_patterns(
    # v1
    path('api/v1/account/', include('apps.api.v1.account.urls')),
    path('api/v1/artist/', include('apps.api.v1.artist.urls')),
)
