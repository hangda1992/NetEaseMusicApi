# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import re
import json
from public.log import logger
from django.http import JsonResponse
from django.views.generic import View
from apps_project.app_music import models
from public.NetEaseMusic.music_api import NetEaseCloudMusic
from .serializers import (SearchSongSerializer, Mp3UrlSerializer)


class SearchMusic(View):
    """搜索歌曲"""

    def get(self, request):
        result = {
            "status": 1,
            "msg": None,
            "song_info": []
        }
        try:
            data = request.GET.dict()
            serializer = SearchSongSerializer(data=data)
            if serializer.is_valid():
                page = request.GET.get('page')
                keyword = request.GET.get('keyword')
                song_ob = NetEaseCloudMusic()
                song_all_info = song_ob.search(song_name=keyword, limit=page)
                result['song_info'] = song_ob.get_song_msg(song_all_info)
                result['status'] = 0
                result['msg'] = "搜索成功"
            else:
                result['status'] = 1
                result['msg'] = serializer.errors

        except Exception as error:
            logger.error("SearchMusic:{error}".format(error=error))

        return JsonResponse(result)


class Mp3Url(View):
    """获取MP3_Url地址"""

    def get(self, request):

        result = {
            "status": 1,
            "msg": None,
            "mp3_url": None
        }
        try:
            data = request.GET.dict()
            serializer = Mp3UrlSerializer(data=data)
            if serializer.is_valid():
                song_id = request.GET.get('id')
                song_ob = NetEaseCloudMusic()
                result['mp3_url'] = song_ob.get_song_mp3url(song_id=song_id)
                result['status'] = 0
                result['msg'] = "搜索成功"
            else:
                result['status'] = 1
                result['msg'] = serializer.errors

        except Exception as error:
            logger.error("Mp3Url:{error}".format(error=error))

        return JsonResponse(result)


class Lyr(View):

    def get(self, request):

        result = {
            "status": 1,
            "msg": None,
            "lyr": None
        }
        try:
            data = request.GET.dict()
            serializer = Mp3UrlSerializer(data=data)
            if serializer.is_valid():
                song_id = request.GET.get('id')
                song_ob = NetEaseCloudMusic()
                result['lyr'] = song_ob.ready_song_lyr(song_id=song_id)
                result['status'] = 0
                result['msg'] = "搜索成功"
            else:
                result['status'] = 1
                result['msg'] = serializer.errors

        except Exception as error:
            logger.error("Lyr:{error}".format(error=error))

        return JsonResponse(result)