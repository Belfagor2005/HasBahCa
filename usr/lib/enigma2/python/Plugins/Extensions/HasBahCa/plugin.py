#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
****************************************
*        coded by Lululla              *
*             skin by MMark            *
*             12/03/2022               *
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
from Components.Pixmap import Pixmap
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
from enigma import *
from enigma import RT_HALIGN_CENTER, RT_VALIGN_CENTER
from enigma import RT_HALIGN_LEFT, RT_HALIGN_RIGHT
from enigma import eListbox, eTimer
from enigma import eListboxPythonMultiContent, eConsoleAppContainer
# from enigma import eServiceCenter
from enigma import eServiceReference
from enigma import iPlayableService
from enigma import gFont
from enigma import iServiceInformation
from enigma import loadPNG
# import base64
import glob
import os
import re
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

try:
    from httplib import HTTPConnection, CannotSendRequest, BadStatusLine, HTTPException
    from urllib2 import urlopen, Request, URLError, HTTPError
    from urlparse import urlparse, parse_qs
    from urllib import urlencode
    import httplib
    import six
except:
    from http.client import HTTPConnection, CannotSendRequest, BadStatusLine, HTTPException
    from urllib.error import URLError, HTTPError
    from urllib.request import urlopen, Request
    from urllib.parse import urlparse
    from urllib.parse import parse_qs, urlencode
    unicode = str; unichr = chr; long = int
    from importlib import reload
    PY3 = True

   
    
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
currversion = '1.3'
title_plug = 'HasBahCa '
desc_plugin = ('..:: HasBahCa by Lululla %s ::.. ' % currversion)
plugin_path = resolveFilename(SCOPE_PLUGINS, "Extensions/{}".format('HasBahCa'))
pluglogo = resolveFilename(SCOPE_PLUGINS, "Extensions/{}/res/pics/logo.png".format('HasBahCa'))
png = resolveFilename(SCOPE_PLUGINS, "Extensions/{}/res/pics/tv.png".format('HasBahCa'))
github = 'https://raw.githubusercontent.com/HasBahCa/m3u_Links/main/'

enigma_path = '/etc/enigma2'
if isFHD():
    path_skin = resolveFilename(SCOPE_PLUGINS, "Extensions/{}/res/skins/fhd/".format('HasBahCa'))
else:
    path_skin = resolveFilename(SCOPE_PLUGINS, "Extensions/{}/res/skins/hd/".format('HasBahCa'))
if DreamOS():
    path_skin = path_skin + 'dreamOs/'
print('HasBahCa path_skin: ', path_skin)

