#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
****************************************
*        coded by Lululla              *
*             skin by MMark            *
*             19/02/2022               *
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
    # import http.client
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
        # import ssl
        sslContext = ssl._create_unverified_context()
    except:
        sslContext = None
try:
    # from OpenSSL import SSL
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
currversion = '1.0'
title_plug = 'HasBahCa '
desc_plugin = ('..:: HasBahCa by Lululla %s ::.. ' % currversion)
plugin_path = resolveFilename(SCOPE_PLUGINS, "Extensions/{}".format('HasBahCa'))
pluglogo = resolveFilename(SCOPE_PLUGINS, "Extensions/{}/res/pics/logo.png".format('HasBahCa'))
png = resolveFilename(SCOPE_PLUGINS, "Extensions/{}/res/pics/setting.png".format('HasBahCa'))
path_skin = resolveFilename(SCOPE_PLUGINS, "Extensions/{}/res/skins/hd/".format('HasBahCa'))
if isFHD():
    path_skin = resolveFilename(SCOPE_PLUGINS, "Extensions/{}/res/skins/fhd/".format('HasBahCa'))
if DreamOS():
    path_skin = path_skin + 'dreamOs/'
print('HasBahCa path_skin: ', path_skin)
enigma_path = '/etc/enigma2'

Panel_Dlist = [
    ('FULL LIST'),
    ('IPTV'),
    ('VOD_FILM'),
    ('RADIO'),
    ('WEBCAM'),
    ('CATEGORY'),
]

def downloadFile(url, target):
    try:
        response = urlopen(url, timeout=10)
        with open(target, 'wb') as output:
            output.write(response.read())
        return True
    except:
        print("download error")
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
        self['actions'] = ActionMap(['SetupActions', 'ColorActions', ], {
            'ok': self.okRun,
            'green': self.okRun,
            'back': self.closerm,
            'red': self.closerm,
            'cancel': self.closerm}, -1)
        self.onLayoutFinish.append(self.updateMenuList)

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
        self['text'].setList(list)
        self['info'].setText(_('Please select ...'))
        self['key_green'].show()

    def okRun(self):
        self.keyNumberGlobalCB(self['text'].getSelectedIndex())

    def keyNumberGlobalCB(self, idx):
        sel = self.menu_list[idx]
        if sel == _('FULL LIST'):
            url = 'https://raw.githubusercontent.com/HasBahCa/IPTV-LIST/main/HasBahCa_IPTV_FULL.m3u'
            self.session.open(HasBahCa1, sel, url)
        elif sel == _('IPTV'):
            url = 'https://raw.githubusercontent.com/HasBahCa/IPTV-LIST/main/hasbahca_iptv.m3u'
            self.session.open(HasBahCa1, sel, url)
        elif sel == _('VOD_FILM'):
            url = 'https://raw.githubusercontent.com/HasBahCa/IPTV-LIST/main/HasBahCa_VOD_MOVIES_FILM.m3u'
            self.session.open(HasBahCa1, sel, url)
        elif sel == _('RADIO'):
            url = 'https://raw.githubusercontent.com/HasBahCa/IPTV-LIST/main/HasBahCa_webWORLD_RADIOS.m3u '
            self.session.open(HasBahCa1, sel, url)
        elif sel == _('WEBCAM'):
            url = 'https://raw.githubusercontent.com/HasBahCa/IPTV-LIST/main/HasBahCa_WEBCAM.m3u'
            self.session.open(HasBahCa1, sel, url)
        elif sel == _('CATEGORY'):
            url = 'https://github.com/HasBahCa/IPTV-LIST'
            self.session.open(HasBahCa, sel, url)
        else:
            return

class HasBahCa(Screen):

    def __init__(self, session, name, url):
        self.session = session
        skin = path_skin + 'settings.xml'
        with open(skin, 'r') as f:
            self.skin = f.read()
        self.setup_title = ('HasBahCa TV')
        Screen.__init__(self, session)
        self.setTitle(title_plug)
        self.list = []
        self.name = name
        self.url = url
        self['text'] = hasList([])
        self['info'] = Label(_('Loading data... Please wait'))
        self['key_red'] = Button(_('Back'))
        self['key_green'] = Button(_('Select'))
        self['key_yellow'] = Button(_(''))
        self["key_blue"] = Button(_(''))
        self['key_green'].hide()
        self['key_yellow'].hide()
        self['key_blue'].hide()
        self['title'] = Label(title_plug)
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
            n1 = content.find('<div class="sr-only" role="row">', 0)
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
                name1 = name.replace('.m3u', '')
                name = name1 + ' ' + date
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
        self.setup_title = ('HasBahCa')
        Screen.__init__(self, session)
        self.setTitle(title_plug)
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
        self.timer = eTimer()
        if DreamOS():
            self.timer_conn = self.timer.timeout.connect(self._gotPageLoad)
        else:
            self.timer.callback.append(self._gotPageLoad)
        self.timer.start(1500, True)
        self['actions'] = ActionMap(['SetupActions', 'ColorActions'], {
            'ok': self.okRun,
            'green': self.okRun,
            'red': self.close,
            'yellow': self.convert,
            'blue': self.deleteBouquets,
            'cancel': self.close}, -2)

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
            regexvideo = 'EXTINF.*?group-title="(.*?)".*?,(.*?)\\n(.*?)\\n'
            match = re.compile(regexvideo, re.DOTALL).findall(content)
            for group, name, url in match:
                name1 = group + ' - ' + name
                print("******** name 2 ******* %s" % name1)
                name = decodeHtml(name1)
                item = name + "###" + url
                print('Webcam4 Items sort: ', item)
                items.append(item)
            items.sort()
            for item in items:
                name = item.split('###')[0]
                url = item.split('###')[1]
                self.names.append(name)
                self.urls.append(url)
            self['info'].setText(_('Please select ...'))
            self['key_green'].show()
            self['key_yellow'].show()
            self['key_blue'].show()
            showlisthasba(self.names, self['text'])
        except Exception as e:
            print('error HasBahCa', str(e))

    def okRun(self):
        idx = self["text"].getSelectionIndex()
        name = self.names[idx]
        url = self.urls[idx]
        self.session.open(Playgo, name, url)

    def convert(self):
        self.session.openWithCallback(self.convert2, MessageBox, _("Do you want to Convert %s to Favorite Bouquet ?\n\nAttention!! Wait while converting !!!") % self.name, MessageBox.TYPE_YESNO, timeout=10, default=True)

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

            file = "/tmp/%s.m3u" % name_file
            downloadFile(self.url, file)

            # if os.path.isfile(file) and os.stat(file).st_size > 0:

            for line in open(file):
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

                with open(path2, 'a+') as f:
                    bouquetTvString = '#SERVICE 1:7:1:0:0:0:0:0:0:0:FROM BOUQUET "' + str(bouquetname) + '" ORDER BY bouquet\n'
                    f.write(str(bouquetTvString))
                self.mbox = self.session.open(MessageBox, _('Shuffle Favorite List in Progress') + '\n' + _('Wait please ...'), MessageBox.TYPE_INFO, timeout=5)
            ReloadBouquets()




# Rename unlinked bouquet file /etc/enigma2/userbouquet.webcam.tv to /etc/enigma2/userbouquet.webcam.tv.del

# remove bouquet  'hbc'
    def deleteBouquets(self):
        """
        Clean up routine to remove any previously made changes
        """
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
