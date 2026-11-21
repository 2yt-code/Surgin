from django.contrib import admin

from apps.api.v1.core.album.models import (
    Album, 
    AlbumCredit, 
    RecordLabel
)


admin.site.register(Album)
admin.site.register(AlbumCredit)
admin.site.register(RecordLabel)