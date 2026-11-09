
import uuid
from apps.api.v1.core.track.models import (
    Genre,
    Track, 
    TrackCredit, 
    TrackPreference, 
    TrackRelease
)


def get_track(track_id: uuid.UUID):
    try:
        track = Track.objects.get(pk=track_id)
        track_release = TrackRelease.objects.get(track=track)
        if not track_release.status == 'published':
            raise

        track_preference = TrackPreference.objects.get(track=track)
        user_disliked = track_preference.users_disliked.count()
        user_liked = track_preference.user_liked.count()

        track_credit = TrackCredit.objects.filter(track=track)
        credit = list()
        for obj in track_credit:
            credit.append(
                dict(
                    artist=obj.artist.name,
                    role=obj.role.name
                )
            )

    except: return None
    return dict(
        disliked=user_disliked,
        liked=user_liked,
        credit=credit
    )

def release_track(track: Track):
    TrackRelease.objects.get_or_create(
        track=track,
        status='draft',
    )
    return True

def create_track(data: dict):
    track = Track.objects.get_or_create(
        title=data.get('title'),
        cover=data.get('cover'),
        audio_file=data.get('audio_file'),
        genres=Genre.objects.get(name=data.get('genres')), # TODO
        description=data.get('description'),
        duration=data.get('duration'),
    )
    TrackRelease.objects.get_or_create(
        track=track,
        status='draft',
    )
    return True