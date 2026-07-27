from rest_framework import generics, status
from rest_framework.response import Response

from apps.v1.artist.serializers import RegisterArtistAccountSerializers
from apps.v1.artist.models import Artist

class RegisterArtistAccountView(generics.CreateAPIView):
    queryset = Artist.objects.all()
    serializer_class = RegisterArtistAccountSerializers

    def post(self, request):
        serializer = RegisterArtistAccountSerializers(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(
                {'success'},
                status=status.HTTP_201_CREATED
            )
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )