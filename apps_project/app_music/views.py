# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import re
import json
from public.log import logger
from django.http import JsonResponse
from django.views.generic import View
from apps_project.app_music import models
from .serializers import SearchSongSerializer
from public.NetEaseMusic.music_api import NetEaseCloudMusic


class SearchMusic(View):

    def get(self, request):

        try:
            result = {
                "status": 1,
                "msg": None,
                "song_info": []
            }
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
