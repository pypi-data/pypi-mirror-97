#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   __init__.py
@Time    :   2020/11/08
@Author  :   Yaronzz
@Version :   2.1
@Contact :   yaronhuang@foxmail.com
@Desc    :   
'''
import logging
import os
import requests
import prettytable
import ssl
import sys
import getopt
import time
import aigpy

from qobuzzz_dl.qobuz import QobuzAPI
from qobuzzz_dl.settings import Settings, TokenSettings, getLogPath
from qobuzzz_dl.printf import Printf, VERSION
from qobuzzz_dl.download import start
from qobuzzz_dl.enum import AudioQuality
from qobuzzz_dl.lang.language import getLang, setLang, initLang, getLangChoicePrint

ssl._create_default_https_context = ssl._create_unverified_context

API = QobuzAPI()
TOKEN = TokenSettings.read()
CONF = Settings.read()
LANG = initLang(CONF.language)

logging.basicConfig(filename=getLogPath(),
                    level=logging.INFO,
                    format='%(asctime)s - %(levelname)s: %(message)s')

def login(username="", password=""):
    while True:
        if aigpy.string.isNull(username) or aigpy.string.isNull(password):
            print("---------------" + LANG.CHOICE_LOGIN + "-----------------")
            username = Printf.enter(LANG.PRINT_USERNAME)
            password = Printf.enter(LANG.PRINT_PASSWORD)
        msg, check = API.login(username, password)
        if check == False:
            Printf.err(msg)
            username = ""
            password = ""
            continue
        break

    TOKEN.username = username
    TOKEN.password = password
    TOKEN.userid = API.key.userid
    TOKEN.countryCode = API.key.countryCode
    TOKEN.user_auth_token = API.key.user_auth_token
    TokenSettings.save(TOKEN)


def checkLogin():
    login(TOKEN.username, TOKEN.password)


def checkLogout():
    login()


def changeSettings():
    global LANG
    Printf.settings(CONF)
    choice = Printf.enter(LANG.CHANGE_START_SETTINGS)
    if choice == '0':
        return

    CONF.downloadPath = Printf.enterPath(LANG.CHANGE_DOWNLOAD_PATH, LANG.MSG_PATH_ERR, '0', CONF.downloadPath)
    CONF.audioQuality = AudioQuality(int(Printf.enterLimit(
        LANG.CHANGE_AUDIO_QUALITY, LANG.MSG_INPUT_ERR, ['0', '1', '2', '3'])))
    # CONF.videoQuality = AudioQuality(int(Printf.enterLimit(
        # LANG.CHANGE_VIDEO_QUALITY, LANG.MSG_INPUT_ERR, ['0', '1', '2', '3'])))
    # CONF.onlyM4a = Printf.enter(LANG.CHANGE_ONLYM4A) == '1'
    CONF.checkExist = Printf.enter(LANG.CHANGE_CHECK_EXIST) == '1'
    # CONF.includeEP = Printf.enter(LANG.CHANGE_INCLUDE_EP) == '1'
    CONF.saveCovers = Printf.enter(LANG.CHANGE_SAVE_COVERS) == '1'
    CONF.showProgress = Printf.enter(LANG.CHANGE_SHOW_PROGRESS) == '1'
    CONF.language = Printf.enter(LANG.CHANGE_LANGUAGE + "(" + getLangChoicePrint() + "):")
    CONF.albumFolderFormat = Printf.enterFormat(
        LANG.CHANGE_ALBUM_FOLDER_FORMAT, CONF.albumFolderFormat, Settings.getDefaultAlbumFolderFormat())
    CONF.trackFileFormat = Printf.enterFormat(LANG.CHANGE_TRACK_FILE_FORMAT,
                                              CONF.trackFileFormat, Settings.getDefaultTrackFileFormat())

    LANG = setLang(CONF.language)
    Settings.save(CONF)


def mainCommand():
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hvl:o:q:r:", ["help", "version",
                                                                "link=", "output=", "quality", "resolution"])
    except getopt.GetoptError as errmsg:
        Printf.err(vars(errmsg)['msg'] + ". Use 'tidal-dl -h' for useage.")
        return

    for opt, val in opts:
        if opt in ('-h', '--help'):
            Printf.usage()
            return
        if opt in ('-v', '--version'):
            Printf.logo()
            return
        if opt in ('-l', '--link'):
            checkLogin()
            start(TOKEN, CONF, val)
            return
        if opt in ('-o', '--output'):
            CONF.downloadPath = val
            Settings.save(CONF)
            return
        if opt in ('-q', '--quality'):
            CONF.audioQuality = Settings.getAudioQuality(val)
            Settings.save(CONF)
            return

        if not aigpy.path.mkdirs(CONF.downloadPath):
            Printf.err(LANG.MSG_PATH_ERR + CONF.downloadPath)
            return


def main():
    if len(sys.argv) > 1:
        mainCommand()
        return

    Printf.logo()
    Printf.settings(CONF)

    checkLogin()

    onlineVer = aigpy.pip.getLastVersion('tidal-dl')
    if not aigpy.string.isNull(onlineVer):
        icmp = aigpy.system.cmpVersion(onlineVer, VERSION)
        if icmp > 0:
            Printf.info(LANG.PRINT_LATEST_VERSION + ' ' + onlineVer)

    while True:
        Printf.choices()
        choice = Printf.enter(LANG.PRINT_ENTER_CHOICE)
        if choice == "0":
            return
        elif choice == "1":
            changeSettings()
        elif choice == "2":
            checkLogout()
        else:
            start(TOKEN, CONF, choice)


if __name__ == "__main__":
    main()
    # test example
    # track 72552900
    # album z2u0t8ukvm5pb
    # artist 167422
    # playlist 1452423
