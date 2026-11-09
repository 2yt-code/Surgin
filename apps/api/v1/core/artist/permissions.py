from rest_framework import permissions

from apps.api.v1.core.artist.models import ArtistMembership


class IsArtistMembershipUser(permissions.BasePermission):
    def has_permission(self, request, view):
        artist_membership = ArtistMembership.objects.filter(user=request.user).exists()
        return bool(request.user and artist_membership)