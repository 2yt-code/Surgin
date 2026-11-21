from django.contrib import admin

from apps.api.v1.core.track.models import (
    Genre, 
    Track, 
    TrackCredit, 
    TrackPreference, 
    TrackRelease
)


admin.site.register(Track)
admin.site.register(TrackPreference)
admin.site.register(TrackCredit)
admin.site.register(TrackRelease)
admin.site.register(Genre)