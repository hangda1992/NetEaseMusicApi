# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from public.log import logger
from django.http import JsonResponse
from django.views.generic import View
from public.NetEaseMusic.music_api import NetEaseCloudMusic
from .serializers import SearchSongSerializer, MusicMp3Serializer


class SearchMusic(View):
    """搜索歌曲"""

    def get(self, request):

        result = {
            "status": 1,
            "msg": None,
            "data": {
                "song_info": []
            }
        }
        try:
            data = request.GET.dict()
            serializer = SearchSongSerializer(data=data)
            if serializer.is_valid():
                page = request.GET.get('page')
                keyword = request.GET.get('keyword')
                song_ob = NetEaseCloudMusic()
                song_all_info = song_ob.search(song_name=keyword, limit=page)
                result['data']['song_info'] = song_ob.get_song_msg(song_all_info)
                result['status'] = 0
                result['msg'] = "搜索成功"
            else:
                result['status'] = 1
                result['msg'] = serializer.errors

        except Exception as error:
            logger.error("SearchMusic:{error}".format(error=error))

        return JsonResponse(result)


class MusicMp3(View):
    """获取MP3链接"""

    def get(self, request):
        result = {
            "status": 1,
            "msg": None,
            "data": None
        }
        try:
            data = request.GET.dict()
            serializer = MusicMp3Serializer(data=data)
            if serializer.is_valid():
                song_id = request.GET.get('song_id')
                song_ob = NetEaseCloudMusic()
                result['data'] = song_ob.get_song_mp3url(song_id=song_id)
                result['msg'] = "获取成功"
            else:
                result['status'] = 1
                result['msg'] = serializer.errors
        except Exception as error:
            print(error)

        return JsonResponse(result)
