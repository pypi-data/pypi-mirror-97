#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :  qobuz.py
@Date    :  2021/02/26
@Author  :  Yaronzz
@Version :  1.0
@Contact :  yaronhuang@foxmail.com
@Desc    :  
'''
import hashlib
import os
import re
import uuid
import requests
import json
import base64
import aigpy
import time

from requests.packages import urllib3
from qobuzzz_dl.model import Album, Track, Artist, Playlist, StreamUrl
from qobuzzz_dl.enum import Type, AudioQuality


__URL_PRE__ = 'https://www.qobuz.com/api.json/0.2'
__APP_ID__ = "950096963"
__APP_SECRET__ = "979549437fcc4a3faad4867b5cd25dcb"
__APP_AUTHORIZATION = "Authorization:Basic WlRKbE9XTmhaR1V0TnpsbVpTMDBaR1UyTFRrd1lqTXRaRGsxT0RSbE1Ea3dPRE01Ok1UUmpaVFZqTTJFdE9HVmxaaTAwT1RVM0xXRm1Oamt0TlRsbE9ERmhObVl5TnpJNQ=="

# SSL Warnings
urllib3.disable_warnings()
# add retry number
requests.adapters.DEFAULT_RETRIES = 5


class LoginKey(object):
    def __init__(self):
        self.offer = ""
        self.user_auth_token = ""
        self.userid = 0
        self.countryCode = ""


class QobuzAPI(object):
    def __init__(self):
        self.key = LoginKey()
        self.__debugVar = 0

    # def __getToken__(self):
    #     aigpy.netHelper.downloadJson()

    def login(self, username, password):
        params = {
            'username': username,
            'email': username,
            'password': password,
            'extra': 'partner',
            'app_id': __APP_ID__,
        }

        result = requests.get(__URL_PRE__ + "/user/login", params=params).json()
        if 'status' in result and result['status'] != 200:
            return "Login failed!", False

        self.key.userid = result['user']["id"]
        self.key.countryCode = result['user']["country_code"]
        self.key.offer = result['user']["subscription"]["offer"]
        self.key.user_auth_token = result['user_auth_token']
        return None, True


    def __toJson__(self, string: str):
        try:
            json_object = json.loads(string)
        except:
            return None
        return json_object


    def __get__(self, path, params={}, retry=3, urlpre=__URL_PRE__):
        params['app_id'] = __APP_ID__
        params['user_auth_token'] = self.key.user_auth_token
        respond = requests.get(urlpre + path,  params=params)

        result = self.__toJson__(respond.text)
        if result is None:
            return "Get operation err!"+respond.text, None
        if 'status' not in result:
            return None, result
        if 'message' in result and result['message'] is not None:
            return result['message'], None
        return "Get operation err!", None
        

    def __getItems__(self, path, params={}, retry=3):
        params['limit'] = 50
        params['offset'] = 0
        ret = []
        while True:
            msg, data = self.__get__(path, params, retry)
            if msg is not None:
                return msg, None
            num = 0
            for item in data["items"]:
                num += 1
                ret.append(item)
            if num < 50:
                break
            params['offset'] += num
        return None, ret

    def __getQualityString__(self, quality: AudioQuality):
        if quality == AudioQuality.Normal:
            return "5"
        if quality == AudioQuality.High:
            return "6"
        if quality == AudioQuality.HiFi:
            return "7"
        return "27"

   
    def getAlbum(self, id):
        msg, data = self.__get__('/album/get?album_id=' + str(id))
        model = aigpy.model.dictToModel(data, Album())
        if msg is None:
            model.tracks = aigpy.model.dictListToModelList(data["tracks"]["items"], Track())
        return msg, model


    def getPlaylist(self, id):
        params = {
            'playlist_id': id,
            'extra': 'tracks',
            'offset': 0,
            'limit': 10000,
        }
        msg, data = self.__get__('/playlist/get', params)
        model = aigpy.model.dictToModel(data, Playlist())
        if msg is None:
            model.tracks = aigpy.model.dictListToModelList(data["tracks"]["items"], Track())
        return msg, model


    def getArtist(self, id):
        params = {
            'artist_id': id,
            'extra': 'albums',
            'offset': 0,
            'limit': 10000,
        }
        msg, data = self.__get__('/artist/get', params)
        model = aigpy.model.dictToModel(data, Artist())
        if msg is None:
            model.albums = aigpy.model.dictListToModelList(data["albums"]["items"], Album())
        return msg, model


    def getTrack(self, id):
        msg, data = self.__get__('/track/get?track_id=' + str(id))
        return msg, aigpy.model.dictToModel(data, Track())


    def getItems(self, id, type: Type):
        if type == Type.Playlist:
            msg, data = self.__getItems__('playlists/' + str(id) + "/items")
        elif type == Type.Album:
            msg, data = self.__getItems__('albums/' + str(id) + "/items")
        else:
            return "invalid Type!", None, None
        if msg is not None:
            return msg, None, None
        tracks = []
        for item in data:
            tracks.append(aigpy.model.dictToModel(item['item'], Track()))
        return msg, tracks

    # def getArtistAlbums(self, id, includeEP=False):
    #     albums = []
    #     msg, data = self.__getItems__('artists/' + str(id) + "/albums")
    #     if msg is not None:
    #         return msg, None
    #     for item in data:
    #         albums.append(dictToModel(item, Album()))
    #     if includeEP == False:
    #         return None, albums
    #     msg, data = self.__getItems__('artists/' + str(id) + "/albums", {"filter": "EPSANDSINGLES"})
    #     if msg is not None:
    #         return msg, None
    #     for item in data:
    #         albums.append(dictToModel(item, Album()))
    #     return None, albums

    def getStreamUrl(self, id, quality: AudioQuality):
        squality = self.__getQualityString__(quality)
        unix = time.time()
        buffer = "trackgetFileUrlformat_id{}intentstreamtrack_id{}{}{}".format(squality, str(id), str(unix), __APP_SECRET__)
        signature = hashlib.md5(buffer.encode("utf-8")).hexdigest()

        params = {
            "track_id": id,
            "request_ts": unix,
            "request_sig": signature,
            "format_id": squality,
            "intent": "stream",
        }
        msg, data = self.__get__('/track/getFileUrl', params)
        return msg, aigpy.model.dictToModel(data, StreamUrl())


    # def getTrackContributors(self, id):
    #     msg, data = self.__get__('tracks/' + str(id) + "/contributors")
    #     if msg is not None:
    #         return msg, None
    #     return None, data

    def getCoverUrl(self, sid, width="320", height="320"):
        if sid is None or sid == "":
            return None
        # return "https://resources.tidal.com/images/" + sid.replace("-", "/") + "/" + width + "x" + height + ".jpg"
        return ""

    def getArtistsName(self, artists=[]):
        if artists is None:
            return ""
        array = []
        return " / ".join(array.append(item.name) for item in artists)

    # def getFlag(self, data, type: Type, short=True, separator=" / "):
    #     master = False
    #     atmos = False
    #     explicit = False
    #     if type == Type.Album or type == Type.Track:
    #         if data.audioQuality == "HI_RES":
    #             master = True
    #         if "DOLBY_ATMOS" in data.audioModes:
    #             atmos = True
    #         if data.explicit is True:
    #             explicit = True
    #     if type == Type.Video:
    #         if data.explicit is True:
    #             explicit = True
    #     if not master and not atmos and not explicit:
    #         return ""
    #     array = []
    #     if master:
    #         array.append("M" if short else "Master")
    #     if atmos:
    #         array.append("A" if short else "Dolby Atmos")
    #     if explicit:
    #         array.append("E" if short else "Explicit")
    #     return separator.join(array)

    def parseUrl(self, url):
        etype = Type.Null
        sid = ""
        if "qobuz.com" not in url:
            return etype, sid

        url = url.lower()
        if 'artist' in url:
            etype = Type.Artist
        if 'album' in url:
            etype = Type.Album
        if 'track' in url:
            etype = Type.Track
        if 'playlist' in url:
            etype = Type.Playlist

        if etype == Type.Null:
            return etype, sid

        sid = aigpy.string.getSub(url, etype.name.lower() + '/', '/')
        return etype, sid


    def getByString(self, string):
        etype = Type.Null
        obj = None

        if aigpy.string.isNull(string):
            return "Please enter something.", etype, obj
        etype, sid = self.parseUrl(string)
        if aigpy.string.isNull(sid):
            sid = string

        if obj is None and (etype == Type.Null or etype == Type.Track):
            msg, obj = self.getTrack(sid)
        if obj is None and (etype == Type.Null or etype == Type.Album):
            msg, obj = self.getAlbum(sid)
        if obj is None and (etype == Type.Null or etype == Type.Playlist):
            msg, obj = self.getPlaylist(sid)
        if obj is None and (etype == Type.Null or etype == Type.Artist):
            msg, obj = self.getArtist(sid)


        if obj is None or etype != Type.Null:
            return msg, etype, obj
        if obj.__class__ == Album:
            etype = Type.Album
        if obj.__class__ == Artist:
            etype = Type.Artist
        if obj.__class__ == Track:
            etype = Type.Track
        if obj.__class__ == Playlist:
            etype = Type.Playlist
        return msg, etype, obj


# api = QobuzAPI()
# # api.login("Yaron202101@icloud.com", "ede4477fe3b8ba54cde94b9049cba838")
# msg, obj = api.getArtist("167422")
# msg, obj = api.getTrack("72552900")
# msg, obj = api.getAlbum("z2u0t8ukvm5pb")
# msg, obj = api.getPlaylist("1452423")
# msg = 0
