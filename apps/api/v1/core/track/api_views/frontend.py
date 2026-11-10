import uuid
from django.utils.translation import gettext_lazy as _
from drf_spectacular.utils import extend_schema
from rest_framework.response import Response
from rest_framework import (
    views,
    status,
    exceptions
)

from apps.api.v1.account.services import check_id_format
from apps.api.v1.core.artist.permissions import IsArtistMembershipUser
from apps.api.v1.core.track.models import Genre, Track
from apps.api.v1.core.track.serializers.frontend import TrackSerializer
from apps.api.v1.core.track.services import create_track, get_track
from apps.api.v1.core.track.serializers import TrackByIDSerializer



@extend_schema(tags=['Track'])
class TrackView(views.APIView):
    permission_classes = (IsArtistMembershipUser,)

    def post(self, request):        
        serializer = TrackSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        create_track(data=serializer.validated_data)
        return Response(
            dict(
                detail=_('Track was successfully submitted and placed in the approval queue'),
                code='track_added_successful'
            ), status=status.HTTP_200_OK
        )

@extend_schema(tags=['Track'])
class TrackByIDView(views.APIView):
    def get(self, request, track_id):
        track_id = check_id_format(id=track_id)
        if not track_id:
            return Response(
                dict(
                    detail=_('The ID format is incorrect'), 
                    code='invalid_id_format'
                ), status=status.HTTP_400_BAD_REQUEST
            )
        
        track = get_track(track_id=track_id)
        if not track:
            raise exceptions.NotFound(
                detail=_('Track not found'),
                code='not_found'
            )   
        serializer = TrackByIDSerializer(instance=track)
        track.update(serializer.validated_data)
        return Response(track)