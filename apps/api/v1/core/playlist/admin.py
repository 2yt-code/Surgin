from django.contrib import admin

from apps.api.v1.core.playlist.models import Playlist, PlaylistFolder


admin.site.register(Playlist)
admin.site.register(PlaylistFolder)