from django.db import models
from django.contrib.auth.models import User

# add realtionship to Spotify music model so each user can have their own playlist
# user = models.ForeignKey(User, on_delete=models.CASCADE)


# Create your models here.

class Playlist(models.Model):
    name = models.CharField(max_length=1000)
    total_tracks = models.IntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class PlaylistTrack(models.Model):
    title = models.CharField(max_length=1000)
    artist = models.CharField(max_length=1000)
    playlist = models.ForeignKey(Playlist, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
    