Panel_Dlist = [
    ('ALL IPTV'),
    ('ALL MOVIE'),
    ('ALL MUSIC'),
    ('ALL RADIO'),
    ('ALL RELAX'),
    ('ALL SPORT'),
    ('ALL WEBCAM'),
    ('~~~~~~~~~~~'),
    ('MOVIES AZ TR RUS'),
    ('MOVIES AZ TR RUS NEW'),
    ('MOVIES LATINO'),    
    ('MOVIES RUS CARTOONS'),
    ('MOVIES RUS COMEDY'),
    ('MOVIES RUS MIX'),
    ('~~~~~~~~~~~'),
    ('WEBCAM CHINA CIN'),
    ('WEBCAM DE AU CH'),
    ('WEBCAM MIX'),
    ('WEBCAM POLAND'),
    ('WEBCAM PORTUGAL'),
    ('WEBCAM RUS EX CCCP'),
    ('WEBCAM TURK'),
    ('WEBCAM USA'),
    ('~~~~~~~~~~~'),
    ('WORLD NEWS BUSINES'),
    ('WORLD OTHERS'),
    ('WORLD PLUTOTV'),
    ('WORLD TVPLUS'),
    ('~~~~~~~~~~~'),
    ('AFGHANISTAN'),
    ('AFRICA'),
    ('ALBANIA BOSNIA KOSOVO'),
    ('ARABIC 1'),
    ('ARABIC 2'),
    ('ARGENTINA'),
    ('ARGENTINA PLUTO'),
    ('ASIA MIX'),
    ('AUSTRIA'),
    ('AUSTRIA TVPLUS'),
    ('AVUSTURALIA NZELAND'),
    ('BALTIC EST LIT LET'),
    ('BANGLADESH'),
    ('BRASIL'),
    ('BRASIL PLUTO'),
    ('BULGARIA'),
    ('CAMBODIA'),
    ('CANADA'),
    ('CANADA TVPLUS'),
    ('CHILE'),
    ('CHINA1'),
    ('CHINA2'),
    ('COLOMBIA'),
    ('COSTARICA'),
    ('CROATIA'),
    ('CZECH'),
    ('DOMINICANRP'),
    ('ENGLAND'),
    ('ENGLAND PLUTO'),
    ('ENGLAND TVPLUS'),
    ('FRANCE'),
    ('FRANCE PLUTO'),
    ('FRANCE TVPLUS'),
    ('GERMAN'),
    ('GERMAN LOKAL'),
    ('GERMAN PLUTO'),
    ('GERMAN TVPLUS'),
    ('GREEK'),
    ('HAITI'),
    ('HOLLAND BELGIEN'),
    ('HOLLAND PLUTO'),
    ('HONDURAS'),
    ('INDIA TAMIL'),
    ('INDONESIA'),
    ('ISRAEL'),
    ('ITALIA'),
    ('ITALIA PLUTO'),
    ('ITALIA TVPLUS'),
    ('JAPAN'),
    ('KHUSUS MALAZIA'),
    ('KOREA'),
    ('KURDI'),
    ('LAOS'),
    ('LATINO MIX'),
    ('LATINO PLUTO'),
    ('LUXEMBOURG'),
    ('MACEDONIA'),
    ('MAGYAR'),
    ('MALTA'),
    ('MEXICO'),
    ('MEXICO PLUTO'),
    ('PAKISTAN'),
    ('PANAMA'),
    ('PERU'),
    ('POLAND'),
    ('PORTUGAL'),
    ('ROMANIA MOLDOVA'),
    ('RUS ARMENIA'),
    ('RUS EX CCCP1'),
    ('RUS EX CCCP2'),
    ('RUS EX CCCP LOCAL'),
    ('RUS GEORGIA'),
    ('RUS KAZAKHSTAN'),
	('RUS UKRAINE1'),
	('RUS UKRAINE2'),
    ('SERBIA'),
    ('SKANDINAV FINLAND'),
    ('SLOVAKIA SLOVENIA'),
    ('SPAIN'),
    ('SPAIN PLUTO'),
    ('SPAIN TVPLUS'),
    ('SWITZERLAND'),
    ('SWITZERLAND PLUTO'),
    ('SWITZERLAND TVPLUS'),
    ('TAIWAN'),
    ('THAILAND'),    
    ('TURKCE FILMLER'),
    ('TURK 1TAMLISTE'),
    ('TURK AVRUPA'),
    ('TURK BLUTV'),
    ('TURK COCUK'),
    ('TURK DINI'),
    ('TURK HABER'),
    ('TURK KARISIK'),
    ('TURK MUZIK'),
    ('TURK OZEL'),
    ('TURK RADYOLAR'),
    ('TURK ULUSAL'),
    ('TURK YEREL'),
    ('TURKI AZERBAYCAN'),
    ('TURKI KKTC'),
    ('TURKI TURKMENISTAN'),
    ('TURKI ULKELER'),
    ('URUGUAY'),
    ('USA'),
    ('USA CHINA ENGLISH'),
    ('USA LOCAL'),
    ('USA MYTVTO VELLYTV'),
    ('USA PLEX'),
    ('USA PLUTO'),
    ('USA TVPLUS'),
    ('USA XUMO'),
    ('VIETNAM'),
    ('~~~~~~~~~~~'),
    ('ALL CATEGORY'),
    ('~~~~~~~~~~~'), 
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
        if isFHD():
            self.l.setItemHeight(60)
            textfont = int(34)
            self.l.setFont(0, gFont('Regular', textfont))
        else:    
            self.l.setItemHeight(60)
            textfont = int(24)
            self.l.setFont(0, gFont('Regular', textfont))            

def hasListEntry(name, idx):
    res = [name]
    if 'radio' in name.lower():
        png = resolveFilename(SCOPE_PLUGINS, "Extensions/{}/res/pics/radio.png".format('HasBahCa'))
    elif 'radyo' in name.lower():
        png = resolveFilename(SCOPE_PLUGINS, "Extensions/{}/res/pics/radio.png".format('HasBahCa'))
    elif 'webcam' in name.lower():
        png = resolveFilename(SCOPE_PLUGINS, "Extensions/{}/res/pics/webcam.png".format('HasBahCa'))
    elif 'music' in name.lower():
        png = resolveFilename(SCOPE_PLUGINS, "Extensions/{}/res/pics/music.png".format('HasBahCa'))
    elif 'sport' in name.lower():
        png = resolveFilename(SCOPE_PLUGINS, "Extensions/{}/res/pics/sport.png".format('HasBahCa'))
    elif 'relax' in name.lower():
        png = resolveFilename(SCOPE_PLUGINS, "Extensions/{}/res/pics/relax.png".format('HasBahCa')) 
    elif 'movie' in name.lower():
        png = resolveFilename(SCOPE_PLUGINS, "Extensions/{}/res/pics/movie.png".format('HasBahCa'))
    elif 'pluto' in name.lower():
        png = resolveFilename(SCOPE_PLUGINS, "Extensions/{}/res/pics/plutotv.png".format('HasBahCa'))          
    elif 'tvplus' in name.lower():
        png = resolveFilename(SCOPE_PLUGINS, "Extensions/{}/res/pics/tvplus.png".format('HasBahCa'))   
    elif '~~~~' in name.lower():
        png = resolveFilename(SCOPE_PLUGINS, "Extensions/{}/res/pics/mark.png".format('HasBahCa'))         
    else:
        png = resolveFilename(SCOPE_PLUGINS, "Extensions/{}/res/pics/tv.png".format('HasBahCa'))

    if isFHD():
        res.append(MultiContentEntryPixmapAlphaTest(pos=(10, 7), size=(50, 40), png=loadPNG(png)))
        res.append(MultiContentEntryText(pos=(90, 0), size=(1900, 60), font=0, text=name, color=0xa6d1fe, flags=RT_HALIGN_LEFT | RT_VALIGN_CENTER))
    else:
        res.append(MultiContentEntryPixmapAlphaTest(pos=(10, 7), size=(50, 40), png=loadPNG(png)))
        res.append(MultiContentEntryText(pos=(90, 0), size=(1000, 60), font=0, text=name, color=0xa6d1fe, flags=RT_HALIGN_LEFT | RT_VALIGN_CENTER))
    return res

def hasbaSetListEntry(name):
    res = [name]
    if 'radio' in name.lower():
        png = resolveFilename(SCOPE_PLUGINS, "Extensions/{}/res/pics/radio.png".format('HasBahCa'))
    elif 'radyo' in name.lower():
        png = resolveFilename(SCOPE_PLUGINS, "Extensions/{}/res/pics/radio.png".format('HasBahCa'))
    elif 'webcam' in name.lower():
        png = resolveFilename(SCOPE_PLUGINS, "Extensions/{}/res/pics/webcam.png".format('HasBahCa'))
    elif 'music' in name.lower():
        png = resolveFilename(SCOPE_PLUGINS, "Extensions/{}/res/pics/music.png".format('HasBahCa'))
    elif 'sport' in name.lower():
        png = resolveFilename(SCOPE_PLUGINS, "Extensions/{}/res/pics/sport.png".format('HasBahCa'))
    elif 'relax' in name.lower():
        png = resolveFilename(SCOPE_PLUGINS, "Extensions/{}/res/pics/relax.png".format('HasBahCa'))  
    elif 'movie' in name.lower():
        png = resolveFilename(SCOPE_PLUGINS, "Extensions/{}/res/pics/movie.png".format('HasBahCa'))    
    elif 'pluto' in name.lower():
        png = resolveFilename(SCOPE_PLUGINS, "Extensions/{}/res/pics/plutotv.png".format('HasBahCa'))          
    elif 'tvplus' in name.lower():
        png = resolveFilename(SCOPE_PLUGINS, "Extensions/{}/res/pics/tvplus.png".format('HasBahCa'))              
    elif '~~~~' in name.lower():
        png = resolveFilename(SCOPE_PLUGINS, "Extensions/{}/res/pics/mark.png".format('HasBahCa'))         
    else:
        png = resolveFilename(SCOPE_PLUGINS, "Extensions/{}/res/pics/tv.png".format('HasBahCa'))

    if isFHD():
        res.append(MultiContentEntryPixmapAlphaTest(pos=(10, 7), size=(50, 40), png=loadPNG(png)))
        res.append(MultiContentEntryText(pos=(90, 0), size=(1200, 60), font=0, text=name, color=0xa6d1fe, flags=RT_HALIGN_LEFT | RT_VALIGN_CENTER))
    else:
        res.append(MultiContentEntryPixmapAlphaTest(pos=(10, 7), size=(50, 40), png=loadPNG(png)))
        res.append(MultiContentEntryText(pos=(90, 0), size=(1000, 60), font=0, text=name, color=0xa6d1fe, flags=RT_HALIGN_LEFT | RT_VALIGN_CENTER))
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
        Screen.__init__(self, session)
        self.session = session
        skin = path_skin + 'settings.xml'
        with open(skin, 'r') as f:
            self.skin = f.read()
        self.setup_title = ('Main HasBahCa')
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
        self['progress'] = ProgressBar()
        self['progresstext'] = StaticText()
        self["progress"].hide()
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
        self["live"].setText('N.' + str(idx) + " CATEGORY")
        self['text'].setList(list)
        self['info'].setText(_('Please select ...'))
        self['key_green'].show()

    def okRun(self):
        self.keyNumberGlobalCB(self['text'].getSelectedIndex())

    def keyNumberGlobalCB(self, idx):
        sel = self.menu_list[idx]
        host = github
        if sel == ('ALL CATEGORY'):
                url = 'https://github.com/HasBahCa/m3u_Links'
                self.session.open(HasBahCaC, sel, url)
        else:
            if sel == ('ALL IPTV'):
                        pixil = host + 'hasbahca_iptv.m3u'
                        self.session.open(HasBahCa1, sel, pixil)
            elif sel == ('ALL MOVIE'):
                        pixil = host + 'HasBahCa_MOVIES.m3u'
                        self.session.open(HasBahCa1, sel, pixil)
            elif sel == ('ALL MUSIC'):
                        pixil = host + '1MUSIC.m3u'
                        self.session.open(HasBahCa1, sel, pixil)
            elif sel == ('ALL RADIO'):
                        pixil = host + 'HasBahCa_RADIOS.m3u'
                        self.session.open(HasBahCa1, sel, pixil)
            elif sel == ('ALL RELAX'):
                        pixil = host + 'RELAX.m3u'
                        self.session.open(HasBahCa1, sel, pixil)
            elif sel == ('ALL SPORT'):
                        pixil = host + '1SPORT.m3u'
                        self.session.open(HasBahCa1, sel, pixil)
            elif sel == ('ALL WEBCAM'):
                        pixil = host + 'HasBahCa_WEBCAMS.m3u'
                        self.session.open(HasBahCa1, sel, pixil)
            elif sel == ('MOVIES AZ TR RUS'):
                        pixil = host + 'MOVIES_AZ_TR_RUS.m3u'
                        self.session.open(HasBahCa1, sel, pixil)
            elif sel == ('MOVIES AZ TR RUS NEW'):
                        pixil = host + 'MOVIES_AZ_TR_RUS_NEW.m3u'
                        self.session.open(HasBahCa1, sel, pixil)
            elif sel == ('MOVIES LATINO'):
                        pixil = host + 'Latino_MOVIES.m3u'
                        self.session.open(HasBahCa1, sel, pixil)                        
            elif sel == ('MOVIES RUS CARTOONS'):
                        pixil = host + 'MOVIES_RUS_CARTOONS.m3u'
                        self.session.open(HasBahCa1, sel, pixil)
            elif sel == ('MOVIES RUS COMEDY'):
                        pixil = host + 'MOVIES_RUS_COMEDY.m3u'
                        self.session.open(HasBahCa1, sel, pixil)
            elif sel == ('MOVIES RUS MIX'):
                        pixil = host + 'MOVIES_RUS_MIX.m3u'
                        self.session.open(HasBahCa1, sel, pixil)
            elif sel == ('WEBCAM CHINA CIN'):
                        pixil = host + 'WEBCAM_CHINA.m3u'
                        self.session.open(HasBahCa1, sel, pixil)
            elif sel == ('WEBCAM DE AU CH'):
                        pixil = host + 'WEBCAM_DE_AU_CH.m3u'
                        self.session.open(HasBahCa1, sel, pixil)
            elif sel == ('WEBCAM MIX'):
                        pixil = host + 'WEBCAM_MIX.m3u'
                        self.session.open(HasBahCa1, sel, pixil)
            elif sel == ('WEBCAM POLAND'):
                        pixil = host + 'WEBCAM_POLAND.m3u'
                        self.session.open(HasBahCa1, sel, pixil)
            elif sel == ('WEBCAM PORTUGAL'):
                        pixil = host + 'WEBCAM_PORTUGAL.m3u'
                        self.session.open(HasBahCa1, sel, pixil)
            elif sel == ('WEBCAM RUS EX CCCP'):
                        pixil = host + 'WEBCAM_RUS_EXCCCP.m3u'
                        self.session.open(HasBahCa1, sel, pixil)
            elif sel == ('WEBCAM USA'):
                        pixil = host + 'WEBCAM_USA.m3u'
                        self.session.open(HasBahCa1, sel, pixil)
            elif sel == ('WEBCAM TURK'):
                        pixil = host + 'TURK_WEBCAM.m3u'
                        self.session.open(HasBahCa1, sel, pixil)
            elif sel == ('WORLD NEWS BUSINES'):
                        pixil = host + 'World_News_Busines.m3u'
                        self.session.open(HasBahCa1, sel, pixil)
            elif sel == ('WORLD OTHERS'):
                        pixil = host + 'WORLD_OTHERS.m3u'
                        self.session.open(HasBahCa1, sel, pixil)
            elif sel == ('WORLD PLUTOTV'):
                        pixil = host + 'WORLD_PLUTOTV.m3u'
                        self.session.open(HasBahCa1, sel, pixil)
            elif sel == ('WORLD TVPLUS'):
                        pixil = host + 'WORLD_TVPLUS.m3u'
                        self.session.open(HasBahCa1, sel, pixil)

            elif sel == ('AFGHANISTAN'):
                        pixil = host + 'AFGHANISTAN.m3u'
                        self.session.open(HasBahCa1, sel, pixil)
            elif sel == ('AFRICA'):
                        pixil = host + 'AFRICA.m3u'
                        self.session.open(HasBahCa1, sel, pixil)
            elif sel == ('ALBANIA BOSNIA KOSOVO'):
                        pixil = host + 'ALBANIA_BOSNIA_KOSOVO.m3u'
                        self.session.open(HasBahCa1, sel, pixil)
            elif sel == ('ARABIC 1'):
                        pixil = host + 'ARABIC1.m3u'
                        self.session.open(HasBahCa1, sel, pixil)
            elif sel == ('ARABIC 2'):
                        pixil = host + 'ARABIC2.m3u'
                        self.session.open(HasBahCa1, sel, pixil)
            elif sel == ('ARGENTINA'):
                        pixil = host + 'ARGENTINA.m3u'
                        self.session.open(HasBahCa1, sel, pixil)
            elif sel == ('ARGENTINA PLUTO'):
                        pixil = host + 'ARGENTINA_PLUTO.m3u'
                        self.session.open(HasBahCa1, sel, pixil)
            elif sel == ('ASIA MIX'):
                        pixil = host + 'ASIA_MIX.m3u'
                        self.session.open(HasBahCa1, sel, pixil)
            elif sel == ('AUSTRIA'):
                        pixil = host + 'AUSTRIA.m3u'
                        self.session.open(HasBahCa1, sel, pixil)
            elif sel == ('AUSTRIA TVPLUS'):
                        pixil = host + 'AUSTRIA_TVPLUS.m3u'
                        self.session.open(HasBahCa1, sel, pixil)
            elif sel == ('AVUSTURALIA NZELAND'):
                        pixil = host + 'AVUSTURALIA_NZELAND.m3u'
                        self.session.open(HasBahCa1, sel, pixil)
            elif sel == ('BALTIC EST LIT LET'):
                        pixil = host + 'BALTIC_EST_LIT_LET.m3u'
                        self.session.open(HasBahCa1, sel, pixil)
            elif sel == ('BANGLADESH'):
                        pixil = host + 'BANGLADESH.m3u'
                        self.session.open(HasBahCa1, sel, pixil)
            elif sel == ('BRASIL'):
                        pixil = host + 'BRASIL.m3u'
                        self.session.open(HasBahCa1, sel, pixil)
            elif sel == ('BRASIL PLUTO'):
                        pixil = host + 'BRASIL_PLUTO.m3u'
                        self.session.open(HasBahCa1, sel, pixil)
            elif sel == ('BULGARIA'):
                        pixil = host + 'BULGARIA.m3u'
                        self.session.open(HasBahCa1, sel, pixil)
            elif sel == ('CAMBODIA'):
                        pixil = host + 'CAMBODIA.m3u'
                        self.session.open(HasBahCa1, sel, pixil)
            elif sel == ('CANADA'):
                        pixil = host + 'CANADA.m3u'
                        self.session.open(HasBahCa1, sel, pixil)
            elif sel == ('CANADA TVPLUS'):
                        pixil = host + 'CANADA_TVPLUS.m3u'
                        self.session.open(HasBahCa1, sel, pixil)
            elif sel == ('CHILE'):
                        pixil = host + 'CHILE.m3u'
                        self.session.open(HasBahCa1, sel, pixil)
            elif sel == ('CHINA1'):
                        pixil = host + 'CHINA1.m3u'
                        self.session.open(HasBahCa1, sel, pixil)
            elif sel == ('CHINA2'):
                        pixil = host + 'CHINA2.m3u'
                        self.session.open(HasBahCa1, sel, pixil)
            elif sel == ('COLOMBIA'):
                        pixil = host + 'COLOMBIA.m3u'
                        self.session.open(HasBahCa1, sel, pixil)
            elif sel == ('COSTARICA'):
                        pixil = host + 'COSTARICA.m3u'
                        self.session.open(HasBahCa1, sel, pixil)
            elif sel == ('CROATIA'):
                        pixil = host + 'CROATIA.m3u'
                        self.session.open(HasBahCa1, sel, pixil)
            elif sel == ('CZECH'):
                        pixil = host + 'CZECH.m3u'
                        self.session.open(HasBahCa1, sel, pixil)
            elif sel == ('DOMINICANRP'):
                        pixil = host + 'DOMINICANRP.m3u'
                        self.session.open(HasBahCa1, sel, pixil)
            elif sel == ('ENGLAND'):
                        pixil = host + 'ENGLAND.m3u'
                        self.session.open(HasBahCa1, sel, pixil)
            elif sel == ('ENGLAND PLUTO'):
                        pixil = host + 'ENGLAND_PLUTO.m3u'
                        self.session.open(HasBahCa1, sel, pixil)
            elif sel == ('ENGLAND TVPLUS'):
                        pixil = host + 'ENGLAND_TVPLUS.m3u'
                        self.session.open(HasBahCa1, sel, pixil)
            elif sel == ('FRANCE'):
                        pixil = host + 'FRANCE.m3u'
                        self.session.open(HasBahCa1, sel, pixil)
            elif sel == ('FRANCE PLUTO'):
                        pixil = host + 'FRANCE_PLUTO.m3u'
                        self.session.open(HasBahCa1, sel, pixil)
            elif sel == ('FRANCE TVPLUS'):
                        pixil = host + 'FRANCE_TVPLUS.m3u'
                        self.session.open(HasBahCa1, sel, pixil)
            elif sel == ('GERMAN'):
                        pixil = host + 'GERMAN.m3u'
                        self.session.open(HasBahCa1, sel, pixil)
            elif sel == ('GERMAN LOKAL'):
                        pixil = host + 'GERMAN_LOKAL.m3u'
                        self.session.open(HasBahCa1, sel, pixil)
            elif sel == ('GERMAN PLUTO'):
                        pixil = host + 'GERMAN_PLUTO.m3u'
                        self.session.open(HasBahCa1, sel, pixil)
            elif sel == ('GERMAN TVPLUS'):
                        pixil = host + 'GERMAN_TVPLUS.m3u'
                        self.session.open(HasBahCa1, sel, pixil)
            elif sel == ('GREEK'):
                        pixil = host + 'GREEK.m3u'
                        self.session.open(HasBahCa1, sel, pixil)
            elif sel == ('HAITI'):
                        pixil = host + 'HAITI.m3u'
                        self.session.open(HasBahCa1, sel, pixil)
            elif sel == ('HOLLAND BELGIEN'):
                        pixil = host + 'HOLLAND_BELGIEN.m3u'
                        self.session.open(HasBahCa1, sel, pixil)
            elif sel == ('HOLLAND PLUTO'):
                        pixil = host + 'HOLLAND_PLUTO.m3u'
                        self.session.open(HasBahCa1, sel, pixil)
            elif sel == ('HONDURAS'):
                        pixil = host + 'HONDURAS.m3u'
                        self.session.open(HasBahCa1, sel, pixil)
            elif sel == ('INDIA TAMIL'):
                        pixil = host + 'INDIA_TAMIL.m3u'
                        self.session.open(HasBahCa1, sel, pixil)
            elif sel == ('INDONESIA'):
                        pixil = host + 'INDONESIA.m3u'
                        self.session.open(HasBahCa1, sel, pixil)
            elif sel == ('ISRAEL'):
                        pixil = host + 'ISRAEL.m3u'
                        self.session.open(HasBahCa1, sel, pixil)
            elif sel == ('ITALIA'):
                        pixil = host + 'ITALIA.m3u'
                        self.session.open(HasBahCa1, sel, pixil)
            elif sel == ('ITALIA PLUTO'):
                        pixil = host + 'ITALIA_PLUTO.m3u'
                        self.session.open(HasBahCa1, sel, pixil)
            elif sel == ('ITALIA TVPLUS'):
                        pixil = host + 'ITALIA_TVPLUS.m3u'
                        self.session.open(HasBahCa1, sel, pixil)
            elif sel == ('JAPAN'):
                        pixil = host + 'JAPAN.m3u'
                        self.session.open(HasBahCa1, sel, pixil)
            elif sel == ('KHUSUS MALAZIA'):
                        pixil = host + 'KHUSUS_MALAZIA.m3u'
                        self.session.open(HasBahCa1, sel, pixil)
            elif sel == ('KOREA'):
                        pixil = host + 'KOREA.m3u'
                        self.session.open(HasBahCa1, sel, pixil)
            elif sel == ('KURDI'):
                        pixil = host + 'KURDI.m3u'
                        self.session.open(HasBahCa1, sel, pixil)
            elif sel == ('LAOS'):
                        pixil = host + 'LAOS.m3u'
                        self.session.open(HasBahCa1, sel, pixil)
            elif sel == ('LATINO MIX'):
                        pixil = host + 'LATINO_MIX.m3u'
                        self.session.open(HasBahCa1, sel, pixil)
            elif sel == ('LATINO PLUTO'):
                        pixil = host + 'LATINO_PLUTO.m3u'
                        self.session.open(HasBahCa1, sel, pixil)
            elif sel == ('LUXEMBOURG'):
                        pixil = host + 'LUXEMBOURG.m3u'
                        self.session.open(HasBahCa1, sel, pixil)
            elif sel == ('MACEDONIA'):
                        pixil = host + 'MACEDONIA.m3u'
                        self.session.open(HasBahCa1, sel, pixil)
            elif sel == ('MAGYAR'):
                        pixil = host + 'MAGYAR.m3u'
                        self.session.open(HasBahCa1, sel, pixil)
            elif sel == ('MALTA'):
                        pixil = host + 'MALTA.m3u'
                        self.session.open(HasBahCa1, sel, pixil)
            elif sel == ('MEXICO'):
                        pixil = host + 'MEXICO.m3u'
                        self.session.open(HasBahCa1, sel, pixil)
            elif sel == ('MEXICO PLUTO'):
                        pixil = host + 'MEXICO_PLUTO.m3u'
                        self.session.open(HasBahCa1, sel, pixil)
            elif sel == ('PAKISTAN'):
                        pixil = host + 'PAKISTAN.m3u'
                        self.session.open(HasBahCa1, sel, pixil)
            elif sel == ('PANAMA'):
                        pixil = host + 'PANAMA.m3u'
                        self.session.open(HasBahCa1, sel, pixil)
            elif sel == ('PERU'):
                        pixil = host + 'PERU.m3u'
                        self.session.open(HasBahCa1, sel, pixil)
            elif sel == ('POLAND'):
                        pixil = host + 'POLAND.m3u'
                        self.session.open(HasBahCa1, sel, pixil)
            elif sel == ('PORTUGAL'):
                        pixil = host + 'PORTUGAL.m3u'
                        self.session.open(HasBahCa1, sel, pixil)
            elif sel == ('ROMANIA MOLDOVA'):
                        pixil = host + 'ROMANIA_MOLDOVA.m3u'
                        self.session.open(HasBahCa1, sel, pixil)
            elif sel == ('RUS ARMENIA'):
                        pixil = host + 'RUS_ARMENIA.m3u'
                        self.session.open(HasBahCa1, sel, pixil)
            elif sel == ('RUS EX CCCP1'):
                        pixil = host + 'RUS_EXCCCP1.m3u'
                        self.session.open(HasBahCa1, sel, pixil)
            elif sel == ('RUS EX CCCP2'):
                        pixil = host + 'RUS_EXCCCP2.m3u'
                        self.session.open(HasBahCa1, sel, pixil)
            elif sel == ('RUS EX CCCP LOCAL'):
                        pixil = host + 'RUS_EXCCCP_LOCAL.m3u'
                        self.session.open(HasBahCa1, sel, pixil)
            elif sel == ('RUS GEORGIA'):
                        pixil = host + 'RUS_GEORGIA.m3u'
                        self.session.open(HasBahCa1, sel, pixil)
            elif sel == ('RUS KAZAKHSTAN'):
                        pixil = host + 'RUS_KAZAKISTAN.m3u'
                        self.session.open(HasBahCa1, sel, pixil)
            elif sel == ('RUS UKRAINE1'):
                        pixil = host + 'RUS_UKRAINE1.m3u'
                        self.session.open(HasBahCa1, sel, pixil)
            elif sel == ('RUS UKRAINE2'):
                        pixil = host + 'RUS_UKRAINE2.m3u'
                        self.session.open(HasBahCa1, sel, pixil)
            elif sel == ('SERBIA'):
                        pixil = host + 'SERBIA.m3u'
                        self.session.open(HasBahCa1, sel, pixil)
            elif sel == ('SKANDINAV FINLAND'):
                        pixil = host + 'SKANDINAV_FINLAND.m3u'
                        self.session.open(HasBahCa1, sel, pixil)
            elif sel == ('SLOVAKIA SLOVENIA'):
                        pixil = host + 'SLOVAKIA_SLOVENIA.m3u'
                        self.session.open(HasBahCa1, sel, pixil)
            elif sel == ('SPAIN'):
                        pixil = host + 'SPAIN.m3u'
                        self.session.open(HasBahCa1, sel, pixil)
            elif sel == ('SPAIN PLUTO'):
                        pixil = host + 'SPAIN_PLUTO.m3u'
                        self.session.open(HasBahCa1, sel, pixil)
            elif sel == ('SPAIN TVPLUS'):
                        pixil = host + 'SPAIN_TVPLUS.m3u'
                        self.session.open(HasBahCa1, sel, pixil)
            elif sel == ('SWITZERLAND'):
                        pixil = host + 'SWITZERLAND.m3u'
                        self.session.open(HasBahCa1, sel, pixil)
            elif sel == ('SWITZERLAND PLUTO'):
                        pixil = host + 'SWITZERLAND_PLUTO.m3u'
                        self.session.open(HasBahCa1, sel, pixil)
            elif sel == ('SWITZERLAND TVPLUS'):
                        pixil = host + 'SWITZERLAND_TVPLUS.m3u'
                        self.session.open(HasBahCa1, sel, pixil)
            elif sel == ('TAIWAN'):
                        pixil = host + 'TAIWAN.m3u'
                        self.session.open(HasBahCa1, sel, pixil)
            elif sel == ('THAILAND'):
                        pixil = host + 'THAILAND.m3u'
                        self.session.open(HasBahCa1, sel, pixil)                        
            elif sel == ('TURKCE FILMLER'):
                        pixil = host + 'TURKCE_FILMLER.m3u'
                        self.session.open(HasBahCa1, sel, pixil)
            elif sel == ('TURK 1TAMLISTE'):
                        pixil = host + 'TURK_1TAMLISTE.m3u'
                        self.session.open(HasBahCa1, sel, pixil)
            elif sel == ('TURK AVRUPA'):
                        pixil = host + 'TURK_AVRUPA.m3u'
                        self.session.open(HasBahCa1, sel, pixil)
            elif sel == ('TURK BLUTV'):
                        pixil = host + 'TURK_BLUTV.m3u'
                        self.session.open(HasBahCa1, sel, pixil)
            elif sel == ('TURK COCUK'):
                        pixil = host + 'TURK_COCUK.m3u'
                        self.session.open(HasBahCa1, sel, pixil)
            elif sel == ('TURK DINI'):
                        pixil = host + 'TURK_DINI.m3u'
                        self.session.open(HasBahCa1, sel, pixil)
            elif sel == ('TURK HABER'):
                        pixil = host + 'TURK_HABER.m3u'
                        self.session.open(HasBahCa1, sel, pixil)
            elif sel == ('TURK KARISIK'):
                        pixil = host + 'TURK_KARISIK.m3u'
                        self.session.open(HasBahCa1, sel, pixil)
            elif sel == ('TURK MUZIK'):
                        pixil = host + 'TURK_MUZIK.m3u'
                        self.session.open(HasBahCa1, sel, pixil)
            elif sel == ('TURK OZEL'):
                        pixil = host + 'TURK_OZEL.m3u'
                        self.session.open(HasBahCa1, sel, pixil)
            elif sel == ('TURK RADYOLAR'):
                        pixil = host + 'TURK_RADYOLAR.m3u'
                        self.session.open(HasBahCa1, sel, pixil)
            elif sel == ('TURK ULUSAL'):
                        pixil = host + 'TURK_ULUSAL.m3u'
                        self.session.open(HasBahCa1, sel, pixil)
            elif sel == ('TURK YEREL'):
                        pixil = host + 'TURK_YEREL.m3u'
                        self.session.open(HasBahCa1, sel, pixil)
            elif sel == ('TURKI AZERBAYCAN'):
                        pixil = host + 'TURKi_AZERBAYCAN.m3u'
                        self.session.open(HasBahCa1, sel, pixil)
            elif sel == ('TURKI KKTC'):
                        pixil = host + 'TURKi_KKTC.m3u'
                        self.session.open(HasBahCa1, sel, pixil)
            elif sel == ('TURKI TURKMENISTAN'):
                        pixil = host + 'TURKi_TURKMENISTAN.m3u'
                        self.session.open(HasBahCa1, sel, pixil)
            elif sel == ('TURKI ULKELER'):
                        pixil = host + 'TURKi_ULKELER.m3u'
                        self.session.open(HasBahCa1, sel, pixil)
            elif sel == ('URUGUAY'):
                        pixil = host + 'URUGUAY.m3u'
                        self.session.open(HasBahCa1, sel, pixil)
            elif sel == ('USA'):
                        pixil = host + 'USA.m3u'
                        self.session.open(HasBahCa1, sel, pixil)
            elif sel == ('USA CHINA ENGLISH'):
                        pixil = host + 'USA_CHINA_ENG.m3u'
                        self.session.open(HasBahCa1, sel, pixil)
            elif sel == ('USA LOCAL'):
                        pixil = host + 'USA_LOCAL.m3u'
                        self.session.open(HasBahCa1, sel, pixil)
            elif sel == ('USA MYTVTO VELLYTV'):
                        pixil = host + 'USA_MyTV_VellyTV.m3u'
                        self.session.open(HasBahCa1, sel, pixil)
            elif sel == ('USA PLEX'):
                        pixil = host + 'USA_PLEX.m3u'
                        self.session.open(HasBahCa1, sel, pixil)
            elif sel == ('USA PLUTO'):
                        pixil = host + 'USA_PLUTO.m3u'
                        self.session.open(HasBahCa1, sel, pixil)
            elif sel == ('USA TVPLUS'):
                        pixil = host + 'USA_TVPLUS.m3u'
                        self.session.open(HasBahCa1, sel, pixil)
            elif sel == ('USA XUMO'):
                        pixil = host + 'USA_XUMO.m3u'
                        self.session.open(HasBahCa1, sel, pixil)
            elif sel == ('VIETNAM'):
                        pixil = host + 'VIETNAM.m3u'
                        self.session.open(HasBahCa1, sel, pixil)
        return

class HasBahCaC(Screen):
    def __init__(self, session, name, url):
        Screen.__init__(self, session)
        self.session = session
        skin = path_skin + 'settings.xml'
        with open(skin, 'r') as f:
            self.skin = f.read()
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
        self['progress'] = ProgressBar()
        self['progresstext'] = StaticText()
        self["progress"].hide()
        self['live'] = Label('')
        self['live'].setText('')
        self['actions'] = ActionMap(['SetupActions', 'ColorActions'], {
            'ok': self.okRun,
            'green': self.okRun,
            'red': self.close,
            # 'yellow': self.convert,
            # 'back': self.close(),
            'cancel': self.close}, -2)
        self.timer = eTimer()
        if DreamOS():
            self.timer_conn = self.timer.timeout.connect(self._gotPageLoad)
        else:
            self.timer.callback.append(self._gotPageLoad)
        self.timer.start(300, True)
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
            # if six.PY3:
                # content =six.ensure_str(content)
            print("HasBahCa t content =", content)
            n1 = content.find('js-details-container Details">', 0)
            n2 = content.find('<div class="Details-content--shown Box-footer', n1)
            content2 = content[n1:n2]
            regexvideo = 'title="(.*?).m3u.*?href="/HasBahCa/m3u_Links/blob/main/(.*?).m3u">.*?wrap">(.*?)</time'
            match = re.compile(regexvideo, re.DOTALL).findall(content2)
            # print("HasBahCa t match =", match)
            for name, url, date in match:
                if 'readme' in name.lower():
                    continue
                if 'enigma2' in name.lower():
                    continue                    
                print("HasBahCa t name =", name)
                print("HasBahCa t url =", url)
                print("HasBahCa t date =", date)
                # url1 =  'https://raw.githubusercontent.com/HasBahCa/m3u_Links/main/' + str(url) + '.m3u'
                url1 = '{}{}{}'.format('https://raw.githubusercontent.com/HasBahCa/m3u_Links/main/',  str(url), '.m3u')
                date = date.replace(',', '')
                name1 = name.replace('HasBahCa', '°')
                name1 = name1.replace('-', ' ').replace('_', ' ')
                name1 = decodeHtml(name1)
                name = name1 + ' | ' + date
                # print("******** name 1 ******* %s" % name)
                # print("HasBahCa t name =", name)
                # print("HasBahCa t url1 =", url1)
                item = name + "###" + url1
                # print('HasBahCa Items sort: ', item)
                items.append(item)
            items.sort()
            for item in items:
                name = item.split('###')[0]
                url2 = item.split('###')[1]
                self.names.append(name)
                self.urls.append(url2)
            self["live"].setText('N.' + str(len(self.names)) + " CATEGORY")
            self['info'].setText(_('Please select ...'))
            self['key_green'].show()
            showlisthasba(self.names, self['text'])
        except Exception as e:
            print('error ', str(e))
        print('-------------HasBahCa-------------')
        MemClean()
        print('-------------memclean-------------')
        # self.onLayoutFinish.append(self.__layoutFinished)

    def okRun(self):
        idx = self["text"].getSelectionIndex()
        name = self.names[idx]
        url = self.urls[idx]
        print("HasBahCa ok url1 =", url)
        self.session.open(HasBahCa1, name, url)

class HasBahCa1(Screen):
    def __init__(self, session, sel, url):
        self.session = session
        Screen.__init__(self, session)
        skin = path_skin + 'settings.xml'
        with open(skin, 'r') as f:
            self.skin = f.read()
        self.setup_title = ('HasBahCa TV')
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
        self.names = []
        self.urls = []
        items = []
        try:
            content = getUrl(url)
            if six.PY3:
                content = six.ensure_str(content)
            content = content.replace('$BorpasFileFormat="1"','')
            regexvideo = '#EXTINF.*?,(.*?)\\n(.*?)\\n'
            # regexvideo = 'EXTINF.*?group-title="(.*?)".*?,(.*?)\\n(.*?)\\n'
            # regexvideo = '#EXTINF.*?,(.*?)\\n(.+)'
            match = re.compile(regexvideo, re.DOTALL).findall(content)
            for name, url in match:
            # for group, name, url in match:
                # name = name.replace('_', ' ').replace('-', ' ')
                # name1 = group + ' | ' + name
                name1 = name.replace('_', ' ').replace('-', ' ')
                # name = get_safe_filename(name1)                
                # name = decodeHtml(name1)
                # name = checkStr(name1)
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
            MemClean()
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
            name_file = self.name.replace('/', '_').replace(',', '').replace('hasbahca', 'hbc')
            cleanName = re.sub(r'[\<\>\:\"\/\\\|\?\*]', '_', str(name_file))
            cleanName = re.sub(r' ', '_', cleanName)
            cleanName = re.sub(r'\d+:\d+:[\d.]+', '_', cleanName)
            name_file = re.sub(r'_+', '_', cleanName)
            bouquetname = 'userbouquet.hbc_%s.%s' % (name_file.lower(), self.type.lower())
            self.tmpx = ''
            self.namel = ''
            tmplist = []
            tmplist.append('#NAME HasBahCa IPTV %s (%s)' % (name_file, self.type))
            # tmplist.append('#NAME HASBAHCA IPTV %s' % name_file)
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
                    if line.startswith('#EXTM3U'):
                        continue
                    if '#EXTM3U $BorpasFileFormat="1"' in line: #force export bouquet ???
                        line = line.replace('$BorpasFileFormat="1"','')
                        continue
                    if line == '':
                        continue
                    if line == ' ':
                        continue
                    if line.startswith("#EXTINF"):
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
        streaml = False
        self.allowPiP = False
        self.service = None
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
            0: '4:3 Letterbox',
            1: '4:3 PanScan',
            2: '16:9',
            3: '16:9 always',
            4: '16:10 Letterbox',
            5: '16:10 PanScan',
            6: '16:9 Letterbox'
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

# if PY3:
    # from importlib import reload
# from . import plugin
# reload(plugin)

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
