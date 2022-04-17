#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
****************************************
*        coded by Lululla              *
*             skin by MMark            *
*             16/04/2022               *
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
    # from urlparse import urlparse
    # from urllib import urlencode, parse_qs
    import httplib
    import six
except:
    from http.client import HTTPConnection, CannotSendRequest, BadStatusLine, HTTPException
    from urllib.error import URLError, HTTPError
    from urllib.request import urlopen, Request
    # from urllib.parse import urlparse
    # from urllib.parse import parse_qs, urlencode
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
currversion = '1.4'
title_plug = 'HasBahCa '
desc_plugin = ('..:: HasBahCa by Lululla %s ::.. ' % currversion)
plugin_path = resolveFilename(SCOPE_PLUGINS, "Extensions/{}".format('HasBahCa'))
pluglogo = resolveFilename(SCOPE_PLUGINS, "Extensions/{}/res/pics/logo.png".format('HasBahCa'))
png = resolveFilename(SCOPE_PLUGINS, "Extensions/{}/res/pics/tv.png".format('HasBahCa'))

hostcategoryes = 'https://github.com/HasBahCa/IPTV-LIST/'
hostcategory = 'https://github.com/HasBahCa/IPTV-LIST'
github = 'https://raw.githubusercontent.com/HasBahCa/IPTV-LIST/main/'

tyurl = 'http://hasbahca.net/hasbahca_m3u/'
enigma_path = '/etc/enigma2'

if isFHD():
    path_skin = resolveFilename(SCOPE_PLUGINS, "Extensions/{}/res/skins/fhd/".format('HasBahCa'))
else:
    path_skin = resolveFilename(SCOPE_PLUGINS, "Extensions/{}/res/skins/hd/".format('HasBahCa'))
if DreamOS():
    path_skin = path_skin + 'dreamOs/'
print('HasBahCa path_skin: ', path_skin)



def downloadFile(url, target):
    try:
        response = ReadUrl(url)
        print('response: ', response)
        # response = urlopen(url, timeout=5)        
        with open(target, 'w') as output:
            output.write(response) #.read())
        return True
    except Exception as e:
        print("downloadFile error ", str(e))
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
        res.append(MultiContentEntryPixmapAlphaTest(pos=(10, 10), size=(50, 40), png=loadPNG(png)))
        res.append(MultiContentEntryText(pos=(90, 0), size=(1200, 60), font=0, text=name, color=0xa6d1fe, flags=RT_HALIGN_LEFT | RT_VALIGN_CENTER))
    else:
        res.append(MultiContentEntryPixmapAlphaTest(pos=(10, 10), size=(50, 40), png=loadPNG(png)))
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
        self['info'] = Label(_('Give me a few seconds ... loading the data'))
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
        self.timer = eTimer()
        if DreamOS():
            self.timer_conn = self.timer.timeout.connect(self.updateMenuList)
        else:
            self.timer.callback.append(self.updateMenuList)
        self.timer.start(1500, True)
        
        # self.onFirstExecBegin.append(self.updateMenuList)
        self.onLayoutFinish.append(self.__layoutFinished)

    def __layoutFinished(self):
        self.setTitle(self.setup_title)

    def closerm(self):
        deletetmp()
        self.close()


