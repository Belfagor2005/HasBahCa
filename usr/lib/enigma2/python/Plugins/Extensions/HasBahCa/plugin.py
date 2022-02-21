#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
****************************************
*        coded by Lululla              *
*             skin by MMark            *
*             20/02/2022               *
*   Thank's                            *
*      HasBahCa, Levi45, KiddaC, Pcd   *
****************************************
'''
from __future__ import print_function
from . import _
from Components.AVSwitch import AVSwitch
from Components.ActionMap import ActionMap
from Components.Button import Button
from Components.config import *
from Components.Label import Label
from Components.MenuList import MenuList
from Components.MultiContent import MultiContentEntryText, MultiContentEntryPixmapAlphaTest
# from Components.Pixmap import Pixmap
from Components.PluginComponent import plugins
from Components.PluginList import *
from Components.ScrollLabel import ScrollLabel
from Components.ServiceEventTracker import ServiceEventTracker, InfoBarBase
from Components.Sources.List import List
from Components.Sources.StaticText import StaticText
from Plugins.Plugin import PluginDescriptor
from Screens.Console import Console
from Screens.InfoBar import InfoBar
from Screens.InfoBar import MoviePlayer
from Components.ProgressBar import ProgressBar
from Components.Sources.Progress import Progress
from Screens.InfoBarGenerics import InfoBarShowHide, InfoBarSubtitleSupport, InfoBarSummarySupport, \
    InfoBarNumberZap, InfoBarMenu, InfoBarEPG, InfoBarSeek, InfoBarMoviePlayerSummarySupport, \
    InfoBarAudioSelection, InfoBarNotifications, InfoBarServiceNotifications
from Screens.MessageBox import MessageBox
from Screens.Screen import Screen
from Tools.Directories import SCOPE_PLUGINS, resolveFilename
# from Tools.LoadPixmap import LoadPixmap
from enigma import *
from enigma import RT_HALIGN_CENTER, RT_VALIGN_CENTER
from enigma import RT_HALIGN_LEFT, RT_HALIGN_RIGHT
from enigma import eListbox, eTimer
from enigma import eListboxPythonMultiContent, eConsoleAppContainer
# from enigma import eServiceCenter
from enigma import eServiceReference
# from enigma import eSize, ePicLoad
from enigma import iPlayableService
from enigma import gFont
from enigma import iServiceInformation
from enigma import loadPNG
# from enigma import quitMainloop
# from enigma import eDVBDB
# from os import path, listdir, remove, mkdir, chmod
# from twisted.web.client import downloadPage, getPage
# from xml.dom import Node, minidom
# import base64
import glob
# import time
import os
import re
# import shutil
import six
import ssl
import sys


try:
    from Plugins.Extensions.HasBahCa.Utils import *
except:
    from . import Utils

global pngs
global downloadhasba
downloadhasba = None

PY3 = sys.version_info.major >= 3
if PY3:
    from http.client import HTTPConnection, CannotSendRequest, BadStatusLine, HTTPException
    from urllib.error import URLError, HTTPError
    from urllib.request import urlopen, Request
    from urllib.parse import urlparse
    from urllib.parse import parse_qs, urlencode
    unicode = str
    unichr = chr
    long = int
    PY3 = True
else:
    from httplib import HTTPConnection, CannotSendRequest, BadStatusLine, HTTPException
    from urllib2 import urlopen, Request, URLError, HTTPError
    from urlparse import urlparse, parse_qs
    from urllib import urlencode
    import httplib
    import six
try:
    from Components.UsageConfig import defaultMoviePath
    downloadhasba = defaultMoviePath()
except:
    if os.path.exists("/usr/bin/apt-get"):
        downloadhasba = ('/media/hdd/movie/')
if sys.version_info >= (2, 7, 9):
    try:
        sslContext = ssl._create_unverified_context()
    except:
        sslContext = None
try:
    from twisted.internet import ssl
    from twisted.internet._sslverify import ClientTLSOptions
    sslverify = True
except:
    sslverify = False
if sslverify:
    class SNIFactory(ssl.ClientContextFactory):
        def __init__(self, hostname=None):
            self.hostname = hostname

        def getContext(self):
            ctx = self._contextFactory(self.method)
            if self.hostname:
                ClientTLSOptions(self.hostname, ctx)
            return ctx

def ssl_urlopen(url):
    if sslContext:
        return urlopen(url, context=sslContext)
    else:
        return urlopen(url)

global path_skin
currversion = '1.1'
title_plug = 'HasBahCa '
desc_plugin = ('..:: HasBahCa by Lululla %s ::.. ' % currversion)
plugin_path = resolveFilename(SCOPE_PLUGINS, "Extensions/{}".format('HasBahCa'))
pluglogo = resolveFilename(SCOPE_PLUGINS, "Extensions/{}/res/pics/logo.png".format('HasBahCa'))
png = resolveFilename(SCOPE_PLUGINS, "Extensions/{}/res/pics/setting.png".format('HasBahCa'))
path_skin = resolveFilename(SCOPE_PLUGINS, "Extensions/{}/res/skins/hd/".format('HasBahCa'))

enigma_path = '/etc/enigma2'
if isFHD():
    path_skin = resolveFilename(SCOPE_PLUGINS, "Extensions/{}/res/skins/fhd/".format('HasBahCa'))
if DreamOS():
    path_skin = path_skin + 'dreamOs/'
print('HasBahCa path_skin: ', path_skin)



Panel_Dlist = [
    ('A-CATEGORY'),
    ('A-FILMON'),
    ('A-FULL LIST SIMPLE'),
    ('A-FULL LIST'),
    ('A-IPTV'),
    ('A-RADIO'),
    ('A-VOD FILM'),
    ('A-WEBCAM'),
    ('IPTV AFGHANISTAN'),
    ('IPTV AFRICA'),
    ('IPTV ALBANIA BOSNIA KOSOVO'),
    ('IPTV ARABIC 1'),
    ('IPTV ARABIC 2'),
    ('IPTV ARGENTINA'),
    ('IPTV ASIA MIX MNC'),
    ('IPTV AVUSTURALYA NZELAND'),
    ('IPTV BALTIC EST LIT LET'),
    ('IPTV BANGLADESH'),
    ('IPTV BRASIL PLUTO'),
    ('IPTV BRASIL'),
    ('IPTV BULGARSAT'),
    ('IPTV CAMBODIA'),
    ('IPTV CANADA ABD'),
    ('IPTV CANADA'),
    ('IPTV CHILE'),
    ('IPTV CHINA1'),
    ('IPTV CHINA2'),
    ('IPTV COLOMBIA'),
    ('IPTV COSTARICA'),
    ('IPTV CROATIA'),
    ('IPTV CZECH HU POLSKI'),
    ('IPTV DEUTSCH GERMAN LOKAL'),
    ('IPTV DEUTSCH GERMAN PLUTO'),
    ('IPTV DEUTSCH GERMAN TVPLUS'),
    ('IPTV DEUTSCH GERMAN'),
    ('IPTV DOMINICAN'),
    ('IPTV FRANCE PLUTO'),
    ('IPTV FRANCE TVPLUS'),
    ('IPTV FRANCE'),
    ('IPTV GREAT BRITAIN PLUTO'),
    ('IPTV GREAT BRITAIN TVPLUS'),
    ('IPTV GREATBRITAIN ENGLAND'),
    ('IPTV GREEK RADIO'),
    ('IPTV GREEK'),
    ('IPTV HAITI'),
    ('IPTV HOLLAND BELGIEN'),
    ('IPTV HOLLAND PLUTO'),
    ('IPTV HONDURAS'),
    ('IPTV HUNGARY MAGYAR'),
    ('IPTV ICELAND'),
    ('IPTV INDIA HINDI TAMIL'),
    ('IPTV INDONESIA'),
    ('IPTV ISRAEL'),
    ('IPTV ITALIA'),
    ('IPTV ITALY PLUTO'),
    ('IPTV ITALY TVPLUS'),
    ('IPTV JAPAN'),
    ('IPTV KHUSUS MALAZIA'),
    ('IPTV KOREA'),
    ('IPTV LAOS'),
    ('IPTV LATINO MIX 1'),
    ('IPTV LATINO MIX 2'),
    ('IPTV LATINO PLUTOTV'),
    ('IPTV LUXEMBOURG'),
    ('IPTV MAKEDONIA'),
    ('IPTV MALTA'),
    ('IPTV MEXICO PLUTO'),
    ('IPTV MEXICO'),
    ('IPTV NORWAY'),
    ('IPTV OSTERREICH AVUSTURIA'),
    ('IPTV OSTERREICH AVUSTURYA PLUTOTV TVPLUS'),
    ('IPTV OSTERREICH AVUSTURYA TVPLUS'),
    ('IPTV PAKISTAN'),
    ('IPTV PANAMA'),
    ('IPTV PERU'),
    ('IPTV POLSKI'),
    ('IPTV PORTUGAL'),
    ('IPTV RELAX'),
    # ('IPTV RELAX TIME'),
    ('IPTV ROMANIA MOLDOVA'),
    ('IPTV RUS ARMENIA'),
    ('IPTV RUS EX CCCP PROSTOTV'),
    # ('IPTV RUS EX CCCP RADIOS'),
    ('IPTV RUS EX CCCP REGIONAL'),
    ('IPTV RUS EX CCCP1'),
    ('IPTV RUS EX CCCP2'),
    ('IPTV RUS GEORGIA'),
    ('IPTV RUS KAZAKHSTAN'),
    ('IPTV RUS LATVIA'),
    ('IPTV RUS UKRAINA1'),
    ('IPTV RUS UKRAINA2'),
    ('IPTV RUS VOD MOVIE'),
    ('IPTV SERBIA'),
    ('IPTV SERBIA SIRBISTAN'),
    ('IPTV SKANDINAV FINLAND'),
    ('IPTV SLOVAKIA SLOVEINA'),
    ('IPTV SPAIN PLUTO'),
    ('IPTV SPAIN'),
    ('IPTV SWITZERLAND SCHWEIZ PLUTO'),
    ('IPTV SWITZERLAND SCHWEIZ'),
    ('IPTV SWITZERLAND TVPLUS'),
    ('IPTV TAIWAN'),
    ('IPTV THAILAND'),
    ('IPTV TURKEY TURKIYE AVRUPA'),
    ('IPTV TURKEY TURKIYE BELGESEL'),
    ('IPTV TURKEY TURKIYE BLUTVGENEL'),
    ('IPTV TURKEY TURKIYE COCUK'),
    ('IPTV TURKEY TURKIYE DIGER'),
    ('IPTV TURKEY TURKIYE DINI'),
    ('IPTV TURKEY TURKIYE FILMER'),
    ('IPTV TURKEY TURKIYE GENEL'),
    ('IPTV TURKEY TURKIYE HABER'),
    # ('IPTV TURKEY TURKIYE KARISIK MIX'),
    ('IPTV TURKEY TURKIYE MIX'),
    ('IPTV TURKEY TURKIYE MUZIK'),
    ('IPTV TURKEY TURKIYE RADYO'),
    ('IPTV TURKEY TURKIYE SPOR'),
    ('IPTV TURKEY TURKIYE YEREL'),
    ('IPTV TURKI STAATEN'),
    ('IPTV URUGUAY'),
    ('IPTV USA 1'),
    ('IPTV USA 2'),
    ('IPTV USA CHINA ENGLISH'),
    ('IPTV USA LOCAL'),
    ('IPTV USA MYTVTO VELLYTV'),
    ('IPTV USA PLEX'),
    ('IPTV USA PLUTO'),
    ('IPTV USA TVPLUS'),
    ('IPTV USA XUMO'),
    ('IPTV VIETNAM'),
    ('IPTV WORLD MIXTV'),
    ('IPTV WORLD MUSIC'),
    ('IPTV WORLD SPORTS'),
    ('WEBCAM CHINA CIN'),
    ('WEBCAM DE AU CH'),
    ('WEBCAM MIX'),
    ('WEBCAM POLSKI'),
    ('WEBCAM PORTUGAL'),
    # ('WEBCAM RUS EX CCCP SOCHICAM'),
    ('WEBCAM RUS EX CCCP'),
    ('WEBCAM TURKEY'),
    ('WEBCAM USA'),
    ]

def downloadFile(url, target):
    try:
        response = urlopen(url, timeout=10)
        with open(target, 'wb') as output:
            output.write(response.read())
        return True
    except:
        print("downloadFile error")
        return False

class hasList(MenuList):
    def __init__(self, list):
        MenuList.__init__(self, list, True, eListboxPythonMultiContent)
        self.l.setItemHeight(50)
        textfont = int(24)
        self.l.setFont(0, gFont('Regular', textfont))
        if isFHD():
            self.l.setItemHeight(50)
            textfont = int(34)
            self.l.setFont(0, gFont('Regular', textfont))

def hasListEntry(name, idx):
    res = [name]
    png = resolveFilename(SCOPE_PLUGINS, "Extensions/{}/res/pics/setting.png".format('HasBahCa'))
    if isFHD():
        res.append(MultiContentEntryPixmapAlphaTest(pos=(10, 12), size=(34, 25), png=loadPNG(png)))
        res.append(MultiContentEntryText(pos=(60, 0), size=(1900, 50), font=0, text=name, color=0xa6d1fe, flags=RT_HALIGN_LEFT | RT_VALIGN_CENTER))
    else:
        res.append(MultiContentEntryPixmapAlphaTest(pos=(10, 12), size=(34, 25), png=loadPNG(png)))
        res.append(MultiContentEntryText(pos=(60, 0), size=(1000, 50), font=0, text=name, color=0xa6d1fe, flags=RT_HALIGN_LEFT | RT_VALIGN_CENTER))
    return res

def hasbaSetListEntry(name):
    res = [name]
    png = resolveFilename(SCOPE_PLUGINS, "Extensions/{}/res/pics/setting.png".format('HasBahCa'))
    res.append(MultiContentEntryPixmapAlphaTest(pos=(10, 12), size=(34, 25), png=loadPNG(png)))
    res.append(MultiContentEntryText(pos=(60, 0), size=(1000, 50), font=0, text=name, color=0xa6d1fe, flags=RT_HALIGN_LEFT | RT_VALIGN_CENTER))
    if isFHD():
        res.append(MultiContentEntryPixmapAlphaTest(pos=(10, 12), size=(34, 25), png=loadPNG(png)))
        res.append(MultiContentEntryText(pos=(60, 0), size=(1200, 50), font=0, text=name, color=0xa6d1fe, flags=RT_HALIGN_LEFT | RT_VALIGN_CENTER))
    else:
        res.append(MultiContentEntryPixmapAlphaTest(pos=(10, 12), size=(34, 25), png=loadPNG(png)))
        res.append(MultiContentEntryText(pos=(60, 0), size=(1000, 50), font=0, text=name, color=0xa6d1fe, flags=RT_HALIGN_LEFT | RT_VALIGN_CENTER))
    return res

def showlisthasba(data, list):
    icount = 0
    plist = []
    for line in data:
        name = data[icount]
        plist.append(hasbaSetListEntry(name))
        icount = icount + 1
        list.setList(plist)

class MainHasBahCa(Screen):
    def __init__(self, session):
        self.session = session
        skin = path_skin + 'settings.xml'
        with open(skin, 'r') as f:
            self.skin = f.read()
        self.setup_title = ('MainHasBahCa')
        Screen.__init__(self, session)
        self.setTitle(title_plug)
        self['text'] = hasList([])
        self['title'] = Label(title_plug)
        self['info'] = Label(_('Loading data... Please wait'))
        self['key_red'] = Button(_('Exit'))
        self['key_green'] = Button(_('Select'))
        self['key_yellow'] = Button(_(''))
        self["key_blue"] = Button(_(''))
        self['key_green'].hide()
        self['key_yellow'].hide()
        self['key_blue'].hide()
        self['live'] = Label('')
        self['live'].setText('')
        self['actions'] = ActionMap(['SetupActions', 'ColorActions', ], {
            'ok': self.okRun,
            'green': self.okRun,
            'back': self.closerm,
            'red': self.closerm,
            'cancel': self.closerm}, -1)
        self.onFirstExecBegin.append(self.updateMenuList)
        self.onLayoutFinish.append(self.__layoutFinished)

    def __layoutFinished(self):
        self.setTitle(self.setup_title)

    def closerm(self):
        deletetmp()
        self.close()

    def updateMenuList(self):
        self.menu_list = []
        for x in self.menu_list:
            del self.menu_list[0]
        list = []
        idx = 0
        for x in Panel_Dlist:

            list.append(hasListEntry(x, idx))
            self.menu_list.append(x)
            idx += 1

        # self.menu_list.sort()

        self["live"].setText('N.' + str(idx) + " CATEGORY")
        self['text'].setList(list)
        self['info'].setText(_('Please select ...'))
        self['key_green'].show()

    def okRun(self):
        self.keyNumberGlobalCB(self['text'].getSelectedIndex())

    def keyNumberGlobalCB(self, idx):
        sel = self.menu_list[idx]
        host = 'https://raw.githubusercontent.com/HasBahCa/IPTV-LIST/main/'
        if sel == ('A-CATEGORY'):
                    url = 'https://github.com/HasBahCa/IPTV-LIST'
                    self.session.open(HasBahCa, sel, url)

        if sel == ('A-FULL LIST'):
                    url = host + 'HasBahCa_IPTV_FULL.m3u'
                    self.session.open(HasBahCa1, sel, url)
        elif sel == ('A-FULL LIST SIMPLE'):
                    url = host + 'HasBahCa_IPTV_FULL_simple.m3u'
                    self.session.open(HasBahCa1, sel, url)
        elif sel == ('A-IPTV'):
                    url = host + 'hasbahca_iptv.m3u'
                    self.session.open(HasBahCa1, sel, url)
        elif sel == ('A-VOD FILM'):
                    url = host + 'HasBahCa_VOD_MOVIES_FILM.m3u'
                    self.session.open(HasBahCa1, sel, url)
        elif sel == ('A-RADIO'):
                    url = host + 'HasBahCa_webWORLD_RADIOS.m3u '
                    self.session.open(HasBahCa1, sel, url)
        elif sel == ('A-WEBCAM'):
                    url = host + 'HasBahCa_WEBCAM.m3u'
                    self.session.open(HasBahCa1, sel, url)
        elif sel == ('A-FILMON'):
                    url = host + 'HasBahCa_FILMon.m3u'
                    self.session.open(HasBahCa1, sel, url)
        elif sel == ('IPTV AFRICA'):
                    url = host + 'HasBahCa_AFRICA_AFRIKA_TV.m3u'
                    self.session.open(HasBahCa1, sel, url)
        elif sel == ('IPTV ISRAEL'):
                    url = host + 'HasBahCa_AFRICA_ISRAEL_israil_TV.m3u'
                    self.session.open(HasBahCa1, sel, url)
        elif sel == ('IPTV CANADA'):
                    url = host + 'HasBahCa_Amerika_Canada.m3u'
                    self.session.open(HasBahCa1, sel, url)
        elif sel == ('IPTV USA LOCAL'):
                    url = host + 'HasBahCa_USA_ABD_LOCALS.m3u'
                    self.session.open(HasBahCa1, sel, url)
        elif sel == ('IPTV USA PLEX'):
                    url = host + 'HasBahCa_USA_ABD_PLEX.m3u'
                    self.session.open(HasBahCa1, sel, url)
        elif sel == ('IPTV USA PLUTO'):
                    url = host + 'HasBahCa_USA_ABD_PLUTO.m3u'
                    self.session.open(HasBahCa1, sel, url)
        elif sel == ('IPTV USA MYTVTO VELLYTV'):
                    url = host + 'HasBahCa_USA_MyTvTo_VellyTV.m3u'
                    self.session.open(HasBahCa1, sel, url)
        elif sel == ('IPTV USA TVPLUS'):
                    url = host + 'HasBahCa_USA_TVPLUS.m3u'
                    self.session.open(HasBahCa1, sel, url)
        elif sel == ('IPTV USA XUMO'):
                    url = host + 'HasBahCa_USA_XUMO.m3u'
                    self.session.open(HasBahCa1, sel, url)
        elif sel == ('IPTV USA 1'):
                    url = host + 'HasBahCa_USA_United_States_Amerika1.m3u'
                    self.session.open(HasBahCa1, sel, url)
        elif sel == ('IPTV USA 2'):
                    url = host + 'HasBahCa_USA_United_States_Amerika2.m3u'
                    self.session.open(HasBahCa1, sel, url)
        elif sel == ('IPTV ARGENTINA'):
                    url = host + 'HasBahCa_Amerika_Argentina_Arjantin.m3u'
                    self.session.open(HasBahCa1, sel, url)
        elif sel == ('IPTV BRASIL'):
                    url = host + 'HasBahCa_Amerika_Brasil_BREZILYA.m3u'
                    self.session.open(HasBahCa1, sel, url)
        elif sel == ('IPTV BRASIL PLUTO'):
                    url = host + 'HasBahCa_Amerika_Brazil_PLUTO.m3u'
                    self.session.open(HasBahCa1, sel, url)
        elif sel == ('IPTV CANADA ABD'):
                    url = host + 'HasBahCa_Amerika_Canada.m3u'
                    self.session.open(HasBahCa1, sel, url)
        elif sel == ('IPTV CHILE'):
                    url = host + 'HasBahCa_Amerika_CHILE.m3u'
                    self.session.open(HasBahCa1, sel, url)
        elif sel == ('IPTV COLOMBIA'):
                    url = host + 'HasBahCa_Amerika_COLOMBIA.m3u'
                    self.session.open(HasBahCa1, sel, url)
        elif sel == ('IPTV COSTARICA'):
                    url = host + 'HasBahCa_Amerika_COSTARICA.m3u'
                    self.session.open(HasBahCa1, sel, url)
        elif sel == ('IPTV DOMINICAN'):
                    url = host + 'HasBahCa_Amerika_DOMINICAN_REPUBLIC.m3u'
                    self.session.open(HasBahCa1, sel, url)
        elif sel == ('IPTV HAITI'):
                    url = host + 'HasBahCa_Amerika_HAITI.m3u'
                    self.session.open(HasBahCa1, sel, url)
        elif sel == ('IPTV HONDURAS'):
                    url = host + 'HasBahCa_Amerika_HONDURAS.m3u'
                    self.session.open(HasBahCa1, sel, url)
        elif sel == ('IPTV LATINO MIX 1'):
                    url = host + 'HasBahCa_Amerika_Latino_MIX1.m3u'
                    self.session.open(HasBahCa1, sel, url)
        elif sel == ('IPTV LATINO MIX 2'):
                    url = host + 'HasBahCa_Amerika_Latino_MIX2.m3u'
                    self.session.open(HasBahCa1, sel, url)
        elif sel == ('IPTV LATINO PLUTOTV'):
                    url = host + 'HasBahCa_Amerika_Latino_PLUTOTV.m3u'
                    self.session.open(HasBahCa1, sel, url)
        elif sel == ('IPTV MEXICO'):
                    url = host + 'HasBahCa_Amerika_MEXICO_Meksika.m3u'
                    self.session.open(HasBahCa1, sel, url)
        elif sel == ('IPTV MEXICO PLUTO'):
                    url = host + 'HasBahCa_Amerika_MEXICO_PLUTO.m3u'
                    self.session.open(HasBahCa1, sel, url)
        elif sel == ('IPTV PANAMA'):
                    url = host + 'HasBahCa_Amerika_PANAMA.m3u'
                    self.session.open(HasBahCa1, sel, url)
        elif sel == ('IPTV PERU'):
                    url = host + 'HasBahCa_Amerika_PERU.m3u'
                    self.session.open(HasBahCa1, sel, url)
        elif sel == ('IPTV URUGUAY'):
                    url = host + 'HasBahCa_Amerika_URUGUAY.m3u'
                    self.session.open(HasBahCa1, sel, url)
        elif sel == ('IPTV ARABIC 1'):
                    url = host + 'HasBahCa_Arabic_ARAPCA1.m3u'
                    self.session.open(HasBahCa1, sel, url)
        elif sel == ('IPTV ARABIC 2'):
                    url = host + 'HasBahCa_Arabic_ARAPCA2.m3u'
                    self.session.open(HasBahCa1, sel, url)
        elif sel == ('IPTV AFGHANISTAN'):
                    url = host + 'HasBahCa_ASIA_Afghanistan.m3u'
                    self.session.open(HasBahCa1, sel, url)
        elif sel == ('IPTV BANGLADESH'):
                    url = host + 'HasBahCa_ASIA_Bangladesh.m3u'
                    self.session.open(HasBahCa1, sel, url)
        elif sel == ('IPTV CAMBODIA'):
                    url = host + 'HasBahCa_ASIA_CAMBODIA.m3u'
                    self.session.open(HasBahCa1, sel, url)
        elif sel == ('IPTV CHINA1'):
                    url = host + 'HasBahCa_ASIA_China1.m3u'
                    self.session.open(HasBahCa1, sel, url)
        elif sel == ('IPTV CHINA2'):
                    url = host + 'HasBahCa_ASIA_China2.m3u'
                    self.session.open(HasBahCa1, sel, url)
        elif sel == ('IPTV INDIA HINDI TAMIL'):
                    url = host + 'HasBahCa_ASIA_INDIA_HINDI_TAMIL.m3u'
                    self.session.open(HasBahCa1, sel, url)
        elif sel == ('IPTV INDONESIA'):
                    url = host + 'HasBahCa_ASIA_Indonesia.m3u'
                    self.session.open(HasBahCa1, sel, url)
        elif sel == ('IPTV JAPAN'):
                    url = host + 'HasBahCa_ASIA_Japan_JAPONYA.m3u'
                    self.session.open(HasBahCa1, sel, url)
        elif sel == ('IPTV KHUSUS MALAZIA'):
                    url = host + 'HasBahCa_ASIA_Khusus_MALAZIA.m3u'
                    self.session.open(HasBahCa1, sel, url)
        elif sel == ('IPTV KOREA'):
                    url = host + 'HasBahCa_ASIA_Korea_KORE.m3u'
                    self.session.open(HasBahCa1, sel, url)
        elif sel == ('IPTV LAOS'):
                    url = host + 'HasBahCa_ASIA_Laos.m3u'
                    self.session.open(HasBahCa1, sel, url)
        elif sel == ('IPTV ASIA MIX MNC'):
                    url = host + 'HasBahCa_ASIA_MIX_MNC.m3u'
                    self.session.open(HasBahCa1, sel, url)
        elif sel == ('IPTV PAKISTAN'):
                    url = host + 'HasBahCa_ASIA_Pakistan.m3u'
                    self.session.open(HasBahCa1, sel, url)
        elif sel == ('IPTV TAIWAN'):
                    url = host + 'HasBahCa_ASIA_Taiwan.m3u'
                    self.session.open(HasBahCa1, sel, url)
        elif sel == ('IPTV THAILAND'):
                    url = host + 'HasBahCa_ASIA_Thai_TAYLAND.m3u'
                    self.session.open(HasBahCa1, sel, url)
        elif sel == ('IPTV VIETNAM'):
                    url = host + 'HasBahCa_ASIA_Vietnam.m3u'
                    self.session.open(HasBahCa1, sel, url)
        elif sel == ('IPTV AVUSTURALYA NZELAND'):
                    url = host + 'HasBahCa_Australia_AVUSTURALYA_NZeland.m3u'
                    self.session.open(HasBahCa1, sel, url)
        elif sel == ('IPTV DEUTSCH GERMAN PLUTO'):
                    url = host + 'HasBahCa_DE_Deutsch_German_PLUTO.m3u'
                    self.session.open(HasBahCa1, sel, url)
        elif sel == ('IPTV DEUTSCH GERMAN'):
                    url = host + 'HasBahCa_DE_Deutsch_German_ALMANCA.m3u'
                    self.session.open(HasBahCa1, sel, url)
        elif sel == ('IPTV DEUTSCH GERMAN LOKAL'):
                    url = host + 'HasBahCa_DE_Deutsch_German_LOKAL.m3u'
                    self.session.open(HasBahCa1, sel, url)
        elif sel == ('IPTV DEUTSCH GERMAN TVPLUS'):
                    url = host + 'HasBahCa_DE_Deutsch_German_TVPLUS.m3u'
                    self.session.open(HasBahCa1, sel, url)
        elif sel == ('IPTV OSTERREICH AVUSTURIA'):
                    url = host + 'HasBahCa_DE_OSTERREICH_AVUSTURYA.m3u'
                    self.session.open(HasBahCa1, sel, url)
        elif sel == ('IPTV OSTERREICH AVUSTURYA PLUTOTV TVPLUS'):
                    url = host + 'HasBahCa_DE_OSTERREICH_AVUSTURYA_PLUTOTV_TVPLUS.m3u'
                    self.session.open(HasBahCa1, sel, url)
        elif sel == ('IPTV OSTERREICH AVUSTURYA TVPLUS'):
                    url = host + 'HasBahCa_DE_OSTERREICH_AVUSTURYA_TVPLUS.m3u'
                    self.session.open(HasBahCa1, sel, url)
        elif sel == ('IPTV SWITZERLAND SCHWEIZ'):
                    url = host + 'HasBahCa_DE_SWITZERLAND_SCHWEIZ.m3u'
                    self.session.open(HasBahCa1, sel, url)
        elif sel == ('IPTV SWITZERLAND SCHWEIZ PLUTO'):
                    url = host + 'HasBahCa_DE_SWITZERLAND_SCHWEIZ_PLUTO.m3u'
                    self.session.open(HasBahCa1, sel, url)
        elif sel == ('IPTV SWITZERLAND TVPLUS'):
                    url = host + 'HasBahCa_DE_SWITZERLAND_SCHWEIZ_TVPLUS.m3u'
                    self.session.open(HasBahCa1, sel, url)
        elif sel == ('IPTV GREAT BRITAIN PLUTO'):
                    url = host + 'HasBahCa_ENG_GreatBritain_PLUTO.m3u'
                    self.session.open(HasBahCa1, sel, url)
        elif sel == ('IPTV GREAT BRITAIN TVPLUS'):
                    url = host + 'HasBahCa_ENG_GreatBritain_TVPLUS.m3u'
                    self.session.open(HasBahCa1, sel, url)
        elif sel == ('IPTV GREATBRITAIN ENGLAND'):
                    url = host + 'HasBahCa_ENG_GreatBritain_England_Ingiltere.m3u'
                    self.session.open(HasBahCa1, sel, url)
        elif sel == ('IPTV ALBANIA BOSNIA KOSOVO'):
                    url = host + 'HasBahCa_EU_Albania_Bosnia_Kosovo.m3u'
                    self.session.open(HasBahCa1, sel, url)
        elif sel == ('IPTV BALTIC EST LIT LET'):
                    url = host + 'HasBahCa_EU_BALTIC_EST_LIT_LET.m3u'
                    self.session.open(HasBahCa1, sel, url)
        elif sel == ('IPTV BULGARSAT'):
                    url = host + 'HasBahCa_EU_BULGARSAT.m3u'
                    self.session.open(HasBahCa1, sel, url)
        elif sel == ('IPTV CZECH HU POLSKI'):
                    url = host + 'HasBahCa_EU_Czech_HU_Polski.m3u'
                    self.session.open(HasBahCa1, sel, url)
        elif sel == ('IPTV CROATIA'):
                    url = host + 'HasBahCa_EU_EXYUGOSLAVIA_CROATIA.m3u'
                    self.session.open(HasBahCa1, sel, url)
        elif sel == ('IPTV FRANCE'):
                    url = host + 'HasBahCa_EU_France_FRANSA.m3u'
                    self.session.open(HasBahCa1, sel, url)
        elif sel == ('IPTV FRANCE PLUTO'):
                    url = host + 'HasBahCa_EU_France_PLUTO.m3u'
                    self.session.open(HasBahCa1, sel, url)
        elif sel == ('IPTV FRANCE TVPLUS'):
                    url = host + 'HasBahCa_EU_France_TVPLUS.m3u'
                    self.session.open(HasBahCa1, sel, url)
        elif sel == ('IPTV GREEK'):
                    url = host + 'HasBahCa_EU_Greek_YUNANCA.m3u'
                    self.session.open(HasBahCa1, sel, url)
        elif sel == ('IPTV GREEK RADIO'):
                    url = host + 'HasBahCa_EU_Greek_YUNANCA_RADIO.m3u'
                    self.session.open(HasBahCa1, sel, url)
        elif sel == ('IPTV HOLLAND BELGIEN'):
                    url = host + 'HasBahCa_EU_Holland_Belgien.m3u'
                    self.session.open(HasBahCa1, sel, url)
        elif sel == ('IPTV HOLLAND PLUTO'):
                    url = host + 'HasBahCa_EU_Holland_PLUTO.m3u'
                    self.session.open(HasBahCa1, sel, url)
        elif sel == ('IPTV HUNGARY MAGYAR'):
                    url = host + 'HasBahCa_EU_Hungary_Macar.m3u'
                    self.session.open(HasBahCa1, sel, url)
        elif sel == ('IPTV ICELAND'):
                    url = host + 'HasBahCa_EU_Iceland.m3u'
                    self.session.open(HasBahCa1, sel, url)
        elif sel == ('IPTV ITALIA'):
                    url = host + 'HasBahCa_EU_Italia_ITALYA.m3u'
                    self.session.open(HasBahCa1, sel, url)
        elif sel == ('IPTV ITALY PLUTO'):
                    url = host + 'HasBahCa_EU_Italy_PLUTO.m3u'
                    self.session.open(HasBahCa1, sel, url)
        elif sel == ('IPTV ITALY TVPLUS'):
                    url = host + 'HasBahCa_EU_Italy_TVPLUS.m3u'
                    self.session.open(HasBahCa1, sel, url)
        elif sel == ('IPTV LUXEMBOURG'):
                    url = host + 'HasBahCa_EU_Luxembourg.m3u'
                    self.session.open(HasBahCa1, sel, url)
        elif sel == ('IPTV MAKEDONIA'):
                    url = host + 'HasBahCa_EU_MAKEDONIA.m3u'
                    self.session.open(HasBahCa1, sel, url)
        elif sel == ('IPTV MALTA'):
                    url = host + 'HasBahCa_EU_Malta.m3u'
                    self.session.open(HasBahCa1, sel, url)
        elif sel == ('IPTV NORWAY'):
                    url = host + 'HasBahCa_EU_Norway_Norvec.m3u'
                    self.session.open(HasBahCa1, sel, url)
        elif sel == ('IPTV POLSKI'):
                    url = host + 'HasBahCa_EU_Polski_POLONYA.m3u'
                    self.session.open(HasBahCa1, sel, url)
        elif sel == ('IPTV PORTUGAL'):
                    url = host + 'HasBahCa_EU_Portugal_PORTEKIZ.m3u'
                    self.session.open(HasBahCa1, sel, url)
        elif sel == ('IPTV ROMANIA MOLDOVA'):
                    url = host + 'HasBahCa_EU_ROMANYA_MOLDOVA.m3u'
                    self.session.open(HasBahCa1, sel, url)
        elif sel == ('IPTV SERBIA'):
                    url = host + 'HasBahCa_EU_Serbia.m3u'
                    self.session.open(HasBahCa1, sel, url)
        elif sel == ('IPTV SERBIA SIRBISTAN'):
                    url = host + 'HasBahCa_EU_Serbia_SIRBISTAN.m3u'
                    self.session.open(HasBahCa1, sel, url)
        elif sel == ('IPTV SKANDINAV FINLAND'):
                    url = host + 'HasBahCa_EU_SKANDINAV_FINLAND.m3u'
                    self.session.open(HasBahCa1, sel, url)
        elif sel == ('IPTV SLOVAKIA SLOVEINA'):
                    url = host + 'HasBahCa_EU_Slovakia-Sloveina.m3u'
                    self.session.open(HasBahCa1, sel, url)
        elif sel == ('IPTV SPAIN'):
                    url = host + 'HasBahCa_EU_Spain_ISPANYOL.m3u'
                    self.session.open(HasBahCa1, sel, url)
        elif sel == ('IPTV SPAIN PLUTO'):
                    url = host + 'HasBahCa_EU_Spain_PLUTO.m3u'
                    self.session.open(HasBahCa1, sel, url)
        elif sel == ('IPTV RELAX'):
                    url = host + 'HasBahCa_RELAX.m3u'
                    self.session.open(HasBahCa1, sel, url)
        elif sel == ('IPTV RELAX TIME'):
                    url = host + 'HasBahCa_RELAXTIME.m3u'
                    self.session.open(HasBahCa1, sel, url)
        elif sel == ('IPTV RUS ARMENIA'):
                    url = host + 'HasBahCa_RUS_Armenia_ERMENISTAN.m3u'
                    self.session.open(HasBahCa1, sel, url)
        elif sel == ('IPTV RUS EX CCCP1'):
                    url = host + 'HasBahCa_RUS_EX_CCCP_Eski_SSCB1.m3u'
                    self.session.open(HasBahCa1, sel, url)
        elif sel == ('IPTV RUS EX CCCP2'):
                    url = host + 'HasBahCa_RUS_EX_CCCP_Eski_SSCB2.m3u'
                    self.session.open(HasBahCa1, sel, url)
        elif sel == ('IPTV RUS EX CCCP RADIOS'):
                    url = host + 'HasBahCa_RUS_EX_CCCP_RADIOS.m3u'
                    self.session.open(HasBahCa1, sel, url)
        elif sel == ('IPTV RUS EX CCCP REGIONAL'):
                    url = host + 'HasBahCa_RUS_EX_CCCP_REGIONAL.m3u'
                    self.session.open(HasBahCa1, sel, url)
        elif sel == ('IPTV RUS EX CCCP PROSTOTV'):
                    url = host + 'HasBahCa_RUS_EX_CCCP_prostotv.m3u'
                    self.session.open(HasBahCa1, sel, url)
        elif sel == ('IPTV RUS GEORGIA'):
                    url = host + 'HasBahCa_RUS_GEORGIA.m3u'
                    self.session.open(HasBahCa1, sel, url)
        elif sel == ('IPTV RUS KAZAKHSTAN'):
                    url = host + 'HasBahCa_RUS_Kazakhstan.m3u'
                    self.session.open(HasBahCa1, sel, url)
        elif sel == ('IPTV RUS LATVIA'):
                    url = host + 'HasBahCa_RUS_Latvia_LITVANYA.m3u'
                    self.session.open(HasBahCa1, sel, url)
        elif sel == ('IPTV RUS VOD MOVIE'):
                    url = host + 'HasBahCa_RUS_VOD_MOVIES.m3u'
                    self.session.open(HasBahCa1, sel, url)
        elif sel == ('IPTV RUS UKRAINA1'):
                    url = host + 'HasBahCa_Rus_UKRAINA1.m3u'
                    self.session.open(HasBahCa1, sel, url)
        elif sel == ('IPTV RUS UKRAINA2'):
                    url = host + 'HasBahCa_Rus_UKRAINA2.m3u'
                    self.session.open(HasBahCa1, sel, url)
        elif sel == ('IPTV TURKEY TURKIYE FILMER'):
                    url = host + 'HasBahCa_TÜRKÇE_Filmler.m3u'
                    self.session.open(HasBahCa1, sel, url)
        elif sel == ('IPTV TURKEY TURKIYE AVRUPA'):
                    url = host + 'HasBahCa_Turkey_TURKiYE_AVRUPA.m3u'
                    self.session.open(HasBahCa1, sel, url)
        elif sel == ('IPTV TURKEY TURKIYE BELGESEL'):
                    url = host + 'HasBahCa_Turkey_TURKiYE_BELGESEL.m3u'
                    self.session.open(HasBahCa1, sel, url)
        elif sel == ('IPTV TURKEY TURKIYE BLUTVGENEL'):
                    url = host + 'HasBahCa_Turkey_TURKiYE_BLUTVGENEL.m3u'
                    self.session.open(HasBahCa1, sel, url)
        elif sel == ('IPTV TURKEY TURKIYE COCUK'):
                    url = host + 'HasBahCa_Turkey_TURKiYE_COCUK.m3u'
                    self.session.open(HasBahCa1, sel, url)
        elif sel == ('IPTV TURKEY TURKIYE DIGER'):
                    url = host + 'HasBahCa_Turkey_TURKiYE_DIGER.m3u'
                    self.session.open(HasBahCa1, sel, url)
        elif sel == ('IPTV TURKEY TURKIYE DINI'):
                    url = host + 'HasBahCa_Turkey_TURKiYE_DiNi.m3u'
                    self.session.open(HasBahCa1, sel, url)
        elif sel == ('IPTV TURKEY TURKIYE GENEL'):
                    url = host + 'HasBahCa_Turkey_TURKiYE_GENEL.m3u'
                    self.session.open(HasBahCa1, sel, url)
        elif sel == ('IPTV TURKEY TURKIYE HABER'):
                    url = host + 'HasBahCa_Turkey_TURKiYE_HABER.m3u'
                    self.session.open(HasBahCa1, sel, url)
        elif sel == ('IPTV TURKEY TURKIYE KARISIK MIX'):
                    url = host + 'HasBahCa_Turkey_KARISIK_MIX.m3u'
                    self.session.open(HasBahCa1, sel, url)
        elif sel == ('IPTV TURKEY TURKIYE MIX'):
                    url = host + 'HasBahCa_Turkey_TURKiYE_MIX_KARISIK.m3u'
                    self.session.open(HasBahCa1, sel, url)
        elif sel == ('IPTV TURKEY TURKIYE MUZIK'):
                    url = host + 'HasBahCa_Turkey_TURKiYE_MUZIK.m3u'
                    self.session.open(HasBahCa1, sel, url)
        elif sel == ('IPTV TURKEY TURKIYE RADYO'):
                    url = host + 'HasBahCa_Turkey_TURKiYE_RADYO.m3u'
                    self.session.open(HasBahCa1, sel, url)
        elif sel == ('IPTV TURKEY TURKIYE SPOR'):
                    url = host + 'HasBahCa_Turkey_TURKiYE_SPOR.m3u'
                    self.session.open(HasBahCa1, sel, url)
        elif sel == ('IPTV TURKEY TURKIYE YEREL'):
                    url = host + 'HasBahCa_Turkey_TURKiYE_YEREL.m3u'
                    self.session.open(HasBahCa1, sel, url)
        elif sel == ('IPTV TURKI STAATEN'):
                    url = host + 'HasBahCa_TURKI_ULKELER.m3u'
                    self.session.open(HasBahCa1, sel, url)
        elif sel == ('IPTV USA CHINA ENGLISH'):
                    url = host + 'HasBahCa_USA_CHINA_ENGLISH.m3u'
                    self.session.open(HasBahCa1, sel, url)
        elif sel == ('IPTV WORLD MIXTV'):
                    url = host + 'HasBahCa_WORLD_MIXTV.m3u'
                    self.session.open(HasBahCa1, sel, url)
        elif sel == ('IPTV WORLD MUSIC'):
                    url = host + 'HasBahCa_WORLD_Music_MUZIKTV.m3u'
                    self.session.open(HasBahCa1, sel, url)
        elif sel == ('IPTV WORLD SPORTS'):
                    url = host + 'HasBahCa_WORLD_Sports_SPOR.m3u'
                    self.session.open(HasBahCa1, sel, url)
        elif sel == ('WEBCAM CHINA CIN'):
                    url = host + 'HasBahCa_WEBCAM_China_CiN.m3u'
                    self.session.open(HasBahCa1, sel, url)
        elif sel == ('WEBCAM DE AU CH'):
                    url = host + 'HasBahCa_WEBCAM_DE_AU_CH.m3u'
                    self.session.open(HasBahCa1, sel, url)
        elif sel == ('WEBCAM MIX'):
                    url = host + 'HasBahCa_WEBCAM_MIX.m3u'
                    self.session.open(HasBahCa1, sel, url)
        elif sel == ('WEBCAM POLSKI'):
                    url = host + 'HasBahCa_webcam_POLSKI.m3u'
                    self.session.open(HasBahCa1, sel, url)
        elif sel == ('WEBCAM PORTUGAL'):
                    url = host + 'HasBahCa_WEBCAM_Portugal.m3u'
                    self.session.open(HasBahCa1, sel, url)
        elif sel == ('WEBCAM RUS EX CCCP'):
                    url = host + 'HasBahCa_WEBCAM_RUS_EX_CCCP.m3u'
                    self.session.open(HasBahCa1, sel, url)
        elif sel == ('WEBCAM RUS EX CCCP SOCHICAM'):
                    url = host + 'HasBahCa_webcam_rus_exCCCP_SOCHICAM_FHD.m3u'
                    self.session.open(HasBahCa1, sel, url)
        elif sel == ('WEBCAM TURKEY'):
                    url = host + 'HasBahCa_Turkey_WEBCAM.m3u'
                    self.session.open(HasBahCa1, sel, url)
        elif sel == ('WEBCAM USA'):
                    url = host + 'HasBahCa_WEBCAM_USA.m3u'
                    self.session.open(HasBahCa1, sel, url)

        else:
            return
        return

class HasBahCa(Screen):
    def __init__(self, session, name, url):
        self.session = session
        skin = path_skin + 'settings.xml'
        with open(skin, 'r') as f:
            self.skin = f.read()
        Screen.__init__(self, session)
        self.setup_title = ('HasBahCa TV')
        self.list = []
        self.name = name
        self.url = url
        self['title'] = Label(name)
        self['text'] = hasList([])
        self['info'] = Label(_('Loading data... Please wait'))
        self['key_red'] = Button(_('Back'))
        self['key_green'] = Button(_('Select'))
        self['key_yellow'] = Button(_(''))
        self["key_blue"] = Button(_(''))
        self['key_green'].hide()
        self['key_yellow'].hide()
        self['key_blue'].hide()
        self['live'] = Label('')
        self['live'].setText('')
        self['actions'] = ActionMap(['SetupActions', 'ColorActions'], {
            'ok': self.okRun,
            'green': self.okRun,
            'red': self.close,
            # 'yellow': self.convert,
            'cancel': self.close}, -2)
        self.timer = eTimer()
        if DreamOS():
            self.timer_conn = self.timer.timeout.connect(self._gotPageLoad)
        else:
            self.timer.callback.append(self._gotPageLoad)
        self.timer.start(500, True)
        self.onLayoutFinish.append(self.__layoutFinished)

    def __layoutFinished(self):
        self.setTitle(self.setup_title)

    def _gotPageLoad(self):
        self.names = []
        self.urls = []
        url = self.url
        items = []
        try:
            content = getUrl(url)
            if six.PY3:
                content = six.ensure_str(content)
            print("HasBahCa t content =", content)
            # https://raw.githubusercontent.com/HasBahCa/IPTV-LIST/main/HasBahCa_03INT_MIXTV.m3u
            # href="/HasBahCa/IPTV-LIST/blob/main/HasBahCa_AFRICA_ISRAEL_israil.m3u">HasBahCa_AFRICA_ISRAEL_israil.m3u</a>
            # <div class="sr-only" role="row">
            # <div id="readme
            # n1 = content.find('<div class="sr-only" role="row">', 0)
            n1 = content.find('js-permalink-shortcut"', 0)
            n2 = content.find('<div id="readme', n1)
            content2 = content[n1:n2]
            regexvideo = 'title="(.*?).m3u.*?href="/HasBahCa/IPTV-LIST/blob/main/(.*?).m3u">.*?wrap">(.*?)</time'
            match = re.compile(regexvideo, re.DOTALL).findall(content2)
            print("HasBahCa t match =", match)
            for name, url, date in match:
                if 'readme' in name.lower():
                    continue
                print("HasBahCa t name =", name)
                print("HasBahCa t url =", url)
                print("HasBahCa t date =", date)
                url1 = 'https://raw.githubusercontent.com/HasBahCa/IPTV-LIST/main/' + url + '.m3u'
                date = date.replace(',', ' ')
                name1 = name.replace('.m3u', '').replace('-', ' ').replace('_', ' ')
                name = name1 + ' | ' + date
                print("******** name 1 ******* %s" % name)
                name = decodeHtml(name)
                print("HasBahCa t name =", name)
                print("HasBahCa t url1 =", url1)

                item = name + "###" + url1
                print('Webcam4 Items sort: ', item)
                items.append(item)
            items.sort()
            for item in items:
                name = item.split('###')[0]
                url = item.split('###')[1]

                self.names.append(name)
                self.urls.append(url)
            self["live"].setText('N.' + str(len(self.names)) + " CATEGORY")
            self['info'].setText(_('Please select ...'))
            self['key_green'].show()
            showlisthasba(self.names, self['text'])
            print('-------------HasBahCa-------------')

        except Exception as e:
            print('error ', str(e))

    def okRun(self):
        idx = self["text"].getSelectionIndex()
        name = self.names[idx]
        url = self.urls[idx]
        self.session.open(HasBahCa1, name, url)

class HasBahCa1(Screen):
    def __init__(self, session, sel, url):
        self.session = session
        skin = path_skin + 'settings.xml'
        with open(skin, 'r') as f:
            self.skin = f.read()
        Screen.__init__(self, session)
        self.setup_title = ('HasBahCa')
        self.list = []
        self.name = sel
        self.url = url
        self.type = None
        self['title'] = Label(sel)
        self['text'] = hasList([])
        self['info'] = Label(_('Loading data... Please wait'))
        self['key_red'] = Button(_('Back'))
        self['key_green'] = Button(_('Select'))
        self['key_yellow'] = Button('Convert')
        self["key_blue"] = Button('Remove')
        self['key_green'].hide()
        self['key_yellow'].hide()
        self['key_blue'].hide()
        self['live'] = Label('')
        self['live'].setText('')
        self['progress'] = ProgressBar()
        self['progresstext'] = StaticText()
        self["progress"].hide()
        self['actions'] = ActionMap(['SetupActions', 'ColorActions'], {
            'ok': self.okRun,
            'green': self.okRun,
            'red': self.close,
            'yellow': self.convert,
            'blue': self.msgdeleteBouquets,
            'cancel': self.close}, -2)
        self.timer = eTimer()
        if DreamOS():
            self.timer_conn = self.timer.timeout.connect(self._gotPageLoad)
        else:
            self.timer.callback.append(self._gotPageLoad)
        self.timer.start(100, True)
        self.onLayoutFinish.append(self.__layoutFinished)

    def __layoutFinished(self):
        self.setTitle(self.setup_title)

    def _gotPageLoad(self):
        url = self.url
        # name = self.name
        self.names = []
        self.urls = []
        items = []
        try:
            content = getUrl(url)
            if six.PY3:
                content = six.ensure_str(content)
            # #EXTINF:-1 group-title="|RADIO|TOP Radio" $ExtFilter="RADIO",WBWB FM - 56 kbit/s
            #filmon
            # #EXTM3U
            # EXTINF:-1 group-title="FILMon TV",A Família Buscapé - The Beverly Hillbillies | Filmon EUA
            # https://nowontv.info/filmon.php?url=https://www.filmon.com/api-v2/channel/2969&pprotocol=hls
            regexvideo = 'EXTINF.*?,(.*?)\\n(.*?)\\n'
            # regexvideo = 'EXTINF.*?group-title="(.*?)".*?,(.*?)\\n(.*?)\\n'
            match = re.compile(regexvideo, re.DOTALL).findall(content)
            for name, url in match:
            # for group, name, url in match:
                # name = name.replace('_', ' ').replace('-', ' ')
                # name1 = group + ' | ' + name

                name1 = name.replace('_', ' ').replace('-', ' ')
                # print("******** name 2 ******* %s" % name1)
                # name1 = name1.replace('United States Amerika', '').replace('+', ' ').replace('HasBhaCa', '')
                # name1 = name1.replace('AVUSTURALYA', '').replace('Arjantin', '').replace('MK', '')
                name = decodeHtml(name1)
                item = name + "###" + url
                print('Items sort: ', item)
                items.append(item)
            items.sort()
            for item in items:
                name = item.split('###')[0]
                url = item.split('###')[1]
                self.names.append(name)
                self.urls.append(url)
            self["live"].setText('N.' + str(len(self.names)) + " STREAM")
            self['info'].setText(_('Please select ...'))
            self['key_green'].show()
            self['key_yellow'].show()
            self['key_blue'].show()
            showlisthasba(self.names, self['text'])
            # MemClean()
        except Exception as e:
            print('error HasBahCa', str(e))

    def okRun(self):
        idx = self["text"].getSelectionIndex()
        name = self.names[idx]
        url = self.urls[idx]
        self.session.open(Playgo, name, url)

    def convert(self):
        self.session.openWithCallback(self.convert2, MessageBox, _("Do you want to Convert %s to Favorite Bouquet ?\n\nAttention!! Wait while converting !!!") % self.name, MessageBox.TYPE_YESNO, timeout=5, default=True)

    def convert2(self, result):
        if result:
            self.type = 'tv'
            if "webcam" in self.name.lower():
                self.type = "tv"
            elif "radio" in self.name.lower():
                self.type = "radio"
            else:
                self.type = "tv"
            # #EXTINF:-1 group-title="|RADIO|TOP Radio" $ExtFilter="RADIO",WBWB FM - 56 kbit/s
            name_file = self.name.replace('/', '_').replace(',', '').replace('hasbahca', 'hbc')
            cleanName = re.sub(r'[\<\>\:\"\/\\\|\?\*]', '_', str(name_file))
            cleanName = re.sub(r' ', '_', cleanName)
            cleanName = re.sub(r'\d+:\d+:[\d.]+', '_', cleanName)
            name_file = re.sub(r'_+', '_', cleanName)
            bouquetname = 'userbouquet.hbc_%s.%s' % (name_file.lower(), self.type.lower())
            # nline = '#SERVICE: 1:7:1:0:0:0:0:0:0:0:FROM BOUQUET "%s" ORDER BY bouquet\n' % bouquetname
            self.tmpx = ''
            self.namel = ''

            tmplist = []
            # tmplist.append('#NAME HasBahCa IPTV %s (%s)' % (name_file,self.type))
            tmplist.append('#NAME HASBAHCA IPTV %s' % name_file)
            tmplist.append('#SERVICE 1:64:0:0:0:0:0:0:0:0::%s CHANNELS' % name_file)
            tmplist.append('#DESCRIPTION --- %s ---' % name_file)
            print("Converting Bouquet %s" % name_file)

            self.file = "/tmp/%s.m3u" % name_file
            try:
                downloadFile(self.url, self.file)
            except Exceptions as e:
                print('Error download self m3u: ', str(e))
            '''
            # self.download_m3u()
            # os.system('sleep 3')
            '''

            '''
            # with open(file, 'wb') as f:
                # content = getUrl(self.url)
                # if six.PY3:
                    # content = six.ensure_str(content)
                # print('Resp 1: ', content)
                # f.write(content)
                # os.system('sleep 3')
                # f.close()
            # # self.download_m3u()
            # print('Error download : ', str(e))
            '''
            if os.path.isfile(self.file) and os.stat(self.file).st_size > 0:

                for line in open(self.file):
                    # print('line: ', line)
                    if line.startswith('#EXTM3U'):
                        continue
                    if '#EXTM3U $BorpasFileFormat="1"' in line: #force export bouquet ???
                        continue
                    if line == '':
                        continue
                    if line == ' ':
                        continue
                    if line.startswith("#EXTINF"):
                        # print('line startswith #EXTINF:')
                        line = '%s' % line.split(',')[-1]
                        line = line.rstrip()
                        namel = '%s' % line.split(',')[-1]
                        self.namel = namel.rstrip()
                        self.tmpx = '#DESCRIPTION %s\r' % line

                    else:
                        if self.type.upper() == 'TV':
                            line = line.replace(':', '%3a')
                            line = line.rstrip()

                            if line.startswith('rtmp') or line.startswith('rtsp') or line.startswith('mms'):
                                line = '#SERVICE 4097:0:1:0:0:0:0:0:0:0:%s:%s' % (line, self.namel)

                            if not line.startswith("#SERVICE 4097:0:1:0:0:0:0:0:0:0:rt"):
                                if line.startswith('http%3a'):
                                    line = '#SERVICE 4097:0:1:0:0:0:0:0:0:0:%s:%s' % (line, self.namel)
                                if line.startswith('https%3a'):
                                    line = '#SERVICE 4097:0:1:0:0:0:0:0:0:0:%s:%s' % (line, self.namel)
                                # print('line TV')
                            tmplist.append(line)
                            tmplist.append(self.tmpx)

                        elif self.type.upper() == 'RADIO':
                            line = line.replace(':', '%3a')
                            line = line.rstrip()
                            if line.startswith('rtmp') or line.startswith('rtsp') or line.startswith('mms'):
                                line = '#SERVICE 4097:0:2:0:0:0:0:0:0:0:%s:%s' % (line, self.namel)
                            if not line.startswith("#SERVICE 4097:0:2:0:0:0:0:0:0:0:rt"):
                                if line.startswith('http%3a'):
                                    line = '#SERVICE 4097:0:2:0:0:0:0:0:0:0:%s:%s' % (line, self.namel)
                                if line.startswith('https%3a'):
                                    line = '#SERVICE 4097:0:2:0:0:0:0:0:0:0:%s:%s' % (line, self.namel)
                            tmplist.append(line)
                            tmplist.append(self.tmpx)
                        else:
                            print("UNKNOWN TYPE: %s" % self.type)

                """
                in_bouquets = 0
                f = open('/etc/enigma2/' + bouquetname, 'w')
                for item in tmplist:
                    f.write("%s\n" % item)
                f.close()
                # write bouquet file
                self.mbox = self.session.open(MessageBox, _('Check out the favorites list ...'), MessageBox.TYPE_INFO, timeout=5)
                if os.path.isfile('/etc/enigma2/bouquets.tv'):
                    # check if bouquet exists in bouquet file
                    for line in open('/etc/enigma2/bouquets.%s' % self.type.lower()):
                        if bouquetname in line:
                            in_bouquets = 1
                    if in_bouquets == 0:
                        path1 = 'etc/enigma2/' + str(bouquetname)
                        path2 = '/etc/enigma2/bouquets.' + str(self.type.lower())
                        path3 = '/etc/enigma2/bouquets.' + str(self.type.lower() + '.bak')
                        if os.path.isfile(path1) and os.path.isfile(path2):
                            remove_line(path2, bouquetname)
                        os.rename(path2, path3)
                        tvfile = open(path2, 'w+')
                        bakfile = open(path3)
                        for line in bakfile:
                            tvfile.write(line)
                        tvfile.write('#SERVICE 1:7:1:0:0:0:0:0:0:0:FROM BOUQUET "%s" ORDER BY bouquet\r\n' % bouquetname)
                        bakfile.close()
                        tvfile.close()
                        in_bouquets = 1
                self.mbox = self.session.open(MessageBox, _('Shuffle Favorite List in Progress') + '\n' + _('Wait please ...'), MessageBox.TYPE_INFO, timeout=5)
                ReloadBouquets()
                """

                path1 = '/etc/enigma2/' + str(bouquetname)
                path2 = '/etc/enigma2/bouquets.' + str(self.type.lower())

                # create userbouquet
                with open(path1, 'w+') as f:
                    for item in tmplist:
                        f.write("%s\n" % item)

                # write bouquet.tv file
                in_bouquets = 0
                for line in open('/etc/enigma2/bouquets.%s' % self.type.lower()):
                    if bouquetname in line:
                        in_bouquets = 1
                        break

                if in_bouquets == 0:
                    '''
                    Rename unlinked bouquet file /etc/enigma2/userbouquet.webcam.tv to /etc/enigma2/userbouquet.webcam.tv.del
                    '''
                    with open(path2, 'a+') as f:
                        bouquetTvString = '#SERVICE 1:7:1:0:0:0:0:0:0:0:FROM BOUQUET "' + str(bouquetname) + '" ORDER BY bouquet\n'
                        f.write(str(bouquetTvString))
                    self.mbox = self.session.open(MessageBox, _('Shuffle Favorite List in Progress') + '\n' + _('Wait please ...'), MessageBox.TYPE_INFO, timeout=5)
                ReloadBouquets()

            else:
                self.mbox = self.session.open(MessageBox, _('Download Error'), MessageBox.TYPE_INFO, timeout=5)


    '''add for future'''
    def download_m3u(self):
        try:
                self.download = downloadWithProgress(self.url, self.file)
                self.download.addProgress(self.downloadProgress)
                self.download.start().addCallback(self.check).addErrback(self.showError)
        except:
                self.session.open(MessageBox, _('Download Failed!!!'), MessageBox.TYPE_INFO, timeout=5)
                pass

    def downloadProgress(self, recvbytes, totalbytes):
        self["progress"].show()
        self['progress'].value = int(100 * recvbytes / float(totalbytes))
        self['progresstext'].text = '%d of %d kBytes (%.2f%%)' % (recvbytes / 1024, totalbytes / 1024, 100 * recvbytes / float(totalbytes))

    def check(self, fplug):
        if os.path.exists(self.file):
            self['progresstext'].text = ''
            self.progclear = 0
            self['progress'].setValue(self.progclear)
            self["progress"].hide()

    def showError(self, error):
        self.session.open(MessageBox, _('Download Failed!!!'), MessageBox.TYPE_INFO, timeout=5)


# remove bouquet  'hbc'
    def msgdeleteBouquets(self):
        self.session.openWithCallback(self.deleteBouquets, MessageBox, _("Remove all HasBahCa Favorite Bouquet ?") , MessageBox.TYPE_YESNO, timeout=5, default=True)

    def deleteBouquets(self, result):
        """
        Clean up routine to remove any previously made changes
        """
        if result:

            try:
                for fname in os.listdir(enigma_path):
                    if 'userbouquet.hbc_' in fname:
                        # os.remove(os.path.join(enigma_path, fname))
                        purge(enigma_path, fname)
                    elif 'bouquets.tv.bak' in fname:
                        # os.remove(os.path.join(enigma_path, fname))
                        purge(enigma_path, fname)
                """
                # if os.path.isdir(epgimport_path):
                    # for fname in os.listdir(epgimport_path):
                        # if 'hbc_' in fname:
                            # os.remove(os.path.join(epgimport_path, fname))
                            """
                os.rename(os.path.join(enigma_path, 'bouquets.tv'), os.path.join(enigma_path, 'bouquets.tv.bak'))
                tvfile = open(os.path.join(enigma_path, 'bouquets.tv'), 'w+')
                bakfile = open(os.path.join(enigma_path, 'bouquets.tv.bak'))
                for line in bakfile:
                    if '.hbc_' not in line:
                        tvfile.write(line)
                bakfile.close()
                tvfile.close()
                self.mbox = self.session.open(MessageBox, _('HasBahCa Favorites List have been removed'), MessageBox.TYPE_INFO, timeout=5)
                ReloadBouquets()
            except Exception as ex:
                print(str(ex))
                raise


class TvInfoBarShowHide():
    """ InfoBar show/hide control, accepts toggleShow and hide actions, might start
    fancy animations. """
    STATE_HIDDEN = 0
    STATE_HIDING = 1
    STATE_SHOWING = 2
    STATE_SHOWN = 3
    skipToggleShow = False

    def __init__(self):
        self["ShowHideActions"] = ActionMap(["InfobarShowHideActions"], {
            "toggleShow": self.OkPressed,
            "hide": self.hide
        }, 0)
        self.__event_tracker = ServiceEventTracker(screen=self, eventmap={iPlayableService.evStart: self.serviceStarted})
        self.__state = self.STATE_SHOWN
        self.__locked = 0
        self.hideTimer = eTimer()
        try:
            self.hideTimer_conn = self.hideTimer.timeout.connect(self.doTimerHide)
        except:
            self.hideTimer.callback.append(self.doTimerHide)
        self.hideTimer.start(5000, True)
        self.onShow.append(self.__onShow)
        self.onHide.append(self.__onHide)

    def OkPressed(self):
        self.toggleShow()

    def toggleShow(self):
        if self.skipToggleShow:
            self.skipToggleShow = False
            return
        if self.__state == self.STATE_HIDDEN:
            self.show()
            self.hideTimer.stop()
        else:
            self.hide()
            self.startHideTimer()

    def serviceStarted(self):
        if self.execing:
            if config.usage.show_infobar_on_zap.value:
                self.doShow()

    def __onShow(self):
        self.__state = self.STATE_SHOWN
        self.startHideTimer()

    def startHideTimer(self):
        if self.__state == self.STATE_SHOWN and not self.__locked:
            self.hideTimer.stop()
            idx = config.usage.infobar_timeout.index
            if idx:
                self.hideTimer.start(idx * 1500, True)

    def __onHide(self):
        self.__state = self.STATE_HIDDEN

    def doShow(self):
        self.hideTimer.stop()
        self.show()
        self.startHideTimer()

    def doTimerHide(self):
        self.hideTimer.stop()
        if self.__state == self.STATE_SHOWN:
            self.hide()

    def lockShow(self):
        try:
            self.__locked += 1
        except:
            self.__locked = 0
        if self.execing:
            self.show()
            self.hideTimer.stop()
            self.skipToggleShow = False

    def unlockShow(self):
        try:
            self.__locked -= 1
        except:
            self.__locked = 0
        if self.__locked < 0:
            self.__locked = 0
        if self.execing:
            self.startHideTimer()

    def debug(obj, text=""):
        print(text + " %s\n" % obj)


class Playgo(InfoBarBase, TvInfoBarShowHide, InfoBarSeek, InfoBarAudioSelection, InfoBarSubtitleSupport, Screen):
    STATE_IDLE = 0
    STATE_PLAYING = 1
    STATE_PAUSED = 2
    ENABLE_RESUME_SUPPORT = True
    ALLOW_SUSPEND = True
    screen_timeout = 3000

    def __init__(self, session, name, url):
        global streaml
        Screen.__init__(self, session)
        global _session
        _session = session
        self.session = session
        self.skinName = 'MoviePlayer'
        # title = name
        streaml = False
        self.allowPiP = False
        self.service = None
        # service = None
        self.url = url
        self.pcip = 'None'
        print("******** name 3 ******* %s" % name)
        self.name = decodeHtml(name)
        self.state = self.STATE_PLAYING
        self.srefInit = self.session.nav.getCurrentlyPlayingServiceReference()
        InfoBarBase.__init__(self, steal_current_service=True)
        TvInfoBarShowHide.__init__(self)
        InfoBarSeek.__init__(self, actionmap="InfobarSeekActions")
        InfoBarAudioSelection.__init__(self)
        InfoBarSubtitleSupport.__init__(self)
        # SubsSupport.__init__(self, searchSupport=True, embeddedSupport=True)
        # SubsSupportStatus.__init__(self)
        try:
            self.init_aspect = int(self.getAspect())
        except:
            self.init_aspect = 0
        self.new_aspect = self.init_aspect

        self['actions'] = ActionMap([
            'MoviePlayerActions',
            'MovieSelectionActions',
            'MediaPlayerActions',
            'EPGSelectActions',
            'MediaPlayerSeekActions',
            'SetupActions',
            'ColorActions',
            'InfobarShowHideActions',
            'InfobarActions',
            'InfobarSeekActions'
        ], {
            # 'stop': self.cancel,
            'epg': self.showIMDB,
            'info': self.showinfo,
            # 'info': self.cicleStreamType,
            'tv': self.cicleStreamType,
            'stop': self.leavePlayer,
            'cancel': self.cancel,
            'back': self.cancel
        }, -1)

        if '8088' in str(self.url):
            # self.onLayoutFinish.append(self.slinkPlay)
            self.onFirstExecBegin.append(self.slinkPlay)
        else:
            # self.onLayoutFinish.append(self.cicleStreamType)
            self.onFirstExecBegin.append(self.cicleStreamType)
        self.onClose.append(self.cancel)

    def getAspect(self):
        return AVSwitch().getAspectRatioSetting()

    def getAspectString(self, aspectnum):
        return {
            0: _('4:3 Letterbox'),
            1: _('4:3 PanScan'),
            2: _('16:9'),
            3: _('16:9 always'),
            4: _('16:10 Letterbox'),
            5: _('16:10 PanScan'),
            6: _('16:9 Letterbox')
        }[aspectnum]

    def setAspect(self, aspect):
        map = {
            0: '4_3_letterbox',
            1: '4_3_panscan',
            2: '16_9',
            3: '16_9_always',
            4: '16_10_letterbox',
            5: '16_10_panscan',
            6: '16_9_letterbox'
        }
        config.av.aspectratio.setValue(map[aspect])
        try:
            AVSwitch().setAspectRatio(aspect)
        except:
            pass

    def av(self):
        temp = int(self.getAspect())
        temp = temp + 1
        if temp > 6:
            temp = 0
        self.new_aspect = temp
        self.setAspect(temp)

    def showinfo(self):
        # debug = True
        sTitle = ''
        sServiceref = ''
        try:
            servicename, serviceurl = getserviceinfo(sref)
            if servicename is not None:
                sTitle = servicename
            else:
                sTitle = ''
            if serviceurl is not None:
                sServiceref = serviceurl
            else:
                sServiceref = ''
            currPlay = self.session.nav.getCurrentService()
            sTagCodec = currPlay.info().getInfoString(iServiceInformation.sTagCodec)
            sTagVideoCodec = currPlay.info().getInfoString(iServiceInformation.sTagVideoCodec)
            sTagAudioCodec = currPlay.info().getInfoString(iServiceInformation.sTagAudioCodec)
            message = 'stitle:' + str(sTitle) + '\n' + 'sServiceref:' + str(sServiceref) + '\n' + 'sTagCodec:' + str(sTagCodec) + '\n' + 'sTagVideoCodec:' + str(sTagVideoCodec) + '\n' + 'sTagAudioCodec : ' + str(sTagAudioCodec)
            self.mbox = self.session.open(MessageBox, message, MessageBox.TYPE_INFO)
        except:
            pass
        return

    def showIMDB(self):
        TMDB = resolveFilename(SCOPE_PLUGINS, "Extensions/{}".format('TMDB'))
        IMDb = resolveFilename(SCOPE_PLUGINS, "Extensions/{}".format('IMDb'))
        if os.path.exists(TMDB):
            from Plugins.Extensions.TMBD.plugin import TMBD
            text_clear = self.name
            text = charRemove(text_clear)
            self.session.open(TMBD, text, False)
        elif os.path.exists(IMDb):
            from Plugins.Extensions.IMDb.plugin import IMDB
            text_clear = self.name
            text = charRemove(text_clear)
            HHHHH = text
            self.session.open(IMDB, HHHHH)
        else:
            text_clear = self.name
            self.session.open(MessageBox, text_clear, MessageBox.TYPE_INFO)

    def slinkPlay(self, url):
        name = self.name
        ref = "{0}:{1}".format(url.replace(":", "%3a"), name.replace(":", "%3a"))
        print('final reference:   ', ref)
        sref = eServiceReference(ref)
        sref.setName(name)
        self.session.nav.stopService()
        self.session.nav.playService(sref)

    def openTest(self, servicetype, url):
        name = self.name
        ref = "{0}:0:1:0:0:0:0:0:0:0:{1}:{2}".format(servicetype, url.replace(":", "%3a"), name.replace(":", "%3a"))
        print('reference:   ', ref)

        if streaml is True:
            url = 'http://127.0.0.1:8088/' + str(url)
            ref = "{0}:0:1:0:0:0:0:0:0:0:{1}:{2}".format(servicetype, url.replace(":", "%3a"), name.replace(":", "%3a"))
            print('streaml reference:   ', ref)

        print('final reference:   ', ref)
        sref = eServiceReference(ref)
        sref.setName(name)
        self.session.nav.stopService()
        self.session.nav.playService(sref)

    def cicleStreamType(self):
        global streml
        # streaml = False
        # from itertools import cycle, islice
        self.servicetype = '4097'
        print('servicetype1: ', self.servicetype)
        url = str(self.url)
        if str(os.path.splitext(self.url)[-1]) == ".m3u8":
            if self.servicetype == "1":
                self.servicetype = "4097"
        # currentindex = 0
        # streamtypelist = ["4097"]
        # # if "youtube" in str(self.url):
            # # self.mbox = self.session.open(MessageBox, _('For Stream Youtube coming soon!'), MessageBox.TYPE_INFO, timeout=5)
            # # return
        # if isStreamlinkAvailable():
            # streamtypelist.append("5002") #ref = '5002:0:1:0:0:0:0:0:0:0:http%3a//127.0.0.1%3a8088/' + url
            # streaml = True
        # if os.path.exists("/usr/bin/gstplayer"):
            # streamtypelist.append("5001")
        # if os.path.exists("/usr/bin/exteplayer3"):
            # streamtypelist.append("5002")
        # if os.path.exists("/usr/bin/apt-get"):
            # streamtypelist.append("8193")
        # for index, item in enumerate(streamtypelist, start=0):
            # if str(item) == str(self.servicetype):
                # currentindex = index
                # break
        # nextStreamType = islice(cycle(streamtypelist), currentindex + 1, None)
        # self.servicetype = str(next(nextStreamType))
        print('servicetype2: ', self.servicetype)
        self.openTest(self.servicetype, url)

    def up(self):
        pass

    def down(self):
        self.up()

    def doEofInternal(self, playing):
        self.close()

    def __evEOF(self):
        self.end = True

    def showVideoInfo(self):
        if self.shown:
            self.hideInfobar()
        if self.infoCallback is not None:
            self.infoCallback()
        return

    def showAfterSeek(self):
        if isinstance(self, TvInfoBarShowHide):
            self.doShow()

    def cancel(self):
        if os.path.isfile('/tmp/hls.avi'):
            os.remove('/tmp/hls.avi')
        self.session.nav.stopService()
        self.session.nav.playService(self.srefInit)
        if not self.new_aspect == self.init_aspect:
            try:
                self.setAspect(self.init_aspect)
            except:
                pass
        # streaml = False
        self.close()

    def leavePlayer(self):
        self.close()


def checks():
    from Plugins.Extensions.HasBahCa.Utils import checkInternet
    checkInternet()
    chekin = False
    if checkInternet():
        chekin = True
    return chekin


def main(session, **kwargs):
    if checks:
        try:
            from Plugins.Extensions.HasBahCa.Update import upd_done
            upd_done()
        except:
            pass
        session.open(MainHasBahCa)
    else:
        session.open(MessageBox, "No Internet", MessageBox.TYPE_INFO)


def StartSetup(menuid, **kwargs):
    if menuid == 'mainmenu':
        return [(_('HasBahCa  IPTV'), main, 'HasBahCa  IPTV', 15)]
    else:
        return []


def Plugins(**kwargs):
    ico_path = 'logo.png'
    if not os.path.exists('/var/lib/dpkg/status'):
        ico_path = plugin_path + '/res/pics/logo.png'
    extensions_menu = PluginDescriptor(name=title_plug, description=desc_plugin, where=PluginDescriptor.WHERE_EXTENSIONSMENU, fnc=main, needsRestart=True)
    result = [PluginDescriptor(name=title_plug, description=desc_plugin, where=PluginDescriptor.WHERE_PLUGINMENU, icon=ico_path, fnc=main)]
    result.append(extensions_menu)
    return result
