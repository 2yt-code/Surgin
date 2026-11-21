from django.contrib import admin
from apps.api.v1.core.artist.models import (
    Artist, 
    ArtistFollow, 
    ArtistGroupMember, 
    ArtistMembership, 
    CreditRole
)


admin.site.register(Artist)
admin.site.register(ArtistMembership)
admin.site.register(ArtistGroupMember)
admin.site.register(ArtistFollow)
admin.site.register(CreditRole)