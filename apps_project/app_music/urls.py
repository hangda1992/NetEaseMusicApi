# -*- coding: utf-8 -*-
from django.conf.urls import url
from apps_project.app_music.views import (SearchMusic, Mp3Url, Lyr)

urlpatterns = [
    url(r'^search_music', SearchMusic.as_view(), name='search_music'),
    url(r'^mp3url', Mp3Url.as_view(), name='mp3url'),
    url(r'^lyr', Lyr.as_view(), name='lyr'),

]