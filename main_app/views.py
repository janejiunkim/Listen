from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.db import models
from django.contrib import admin
from .models import Playlist, PlaylistTrack
from django.contrib.auth.models import User
from spotipy.oauth2 import SpotifyClientCredentials
import sys

import spotipy
from spotipy.oauth2 import SpotifyOAuth

# Create your views here.
def index(request):
    return render(request, 'index.html')

def about(request):
    return render(request, 'about.html')

def login_view(request):
    # if post, then authenticate (user submitted username and password)
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            u = form.cleaned_data['username']
            p = form.cleaned_data['password']
            user = authenticate(username = u, password = p)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponseRedirect('/user/' +u)
                else:
                    print('The account has been disabled.')
            else:
                print('The username and/or password is incorrect')
    else:
        form = AuthenticationForm()
        return render(request, 'login.html', {'form': form})

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('connect', user_id=user.id)
        else:
            print('Invalid Form Submitted.')
            return redirect('/signup')
    else:
        form = UserCreationForm()
        return render(request, 'signup.html', {'form': form})
        

def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/')


def connect(request, user_id):
    def show_tracks(results):
        for i, item in enumerate(results['items']):
            track = item['track']
            t = PlaylistTrack(title=track['name'], artist=track['artists'][0]['name'],playlist = curr_playlist)
            t.save()
            print(
                "   %d %32.32s %s" %
                (i, track['artists'][0]['name'], track['name']))


       # if __name__ == '__main__':
    scope = 'playlist-read-private'
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))

    playlists = sp.current_user_playlists()
    spotify_id = sp.me()['id']

    current_user=User.objects.get(id = user_id)

    for playlist in playlists['items']:
        if playlist['owner']['id'] == spotify_id:
            print()
            print(playlist['name'])
            print('  total tracks', playlist['tracks']['total'])
            p = Playlist(name=playlist['name'], total_tracks=playlist['tracks']['total'], user=current_user)
            p.save()
            curr_playlist = Playlist.objects.get(id = p.id)
            results = sp.playlist(playlist['id'], fields="tracks,next")
            tracks = results['tracks']
            show_tracks(tracks)

            while tracks['next']:
                tracks = sp.next(tracks)
                show_tracks(tracks)
    return render(request, 'connect.html')

def match(request):
    matched =[]
    mySongs = PlaylistTrack.objects.filter(pk__lt = 1415)
    theirSongs = PlaylistTrack.objects.filter(pk__gt = 1415)
    
    for i in range(len(mySongs)):
        for j in range(len(theirSongs)):
            if mySongs[i].title == theirSongs[j].title and mySongs[i].artist == theirSongs[j].artist:
                if mySongs[i] in matched:
                    continue
                else:
                    matched.append(mySongs[i])
    
    print(matched)
    for i in range(len(matched)):
        print(matched[i].title, matched[i].artist, matched[i].id)
        


        
    return render(request, 'match.html', {'matched': matched})

def playlists(request):
    my_playlists = Playlist.objects.filter(user_id=1)
    other_playlists = Playlist.objects.filter(user_id=2)
    print(other_playlists)
    return render(request, 'playlists.html', {'my_playlists': my_playlists, 'other_playlists':other_playlists})

def match_failure(request):
    return render(request, 'match_failure.html')

def match_success(request):
    return render(request, 'match_success.html')

def profile(request):
    def show_tracks(results):
            for i, item in enumerate(results['items']):
                track = item['track']
                t = PlaylistTrack(title=track['name'], artist=track['artists'][0]['name'], playlist = curr_playlist)
                t.save()
                print(
                    "   %d %32.32s %s" %
                    (i, track['artists'][0]['name'], track['name']))
    # user = User.objects.get(username=username)
    # Gets all the public playlists for the given
# user. Uses Client Credentials flow
#

    client_credentials_manager = SpotifyClientCredentials()
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

    #user = 'mwnwwogj9wr671v66w98uorbo'
    spotify_user = '128787688'
    sp_user_obj = User.objects.get(id=2)

    if len(sys.argv) > 1:
        user = sys.argv[1]

    playlists = sp.user_playlists(spotify_user)

    while playlists:
        for i, playlist in enumerate(playlists['items']):
            print(
                "%4d %s %s" %
                (i +
                1 +
                playlists['offset'],
                playlist['uri'],
                playlist['name']))
        if playlists['next']:
            playlists = sp.next(playlists)
        #else:
            #playlists = None

        for playlist in playlists['items']:
            if playlist['owner']['id'] == spotify_user:
                print()
                print(playlist['name'])
                print('  total tracks', playlist['tracks']['total'])
                p = Playlist(name=playlist['name'], total_tracks=playlist['tracks']['total'], user=sp_user_obj)
                p.save()
                curr_playlist = p
                results = sp.playlist(playlist['id'], fields="tracks,next")
                #print(results['tracks'])
                tracks = results['tracks']
                show_tracks(tracks)

                while tracks['next']:
                    tracks = sp.next(tracks)
                    show_tracks(tracks)
        

        return HttpResponseRedirect('/')
