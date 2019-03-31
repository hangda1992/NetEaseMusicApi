# -*- coding: utf-8 -*-
from django.conf.urls import url
from apps_project.app_music.views import SearchMusic, MusicMp3

urlpatterns = [
    url(r'^search_music', SearchMusic.as_view(), name='search_music'),
    url(r'^music_mp3', MusicMp3.as_view(), name='music_mp3'),

]