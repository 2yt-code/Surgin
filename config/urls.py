from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from django.conf.urls.i18n import i18n_patterns


i18n_urls = [
    path('i18n/', include('django.conf.urls.i18n'))
]

version_1 = i18n_patterns(
    path('api/v1/', include('apps.api.v1.core.urls')),
    path('api/v1/song/', include('apps.api.v1.core.song.urls')),
    path('api/v1/account/', include('apps.api.v1.account.urls')),
)

urlpatterns = [] + i18n_urls + version_1

if settings.DEBUG:
    urlpatterns += static(
    settings.MEDIA_URL, 
    document_root=settings.MEDIA_ROOT
)