#<tr><td valign="top">&nbsp;</td><td><a href="1MUSIC.m3u">1MUSIC.m3u</a>             </td><td align="right">2022-03-07 15:40  </td><td align="right"> 33K</td><td>&nbsp;</td></tr>
#<tr><td valign="top">&nbsp;</td><td><a href="ALBANIA_BOSNIA_KOSOVO.m3u">ALBANIA_BOSNIA_KOSOV..&gt;</a></td><td align="right">2022-03-06 06:08  </td><td align="right">3.8K</td><td>&nbsp;</td></tr>
    def updateMenuList(self):
        self.names = []
        self.urls = []
        items = []
        urls = tyurl
        try:
            content = getUrl(urls)
            if six.PY3:
                content = six.ensure_str(content)
            content = content.replace('..&gt;','')
            regexvideo = 'td><a href="(.*?)">(.*?).m3u.*?right">(.*?)  </td>.*?'
            match = re.compile(regexvideo,re.DOTALL).findall(content)
            idx = 0
            for url, name, date in match:
                print('url= ',url)
                print('date= ',date)
                if 'parent' in name.lower():
                    continue
                elif 'hasbahcanetlink' in url:
                    continue
                elif '.txt' in name.lower():
                    continue
                name = url.replace('..&gt;','').replace('_',' ').replace('.m3u','')   
                name = name #+ ' ' + date
                url = urls + url
                item = name + "###" + url
                items.append(item)
            items.sort()
            for item in items:
                name = item.split("###")[0]
                url = item.split("###")[1]
                self.names.append(name)
                self.urls.append(url)
                idx += 1
                
            self.names.append('ALL CATEGORY')
            self.urls.append(hostcategoryes)
            idx += 1    
            
            self['info'].setText(_('Please now select ...'))
            self["live"].setText('N.' + str(idx) + " CATEGORY")
            self['key_green'].show()
            showlisthasba(self.names, self['text'])
        except Exception as e:
            print('error HasBahCa1', str(e))


    def okRun(self):
        i = len(self.names)
        print('iiiiii= ',i)
        # if i < 1:
            # return
        idx = self["text"].getSelectionIndex()
        name = self.names[idx]
        url = self.urls[idx]
        if 'parent' in name.lower():
            return
        elif 'hasbahcanetlink' in url:
            return            
        elif 'parent' in name.lower():
            return
        elif '.txt' in name.lower():
            return
        elif 'category' in name.lower(): 
            self.session.open(HasBahCaC, name, url) 
            print('url HasBahCa C : ', url)
        else:    
            self.session.open(HasBahCa1, name, url)
            print('url HasBahCa 1 : ', url)

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
            print('urlll content: ', url)
            n1 = content.find('js-details-container Details">', 0)
            n2 = content.find('<div class="Details-content--shown Box-footer', n1)
            content2 = content[n1:n2]
            regexvideo = 'title="(.*?).m3u.*?href="/HasBahCa/IPTV-LIST/blob/main/(.*?).m3u">.*?</a></span.*?</div>'
            # regexvideo = 'title="(.*?).m3u.*?href="/HasBahCa/m3u_Links/blob/main/(.*?).m3u">.*?wrap">(.*?)</time'            
            match = re.compile(regexvideo, re.DOTALL).findall(content2)
            print('match:  ', match)
            # print("HasBahCa t match =", match)
            for name, url in match:
                if 'readme' in name.lower():
                    continue
                if 'enigma2' in name.lower():
                    continue                    
                print("HasBahCa t name =", name)
                print("HasBahCa t url =", url)
                # print("HasBahCa t date =", date)
                url1 = '{}{}{}'.format(github, str(url), '.m3u')
                # date = date.replace(',', '')
                name1 = name.replace('HasBahCa', '°')
                name1 = name1.replace('-', ' ').replace('_', ' ')
                name = decodeHtml(name1)
                # name = name1 + ' | ' + date
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
            self['info'].setText(_('Please now select ...'))
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
        print('self.url: ', self.url)
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
            self['info'].setText(_('Please now select ...'))
            self['key_green'].show()
            self['key_yellow'].show()
            self['key_blue'].show()
            showlisthasba(self.names, self['text'])
            MemClean()
        except Exception as e:
            print('error HasBahCa', str(e))

    def okRun(self):
        i = len(self.names)
        print('iiiiii= ',i)
        if i < 1:
            return    
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
            tmplist.append('#SERVICE 1:64:0:0:0:0:0:0:0:0::%s CHANNELS' % name_file)
            tmplist.append('#DESCRIPTION --- %s ---' % name_file)
            print("Converting Bouquet %s" % name_file)
            # self.file = "/tmp/%s.m3u" % name_file.lower()  #use downloadhasba
            self.file = "/tmp/tempm3u.m3u" # % name_file.lower()  #use downloadhasba            
            # try:
            downloadFile(self.url, self.file)
            # except Exceptions as e:
                # print('Error download self m3u: ', str(e))
                # # self.download_m3u()
                
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
