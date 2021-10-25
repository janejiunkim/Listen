from django.urls import path
from . import views
from .models import Playlist, PlaylistTrack
from django.db import models

urlpatterns = [
        path('', views.index, name='index'),
        path('about/', views.about, name='about'),
        path('connect/<int:user_id>', views.connect, name='connect'),
        path('profile/', views.profile, name='profile'),
        path('login/', views.login_view, name="login"),
        path('logout/', views.logout_view, name="logout"),
        path('signup/', views.signup, name='signup'),
        path('match/', views.match, name='match'),
        path('playlists/', views.playlists, name="playlists")

]