# -*- coding: utf-8 -*-
from django.conf.urls import url
from apps_project.app_music.views import SearchMusic

urlpatterns = [
    url(r'^search_music', SearchMusic.as_view(), name='search_music'),

]