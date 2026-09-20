from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
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
    path('api/v1/song/', include('apps.api.v1.core.song.urls')),
    path('api/v1/account/', include('apps.api.v1.account.urls')),
)

if settings.DEBUG:
    urlpatterns += static(
    settings.MEDIA_URL, 
    document_root=settings.MEDIA_ROOT
)
