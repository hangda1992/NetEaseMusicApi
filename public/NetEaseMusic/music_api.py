#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import json
import codecs
import requests
from base64 import b64encode
from Crypto.Cipher import AES

"""
Windows下Crypto模块的安装
1. pip install crypto
2. pip install pycrypto
3. 将crypto包对应的文件夹改成Crypto

Linux下Crypto模块的安装
1.pip install pycrypto
2.pip install pycryptodome
"""

# 加密需要的固定数据
pubKey = '010001'
nonce = '0CoJUm6Qyw8W8jud'
modulus = '00e0b509f6259df8642dbc35662901477df22677ec152b5ff68ace' \
          '615bb7b725152b3ab17a876aea8a5aa76d2e417629ec4ee341f56135' \
          'fccf695280104e0312ecbda92557c93870114af6c9d05c4f7f0c3685' \
          'b7a46bee255932575cce10b424d813cfe4875d3e82047b97ddef5274' \
          '1d546b8e289dc6935b3ece0462db0a22b8e7'

# url请求类型
url = {
    # 获取mp3播放地址
    'play': 'http://music.163.com/weapi/song/enhance/player/url?csrf_token=',
    # 获取搜索结果
    'search': 'http://music.163.com/weapi/cloudsearch/get/web?csrf_token=',
    # 获取歌词
    'lyr': "http://music.163.com/weapi/song/lyric?csrf_token=",
    # 获取mp3url地址
    "mp3_url": "https://music.163.com/weapi/song/enhance/player/url?csrf_token=",
}


class NetEaseCloudMusic(object):

    def __init__(self):
        """
        浏览器头文件定义
        """
        self.header = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 '
                          '(KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'
        }
        self.cookies = {'appver': '1.5.2'}
        self.session = requests.Session()

    def random_num(self, size):
        """
        生成随机数，用于加密
        :param size:
        :return:
        """
        return (''.join(map(lambda xx: (hex(ord(xx))[2:]), str(os.urandom(size)))))[0:16]

    def aes_encrypt(self, text, sec_key):
        """
        AES加密
        :param text:
        :param sec_key:
        :return:
        """
        cipher_text = None
        try:
            pad = 16 - len(text) % 16
            if isinstance(text, bytes):
                text = text.decode('utf-8')
            text = text + str(pad * chr(pad))
            cryptor_ob = AES.new(sec_key, 2, '0102030405060708')
            cipher_text = cryptor_ob.encrypt(text)
            cipher_text = b64encode(cipher_text)

        except Exception as error:
            print("fun:aes_encrypt={}".format(error))
        return cipher_text

    def rsa_encrypt(self, text, pub_key, modulus):
        """
        RSA加密
        :param text:
        :param pub_key:
        :param modulus:
        :return:
        """
        text = text[::-1]
        rs = int(codecs.encode(text.encode('utf-8'), 'hex_codec'), 16) ** int(pub_key, 16) % int(modulus, 16)
        return format(rs, 'x').zfill(256)

    def song_public_1(self, url, data):
        """
        公共方法，获取网易请求方法，核心代码
        :param data:
        :return:
        """
        play_dic = {}
        try:
            text = json.dumps(data)
            sec_key = "a8LWv2uAtXjzSfkQ"
            enc_text = self.aes_encrypt(self.aes_encrypt(text, nonce), sec_key)
            payload = {
                'params': enc_text,
                'encSecKey':
                    '2d48fd9fb8e58bc9c1f14a7bda1b8e49a3520a67a2300a1f73766'
                    'caee29f2411c5350bceb15ed196ca963d6a6d0b61f3734f0a0f'
                    '4a172ad853f16dd06018bc5ca8fb640eaa8decd1cd41f66e166'
                    'cea7a3023bd63960e656ec97751cfc7ce08d943928e9db9b354'
                    '00ff3d138bda1ab511a06fbee75585191cabe0e6e63f7350d6'
            }
            r = requests.post(url=url, headers=self.header, data=payload)
            r.raise_for_status()
            play_dic = json.loads(r.text)

        except Exception as error:
            print("fun:song_public_1={}".format(error))

        return play_dic

    def search(self, song_name, type=1, total='true', limit='10'):
        """
        搜索歌曲id与其他相关信息
        搜索单曲(1)，歌手(100)，专辑(10)，歌单(1000)，用户(1002) *(type)*
        :param s:歌名
        :param type:类型，默认为单曲搜索
        :param total:
        :param limit:搜索歌曲的数量
        :return:
        """
        try:
            play_dic = {}
            play_j = {
                's': song_name,
                'type': type,
                'offset': 0,
                'total': total,
                'limit': limit,
            }
            play_dic = self.song_public_1(url=url['search'], data=play_j)

        except Exception as error:
            print("fun:search={}".format(error))

        return play_dic

    def get_song_msg(self, song_info):
        """
        获取歌曲信息
        :param song_info:歌曲信息
        :return: 返回有用信息，包含：歌名、歌曲id、歌曲图片链接、播放时长
        """
        song_list = []
        song_dic = {}
        try:
            if 'result' in song_info:

                # 搜索到的全部信息长度，暂时不用
                song_count = song_info['result']['songCount']
                song_all = song_info['result']['songs']

                for song in song_all:
                    song_id = song['id']
                    song_name = song['name']
                    song_img = None
                    user_name = None
                    if "al" in song:
                        song_img = song['al']['picUrl']
                        al_name = song['al']['name']
                    if "ar" in song:
                        user_name = ' & '.join([i['name'] for i in song['ar']])

                    song_dic.update({
                        "song_name": song_name,
                        "id": song_id,
                        "img": song_img,
                        "author": user_name,
                        "al_name": al_name
                    })
                    song_list.append(song_dic)
                    song_dic = {}

        except Exception as error:
            print("fun:get_song_msg={}".format(error))

        return song_list

    def ready_song_lyr(self, song_id):
        """
        获取歌曲歌词信息
        :param song_id:
        :return:
        """
        song_lyr_list = []
        try:
            url = "http://music.163.com/api/song/lyric?os=pc&id={song_id}&lv=-1&kv=-1&tv=-1".format(song_id=song_id)
            r = requests.get(url=url, timeout=3)
            song_lyr = json.loads(r.text)

            if "lrc" in song_lyr:
                song_lyrs = song_lyr['lrc']['lyric'].split('\n')
                for lyr in song_lyrs:
                    lyr_split = lyr.split(']')
                    lyr_msg = lyr_split[-1].strip()
                    lyr_time_str = lyr_split[0][1:]
                    lyr_time_str = lyr_time_str.split(":")
                    lyr_time = int(lyr_time_str[0]) * 60 + float(lyr_time_str[1])
                    song_lyr_list.append({
                        "msg": lyr_msg,
                        "time": lyr_time
                    })

        except Exception as error:
            print("fun:ready_song_lyr:{}".format(error))

        return song_lyr_list

    def get_song_mp3url(self, song_id):
        """
        获取歌曲mp3 url地址
        :return:
        """
        mp3_url = None
        try:
            play_j = {
                "br": 128000,
                "csrf_token": "",
                "ids": "[{song_id}]".format(song_id=song_id)
            }
            play_dic = self.song_public_1(url=url['mp3_url'], data=play_j)
            if "data" in play_dic:
                mp3_url = play_dic['data'][0]['url']

        except Exception as error:
            print("fun:search={}".format(error))

        return mp3_url
