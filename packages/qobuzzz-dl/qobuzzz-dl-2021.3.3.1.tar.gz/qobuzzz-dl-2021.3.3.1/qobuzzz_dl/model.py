#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   model.py
@Time    :   2020/08/08
@Author  :   Yaronzz
@Version :   2.0
@Contact :   yaronhuang@foxmail.com
@Desc    :   
'''


class StreamUrl(object):
    track_id = 0
    duration = 0
    url = None
    format_id = 0
    mime_type = None
    sample = False
    sampling_rate = 0
    bit_depth = 0


class Image(object):
    large = None
    medium = None
    extralarge = None
    thumbnail = None
    back = None
    mega = None


class Property(object):
    id = 0
    name = None


class AudioInfo(object):
    replaygain_track_gain = 0
    replaygain_track_peak = 0


class Article(object):
    id = 0
    url = None
    price = 0
    currency = None
    type = None
    label = None
    description = None


class Artist(object):
    id = 0
    name = None
    picture = None
    albums_count = 0
    slug = None
    Image = Image()
    albums = None


class Album(object):
    qobuz_id = 0
    duration = 0
    maximum_bit_depth = 0
    tracks_count = 0
    media_count = 0
    popularity = 0
    maximum_sampling_rate = 0
    hires = False
    image = Image()
    id = None
    title = None
    subtitle = None
    version = None
    url = None
    copyright = None
    release_date_original = None
    upc = None
    description = None
    genres_list = None
    composer = Artist()
    artist = Artist()
    artists = Artist()
    articles = Article()
    tracks = None


class Track(object):
    id = 0
    duration = 0
    track_number = 0
    media_number = 0
    maximum_bit_depth = 0
    maximum_sampling_rate = 0
    hires = False
    title = None
    version = None
    isrc = None
    copyright = None
    performers = None
    album = Album()
    audio_info = AudioInfo()
    performer = Property()
    composer = Property()
    articles = Article()
    trackNumberOnPlaylist = 0


class Playlist(object):
    id = None
    name = None
    description = None
    duration = 0
    tracks_count = 0
    created_at = 0
    updated_at = 0
    images300 = None
    images150 = None
    images = None
    tracks = None
