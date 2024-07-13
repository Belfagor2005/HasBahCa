#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
****************************************
*        coded by Lululla              *
*             skin by MMark            *
*             14/02/2023               *
*   Thank's                            *
*      HasBahCa, Levi45, KiddaC, Pcd   *
****************************************
'''
from __future__ import print_function
from .__init__ import _
from . import Utils
from . import html_conv
# from . import cvbq
# from .plugin import currversion
from .Console import Console as xConsole
from Components.AVSwitch import AVSwitch
from Components.ActionMap import ActionMap
from Components.Button import Button
from Components.config import config
from Tools.Downloader import downloadWithProgress
from Components.Label import Label
from Components.MenuList import MenuList
from Components.MultiContent import MultiContentEntryText
from Components.MultiContent import MultiContentEntryPixmapAlphaTest
from Components.ServiceEventTracker import ServiceEventTracker, InfoBarBase
from Components.Sources.StaticText import StaticText
from Components.ProgressBar import ProgressBar
from Components.Sources.Progress import Progress
from Screens.InfoBarGenerics import InfoBarSubtitleSupport
from Screens.InfoBarGenerics import InfoBarSeek, InfoBarAudioSelection
from Screens.MessageBox import MessageBox
from Screens.Screen import Screen
from Tools.Directories import SCOPE_PLUGINS, resolveFilename
from enigma import (
    RT_VALIGN_CENTER,
    RT_HALIGN_LEFT,
    eTimer,
    eListboxPythonMultiContent,
    eServiceReference,
    iPlayableService,
    gFont,
    loadPNG,
    getDesktop,
)
from time import sleep
import os
import re
import six
import ssl
import sys
from datetime import datetime
import codecs
import json
global downloadhasba
global path_skin
global tyurl

tyurl = False
downloadhasba = None
currversion = '1.6'
PY3 = sys.version_info.major >= 3
hostcategoryes = 'https://github.com/HasBahCa/IPTV-LIST/'
github = 'https://raw.githubusercontent.com/HasBahCa/IPTV-LIST/main/'
tyurl1 = 'http://eviptv.com/m3u/'
tyurl2 = 'https://hasbahca.net/hasbahca_m3u/'
tyurl3 = tyurl1 + 'M3U_Listeleri/'
plugin_path = resolveFilename(SCOPE_PLUGINS, "Extensions/{}".format('HasBahCa'))
enigma_path = '/etc/enigma2'
path_playlist = os.path.join(plugin_path, 'Playlists')
installer_url = 'aHR0cHM6Ly9yYXcuZ2l0aHVidXNlcmNvbnRlbnQuY29tL0JlbGZhZ29yMjAwNS9IYXNCYWhDYS9tYWluL2luc3RhbGxlci5zaA=='
developer_url = 'aHR0cHM6Ly9hcGkuZ2l0aHViLmNvbS9yZXBvcy9CZWxmYWdvcjIwMDUvSGFzQmFoQ2E='
try:
    from urllib2 import urlopen, Request, URLError, HTTPError
except:
    from urllib.error import URLError, HTTPError
    from urllib.request import urlopen, Request
    PY3 = True

try:
    from Components.UsageConfig import defaultMoviePath
    downloadhasba = defaultMoviePath()
except:
    if os.path.exists("/usr/bin/apt-get"):
        downloadhasba = ('/media/hdd/movie/')

if sys.version_info >= (2, 7, 9):
    try:
        import ssl
        sslContext = ssl._create_unverified_context()
    except:
        sslContext = None


def ssl_urlopen(url):
    if sslContext:
        return urlopen(url, context=sslContext)
    else:
        return urlopen(url)


def downloadFilest(url, target):
    try:
        req = Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        response = ssl_urlopen(req)
        with open(target, 'w') as output:
            if PY3:
                output.write(response.read().decode('utf-8'))
            else:
                output.write(response.read())
            print('response: ', response)
        return True
    except HTTPError as e:
        print('HTTP Error code: ', e.code)
    except URLError as e:
        print('URL Error: ', e.reason)


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

# server
# https://eviptv.com/m3u8/

screenwidth = getDesktop(0).size()
if screenwidth.width() == 2560:
    path_skin = os.path.join(plugin_path, 'res/skins/uhd/')
elif screenwidth.width() == 1920:
    path_skin = os.path.join(plugin_path, 'res/skins/fhd/')
else:
    path_skin = os.path.join(plugin_path, 'res/skins/hd/')
if Utils.DreamOS():
    path_skin = os.path.join(path_skin, 'dreamOs/')
print('HasBahCa path_skin: ', path_skin)


class hasList(MenuList):
    def __init__(self, list):
        MenuList.__init__(self, list, True, eListboxPythonMultiContent)
        if screenwidth.width() == 2560:
            self.l.setItemHeight(60)
            textfont = int(42)
            self.l.setFont(0, gFont('Regular', textfont))
        elif screenwidth.width() == 1920:
            self.l.setItemHeight(50)
            textfont = int(30)
            self.l.setFont(0, gFont('Regular', textfont))
        else:
            self.l.setItemHeight(50)
            textfont = int(24)
            self.l.setFont(0, gFont('Regular', textfont))


# filter list assign png
EXTRAD = "radio", "radyo", "mix", "fm", "kbit", "rap", "metal", "alternative"
EXTXXX = "adult", "xxx"
EXTCAM = "webcam", "webcams"
EXTMUS = "music", "mtv", "deluxe", "djing", "fashion", "kiss", "mpeg", "sluhay", "stingray", "techno", "viva", "country", "vevo"
EXTSPOR = "spor", "boxing", "racing", "fight", "golf", "knock", "harley", "futbool", "motor", "nba", "nfl", "bull", "poker", "billiar", "fite"
EXTRLX = "relax", "nature", "escape"
EXTMOV = "movie", "film"


def hasbaSetListEntry(name):
    res = [name]
    png = os.path.join(plugin_path, 'res/pics/tv.png')
    if any(s in name.lower() for s in EXTCAM):
        png = os.path.join(plugin_path, 'res/pics/webcam.png')
    elif any(s in name.lower() for s in EXTRAD):
        png = os.path.join(plugin_path, 'res/pics/radio.png')
    elif any(s in name.lower() for s in EXTXXX):
        png = os.path.join(plugin_path, 'res/pics/xxx.png')
    elif any(s in name.lower() for s in EXTMUS):
        png = os.path.join(plugin_path, 'res/pics/music.png')
    elif any(s in name.lower() for s in EXTRLX):
        png = os.path.join(plugin_path, 'res/pics/relax.png')
    elif any(s in name.lower() for s in EXTMOV):
        png = os.path.join(plugin_path, 'res/pics/movie.png')
    elif any(s in name.lower() for s in EXTSPOR):
        png = os.path.join(plugin_path, 'res/pics/sport.png')
    elif 'pluto' in name.lower():
        png = os.path.join(plugin_path, 'res/pics/plutotv.png')
    elif 'tvplus' in name.lower():
        png = os.path.join(plugin_path, 'res/pics/tvplus.png')
    elif '~~~~' in name.lower():
        png = os.path.join(plugin_path, 'res/pics/mark.png')
    else:
        png = os.path.join(plugin_path, 'res/pics/tv.png')

    if screenwidth.width() == 2560:
        res.append(MultiContentEntryPixmapAlphaTest(pos=(5, 5), size=(50, 50), png=loadPNG(png)))
        res.append(MultiContentEntryText(pos=(90, 0), size=(1200, 60), font=0, text=name, color=0xa6d1fe, flags=RT_HALIGN_LEFT | RT_VALIGN_CENTER))
    elif screenwidth.width() == 1920:
        res.append(MultiContentEntryPixmapAlphaTest(pos=(5, 5), size=(40, 40), png=loadPNG(png)))
        res.append(MultiContentEntryText(pos=(70, 0), size=(1000, 50), font=0, text=name, color=0xa6d1fe, flags=RT_HALIGN_LEFT | RT_VALIGN_CENTER))
    else:
        res.append(MultiContentEntryPixmapAlphaTest(pos=(3, 5), size=(40, 40), png=loadPNG(png)))
        res.append(MultiContentEntryText(pos=(50, 0), size=(500, 50), font=0, text=name, color=0xa6d1fe, flags=RT_HALIGN_LEFT | RT_VALIGN_CENTER))
    return res


def showlisthasba(data, list):
    icount = 0
    plist = []
    for line in data:
        name = data[icount]
        plist.append(hasbaSetListEntry(name))
        icount += 1
        list.setList(plist)


def returnIMDB(text_clear):
    TMDB = resolveFilename(SCOPE_PLUGINS, "Extensions/{}".format('TMDB'))
    IMDb = resolveFilename(SCOPE_PLUGINS, "Extensions/{}".format('IMDb'))
    if os.path.exists(TMDB):
        try:
            from Plugins.Extensions.TMBD.plugin import TMBD
            text = html_conv.html_unescape(text_clear)
            _session.open(TMBD.tmdbScreen, text, 0)
        except Exception as e:
            print("[XCF] Tmdb: ", str(e))
        return True
    elif os.path.exists(IMDb):
        try:
            from Plugins.Extensions.IMDb.plugin import main as imdb
            text = html_conv.html_unescape(text_clear)
            imdb(_session, text)
        except Exception as e:
            print("[XCF] imdb: ", str(e))
        return True
    else:
        text_clear = html_conv.html_unescape(text_clear)
        _session.open(MessageBox, text_clear, MessageBox.TYPE_INFO)
        return True
    return False

def decodename(name):
    import unicodedata
    import six
    if isinstance(name, six.text_type):
        name = name.encode('utf-8')
    name = unicodedata.normalize('NFKD', six.text_type(name, 'utf_8', errors='ignore')).encode('ASCII', 'ignore')
    name = re.sub(b'[^a-z0-9-_]', b'', name.lower())
    if not name:
        name = fallback
    return six.ensure_str(name)
    

class MainHasBahCa(Screen):
    def __init__(self, session):
        Screen.__init__(self, session)
        self.session = session
        skin = os.path.join(path_skin, 'settings.xml')
        with codecs.open(skin, "r", encoding="utf-8") as f:
            self.skin = f.read()
        self.setup_title = ('Main HasBahCa')
        self.setTitle('HasBahCa')
        self['text'] = hasList([])
        self['title'] = Label('HasBahCa')
        self['info'] = Label(_('Give me a few seconds ... loading the data'))
        self['key_red'] = Button(_('Exit'))
        self['key_green'] = Button(_('Select'))
        self['key_yellow'] = Button(_('Update'))
        self["key_blue"] = Button(_('Remove'))
        self['key_green'].hide()
        self['key_yellow'].hide()
        self['key_blue'].hide()
        self['progress'] = ProgressBar()
        self['progresstext'] = StaticText()
        self["progress"].hide()
        self['live'] = Label()
        self.Update = False
        self['actions'] = ActionMap(['OkCancelActions',
                                     'ColorActions',
                                     'DirectionActions',
                                     'HotkeyActions',
                                     'InfobarEPGActions',
                                     'ChannelSelectBaseActions'], {'ok': self.okRun,
                                                                   'back': self.closerm,
                                                                   'cancel': self.closerm,
                                                                   'yellow': self.update_me,  # update_me,
                                                                   'green': self.okRun,
                                                                   'blue': self.msgdeleteBouquets,
                                                                   'yellow_long': self.update_dev,
                                                                   'info_long': self.update_dev,
                                                                   'infolong': self.update_dev,
                                                                   'showEventInfoPlugin': self.update_dev,
                                                                   'red': self.closerm}, -1)
        self.timer = eTimer()
        if os.path.exists('/var/lib/dpkg/status'):
            self.timer_conn = self.timer.timeout.connect(self.check_vers)
        else:
            self.timer.callback.append(self.check_vers)
        self.timer.start(500, 1)
        self.onLayoutFinish.append(self.updateMenuList)
        self.onLayoutFinish.append(self.__layoutFinished)

    def check_vers(self):
        remote_version = '0.0'
        remote_changelog = ''
        req = Utils.Request(Utils.b64decoder(installer_url), headers={'User-Agent': 'Mozilla/5.0'})
        page = Utils.urlopen(req).read()
        if PY3:
            data = page.decode("utf-8")
        else:
            data = page.encode("utf-8")
        if data:
            lines = data.split("\n")
            for line in lines:
                if line.startswith("version"):
                    remote_version = line.split("=")
                    remote_version = line.split("'")[1]
                if line.startswith("changelog"):
                    remote_changelog = line.split("=")
                    remote_changelog = line.split("'")[1]
                    break
        self.new_version = remote_version
        self.new_changelog = remote_changelog
        # if float(currversion) < float(remote_version):
        if currversion < remote_version:
            self.Update = True
            self['key_yellow'].show()
            # self['key_green'].show()
            self.session.open(MessageBox, _('New version %s is available\n\nChangelog: %s\n\nPress info_long or yellow_long button to start force updating.') % (self.new_version, self.new_changelog), MessageBox.TYPE_INFO, timeout=5)
        # self.update_me()

    def update_me(self):
        if self.Update is True:
            self.session.openWithCallback(self.install_update, MessageBox, _("New version %s is available.\n\nChangelog: %s \n\nDo you want to install it now?") % (self.new_version, self.new_changelog), MessageBox.TYPE_YESNO)
        else:
            self.session.open(MessageBox, _("Congrats! You already have the latest version..."),  MessageBox.TYPE_INFO, timeout=4)

    def update_dev(self):
        try:
            req = Utils.Request(Utils.b64decoder(developer_url), headers={'User-Agent': 'Mozilla/5.0'})
            page = Utils.urlopen(req).read()
            data = json.loads(page)
            remote_date = data['pushed_at']
            strp_remote_date = datetime.strptime(remote_date, '%Y-%m-%dT%H:%M:%SZ')
            remote_date = strp_remote_date.strftime('%Y-%m-%d')
            self.session.openWithCallback(self.install_update, MessageBox, _("Do you want to install update ( %s ) now?") % (remote_date), MessageBox.TYPE_YESNO)
        except Exception as e:
            print('error xcons:', e)

    def install_update(self, answer=False):
        if answer:
            cmd1 = 'wget -q "--no-check-certificate" ' + Utils.b64decoder(installer_url) + ' -O - | /bin/sh'
            self.session.open(xConsole, 'Upgrading...', cmdlist=[cmd1], finishedCallback=self.myCallback, closeOnSuccess=False)
        else:
            self.session.open(MessageBox, _("Update Aborted!"),  MessageBox.TYPE_INFO, timeout=3)

    def myCallback(self, result=None):
        print('result:', result)
        return

    def __layoutFinished(self):
        self.setTitle(self.setup_title)

    def closerm(self):
        Utils.deletetmp()
        self.close()

    def updateMenuList(self):
        global tyurl
        self.names = []
        self.urls = []
        idx = 0
        try:
            urlx = 'http://eviptv.com/m3u8/'
            # if tyurl is True:
                # urls = tyurl  # tyurl2
            print('urlx  ', urlx)
            content = Utils.make_request(urlx)
            # if six.PY3:
                # content = six.ensure_str(content)
            n1 = content.find('Directory</a>', 0)
            n2 = content.find('</body', n1)
            content2 = content[n1:n2]


            if six.PY3:
                # content2 = content2.decode("utf-8")
                content2 = six.ensure_str(content2)
            else:
                content2 = content2.encode("utf-8")
            if content2:

                # <tr><td valign="top">&nbsp;</td><td><a href="HasBahCa_ALL.m3u">HasBahCa_ALL.m3u</a>       </td><td align="right">2024-06-28 00:30  </td><td align="right"> 18M</td><td>&nbsp;</td></tr>
                # content3 = content2.replace('..&gt;', '')
                regexvideo = 'href="(.*?).m3u">(.*?)</a>.*?align.*?">(.*?)</td><td.*?</tr>'
                match = re.compile(regexvideo, re.DOTALL).findall(content2)
                for url, name, date in match:
                    name = name.replace('..', '').replace('HasBahCa_', '')
                    name = name.replace('&gt;', '').replace('_', ' ').replace('.m3u', '')
                    name = decodename(name)
                    name = '{}{}{}'.format(name, ' ', date)
                    url = '{}{}'.format(urlx, url + '.m3u')

                    self.names.append(name.strip())
                    self.urls.append(url.strip())
                    idx += 1
                print(len(self.names))
        except Exception as e:
            print('error HasBahCa1', str(e))

        # # don't work
        # try:
            # for root, dirs, files in os.walk(path_playlist):
                # for name in files:
                    # if '.m3u' not in name:
                        # continue
                    # # print('name ', name)
                    # namex = name.replace('.m3u', '').capitalize()
                    # self.names.append(namex)
                    # self.urls.append(path_playlist + '/' + name)
                    # idx += 1
        # except Exception as e:
            # print('error HasBahCa1', str(e))

        try:
            self['info'].setText(_('Please now select ...'))
            self["live"].setText('N.' + str(idx) + " CATEGORY")
            self['key_green'].show()
            self['key_blue'].show()
            showlisthasba(self.names, self['text'])
        except Exception as e:
            print('error HasBahCa1', str(e))

    def adultonly(self, answer=None):
        idx = self["text"].getSelectionIndex()
        name = self.names[idx]
        url = self.urls[idx]
        if answer is None:
            self.session.openWithCallback(self.adultonly, MessageBox, _("These streams may contain Adult content\n\nare you sure you want to continue?"), MessageBox.TYPE_YESNO)
        else:
            self.session.open(HasBahCa1, name, url)
        return

    def okRun(self):
        i = len(self.names)
        print('iiiiii= ', i)
        if i < 0:
            return
        idx = self["text"].getSelectionIndex()
        name = self.names[idx]
        url = self.urls[idx]
        if 'xxx' in name.lower() or 'porn' in name.lower() or 'adult' in name.lower():
            self.adultonly()
            return
        if 'parent' in name.lower():
            return
        elif 'hasbahcanetlink' in url:
            return
        elif '.txt' in name.lower():
            return
        elif 'category' in name.lower():
            self.session.open(HasBahCaC, name, url)
            print('url HasBahCa C : ', url)
        else:
            self.session.open(HasBahCa1, name, url)
            print('url HasBahCa 1 : ', url)

    def msgdeleteBouquets(self):
        self.session.openWithCallback(self.deleteBouquets, MessageBox, _("Remove all HasBahCa Favorite Bouquet ?"), MessageBox.TYPE_YESNO, timeout=5, default=True)

    def deleteBouquets(self, result):
        """
        Clean up routine to remove any previously made changes
        """
        if result:
            try:
                for fname in os.listdir(enigma_path):
                    if 'userbouquet.hbc_' in fname:
                        # os.remove(os.path.join(enigma_path, fname))
                        Utils.purge(enigma_path, fname)
                    elif 'bouquets.tv.bak' in fname:
                        # os.remove(os.path.join(enigma_path, fname))
                        Utils.purge(enigma_path, fname)
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
                self.session.open(MessageBox, _('HasBahCa Favorites List have been removed'), MessageBox.TYPE_INFO, timeout=5)
                Utils.ReloadBouquets()
            except Exception as ex:
                print(str(ex))
                raise


class HasBahCaC(Screen):
    def __init__(self, session, name, url):
        Screen.__init__(self, session)
        self.session = session
        skin = os.path.join(path_skin, 'settings.xml')
        with codecs.open(skin, "r", encoding="utf-8") as f:
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
        self['live'] = Label()
        self['actions'] = ActionMap(['OkCancelActions',
                                     'ColorActions',
                                     'ButtonSetupActions',
                                     'WizardActions', ], {'ok': self.okRun,
                                                          'green': self.okRun,
                                                          'red': self.close,
                                                          # 'yellow': self.convert,
                                                          # 'back': self.close(),
                                                          'cancel': self.close}, -2)
        self.timer = eTimer()
        if Utils.DreamOS():
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
        # items = []
        try:
            content = Utils.make_request(url)
            # if six.PY3:
                # content = six.ensure_str(content)
            print("HasBahCa t content =", content)
            print('urlll content: ', url)
            n1 = content.find('js-details-container Details">', 0)
            n2 = content.find('<div class="Details-content--shown Box-footer', n1)
            content2 = content[n1:n2]

            regexvideo = 'title="HasBahCa_(.*?).m3u.*?href="/HasBahCa/IPTV-LIST/blob/main/(.*?).m3u">.*?</a></span.*?</div>'
            match = re.compile(regexvideo, re.DOTALL).findall(content2)
            for name, url in match:
                if 'readme' in name.lower():
                    continue
                if 'enigma2' in name.lower():
                    continue
                url1 = '{}{}{}'.format(github, str(url), '.m3u')
                name1 = name.replace('HasBahCa', '°').replace('-', ' ').replace('_', ' ')
                name = decodename(name1)

                self.names.append(name.strip())
                self.urls.append(url1.strip())
            self["live"].setText('N.' + str(len(self.names)) + " CATEGORY")
            self['info'].setText(_('Please now select ...'))
            self['key_green'].show()
            showlisthasba(self.names, self['text'])
        except Exception as e:
            print('error ', str(e))
        print('-------------HasBahCa-------------')
        Utils.MemClean()
        print('-------------memclean-------------')

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
        skin = os.path.join(path_skin, 'settings.xml')
        with codecs.open(skin, "r", encoding="utf-8") as f:
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
        self["key_blue"] = Button('Search')
        self['key_green'].hide()
        self['key_yellow'].hide()
        self['key_blue'].hide()
        self['live'] = Label()
        self['progress'] = ProgressBar()
        self['progresstext'] = StaticText()
        self["progress"].hide()
        self.srefInit = self.session.nav.getCurrentlyPlayingServiceReference()
        global search_ok
        self.search = ''
        search_ok = False
        self['actions'] = ActionMap(['OkCancelActions',
                                     'ColorActions',
                                     'ButtonSetupActions',
                                     'WizardActions', ], {'ok': self.okRun,
                                                          'green': self.okRun,
                                                          'red': self.cancel,
                                                          'yellow': self.convert,
                                                          'blue': self.search_m3u,
                                                          'cancel': self.cancel}, -2)
        self.timer = eTimer()
        if Utils.DreamOS():
            self.timer_conn = self.timer.timeout.connect(self._gotPageLoad)
        else:
            self.timer.callback.append(self._gotPageLoad)
        self.timer.start(100, True)
        self.onLayoutFinish.append(self.__layoutFinished)

    def __layoutFinished(self):
        self.setTitle(self.setup_title)

    def search_m3u(self):
        from Screens.VirtualKeyBoard import VirtualKeyBoard
        self.session.openWithCallback(
            self.filterM3u,
            VirtualKeyBoard,
            title=_("Filter this category..."),
            text=self.search)

    def filterM3u(self, result):
        global search_ok
        if result:
            self.names = []
            self.urls = []
            self.pics = []
            search = result
            try:
                content = Utils.make_request(self.url)
                content = content.replace('$BorpasFileFormat="1"', '')

                if "#EXTM3U" and 'tvg-logo' in content:
                    regexcat = 'EXTINF.*?tvg-logo.*?,(.*?)\\n(.*?)\\n'
                    match = re.compile(regexcat, re.DOTALL).findall(content)
                    for name, url in match:
                        name = name.replace('_', ' ').replace('-', ' ')
                        if str(search).lower() in name.lower():
                            search_ok = True   
                        url = url.replace(' ', '').replace('\\n', '')
                        name = decodename(name)
                        self.names.append(str(name))
                        self.urls.append(str(url))
                else:
                    regexcat = '#EXTINF.*?,(.*?)\\n(.*?)\\n'
                    match = re.compile(regexcat, re.DOTALL).findall(content)
                    for name, url in match:
                        name = name.replace('_', ' ').replace('-', ' ')
                        
                        if str(search).lower() in name.lower():
                            search_ok = True                        
                            url = url.replace(' ', '').replace('\\n', '')
                            name = decodename(name)
                            self.names.append(str(name))
                            self.urls.append(str(url))
                    
                if search_ok is True:
                    showlisthasba(self.names, self['text'])
            except:
                self._gotPageLoad()
        else:
            self._gotPageLoad()

    def _gotPageLoad(self):
        global search_ok
        search_ok = False
        url = self.url
        print('self.url: ', self.url)
        self.names = []
        self.urls = []
        try:
            if plugin_path in url:
                f1 = open(url, "r")
                content = f1.read()
                f1.close()
            else:
                content = Utils.make_request(url)

            content = content.replace('$BorpasFileFormat="1"', '')

            if "#EXTM3U" and 'tvg-logo' in content:
                regexcat = 'EXTINF.*?tvg-logo.*?,(.*?)\\n(.*?)\\n'
                match = re.compile(regexcat, re.DOTALL).findall(content)
                for name, url in match:
                    name = name.replace('_', ' ').replace('-', ' ')
                    url = url.replace(' ', '').replace('\\n', '')
                    name = decodename(name)
                    self.names.append(str(name))
                    self.urls.append(str(url))
            else:
                regexcat = '#EXTINF.*?,(.*?)\\n(.*?)\\n'
                match = re.compile(regexcat, re.DOTALL).findall(content)
                for name, url in match:
                    name = name.replace('_', ' ').replace('-', ' ')
                    url = url.replace(' ', '').replace('\\n', '')
                    name = decodename(name)
                    self.names.append(str(name))
                    self.urls.append(str(url))

            self["live"].setText('N.' + str(len(self.names)) + " STREAM")
            self['info'].setText(_('Please now select ...'))
            self['key_green'].show()
            self['key_yellow'].show()
            self['key_blue'].show()
            showlisthasba(self.names, self['text'])
            Utils.MemClean()
        except Exception as e:
            print('error HasBahCa', str(e))

    def okRun(self):
        i = len(self.names)
        print('iiiiii= ', i)
        if i < 0:
            return
        idx = self["text"].getSelectionIndex()
        name = self.names[idx]
        url = self.urls[idx]
        self.session.open(Playgo, name, url)

    def convert(self, answer=None):
        i = len(self.names)
        if i < 0:
            return
        if answer is None:
            self.session.openWithCallback(self.convert, MessageBox, _("Do you want to Convert %s\nto Favorite Bouquet ?\n\nAttention!! Wait while converting !!!") % self.name)
        elif answer:
            self.type = 'tv'
            # if "radio" in self.name.lower():
                # self.type = "radio"
            name_file = self.name.replace('/', '_').replace(',', '').replace('hasbahca', 'hbc')
            cleanName = re.sub(r'[\<\>\:\"\/\\\|\?\*]', '_', str(name_file))
            cleanName = re.sub(r' ', '_', cleanName)
            cleanName = re.sub(r'\d+:\d+:[\d.]+', '_', cleanName)
            name_file = re.sub(r'_+', '_', cleanName)
            bouquetname = 'userbouquet.hbc_%s.%s' % (name_file.lower(), self.type.lower())
            print("Converting Bouquet %s" % name_file)
            if plugin_path in self.url:
                self.file = self.url
            else:
                self.file = "/tmp/tempm3u.m3u"
                if os.path.isfile(self.file):
                    os.remove(self.file)
                urlm3u = self.url.strip()
                if PY3:
                    urlm3u.encode()
                downloadFilest(urlm3u, self.file)
            sleep(5)
            path1 = '/etc/enigma2/' + str(bouquetname)
            path2 = '/etc/enigma2/bouquets.' + str(self.type.lower())
            service = '4097'
            ch = 0
            # try:
            if os.path.isfile(self.file) and os.stat(self.file).st_size > 0:
                print('ChannelList is_tmp exist in playlist')
                desk_tmp = ''
                in_bouquets = 0
                with open('%s' % path1, 'w+') as outfile:
                    outfile.write('#NAME %s\r\n' % name_file.capitalize())
                    for line in open(self.file):
                        if line.startswith('http://') or line.startswith('https'):
                            outfile.write('#SERVICE %s:0:1:1:0:0:0:0:0:0:%s' % (service, line.replace(':', '%3a')))
                            outfile.write('#DESCRIPTION %s' % desk_tmp)
                        elif line.startswith('#EXTINF'):
                            desk_tmp = '%s' % line.split(',')[-1]
                        elif '<stream_url><![CDATA' in line:
                            outfile.write('#SERVICE %s:0:1:1:0:0:0:0:0:0:%s\r\n' % (service, line.split('[')[-1].split(']')[0].replace(':', '%3a')))
                            outfile.write('#DESCRIPTION %s\r\n' % desk_tmp)
                        elif '<title>' in line:
                            if '<![CDATA[' in line:
                                desk_tmp = '%s\r\n' % line.split('[')[-1].split(']')[0]
                            else:
                                desk_tmp = '%s\r\n' % line.split('<')[1].split('>')[1]
                        ch += 1
                    outfile.close()
                if os.path.isfile(path2):
                    for line in open(path2):
                        if bouquetname in line:
                            in_bouquets = 1
                    if in_bouquets == 0:
                        if os.path.isfile('%s/%s' % (enigma_path, bouquetname)) and os.path.isfile('/etc/enigma2/bouquets.tv'):
                            Utils.remove_line(path2, bouquetname)
                            with open(path2, 'a+') as outfile:
                                outfile.write('#SERVICE 1:7:1:0:0:0:0:0:0:0:FROM BOUQUET "%s" ORDER BY bouquet\r\n' % bouquetname)
                                outfile.close()
                                in_bouquets = 1
                    Utils.ReloadBouquets()
                self.session.open(MessageBox, (_('Shuffle Favorite %s List in Progress') % ch) + '\n' + _('Wait please ...'), MessageBox.TYPE_INFO, timeout=5)

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
        self.session.openWithCallback(self.deleteBouquets, MessageBox, _("Remove all HasBahCa Favorite Bouquet ?"), MessageBox.TYPE_YESNO, timeout=5, default=True)

    def deleteBouquets(self, result):
        """
        Clean up routine to remove any previously made changes
        """
        if result:
            try:
                for fname in os.listdir(enigma_path):
                    if 'hbc_' in fname:
                        # os.remove(os.path.join(enigma_path, fname))
                        Utils.purge(enigma_path, fname)
                    elif 'bouquets.tv.bak' in fname:
                        # os.remove(os.path.join(enigma_path, fname))
                        Utils.purge(enigma_path, fname)
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
                    if 'hbc_' not in line:
                        tvfile.write(line)
                bakfile.close()
                tvfile.close()
                self.session.open(MessageBox, _('HasBahCa Favorites List have been removed'), MessageBox.TYPE_INFO, timeout=5)
                Utils.ReloadBouquets()
            except Exception as ex:
                print(str(ex))
                raise

    def cancel(self):
        if search_ok is True:
            self._gotPageLoad()
        else:
            # self.session.nav.stopService()
            # self.session.nav.playService(self.srefInit)
            self.close()


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
        self.name = html_conv.html_unescape(name)
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
        self['actions'] = ActionMap(['MoviePlayerActions',
                                     'MovieSelectionActions',
                                     'MediaPlayerActions',
                                     'EPGSelectActions',
                                     'MediaPlayerSeekActions',
                                     'ButtonSetupActions',
                                     'InfobarShowHideActions',
                                     'OkCancelActions',
                                     'InfobarActions',
                                     'InfobarSeekActions'], {'epg': self.showIMDB,
                                                             'info': self.showIMDB,
                                                             'tv': self.cicleStreamType,
                                                             'stop': self.leavePlayer,
                                                             'cancel': self.cancel,
                                                             'leavePlayer': self.cancel,
                                                             'down': self.av,
                                                             'back': self.cancel}, -1)
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
        return {0: '4:3 Letterbox',
                1: '4:3 PanScan',
                2: '16:9',
                3: '16:9 always',
                4: '16:10 Letterbox',
                5: '16:10 PanScan',
                6: '16:9 Letterbox'}[aspectnum]

    def setAspect(self, aspect):
        map = {0: '4_3_letterbox',
               1: '4_3_panscan',
               2: '16_9',
               3: '16_9_always',
               4: '16_10_letterbox',
               5: '16_10_panscan',
               6: '16_9_letterbox'}
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

    def showIMDB(self):
        text_clear = self.name
        if returnIMDB(text_clear):
            print('show imdb/tmdb')

    def slinkPlay(self, url):
        name = self.name
        ref = "{0}:{1}".format(url.replace(":", "%3a"), name.replace(":", "%3a"))
        print('final reference:   ', ref)
        sref = eServiceReference(ref)
        sref.setName(str(name))
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
        sref.setName(str(name))
        self.session.nav.stopService()
        self.session.nav.playService(sref)

    def cicleStreamType(self):
        global streml
        # streaml = False
        from itertools import cycle, islice
        self.servicetype = '4097'
        print('servicetype1: ', self.servicetype)
        url = str(self.url)
        if str(os.path.splitext(self.url)[-1]) == ".m3u8":
            if self.servicetype == "1":
                self.servicetype = "4097"
        currentindex = 0
        streamtypelist = ["4097"]
        '''
        # if "youtube" in str(self.url):
            # self.mbox = self.session.open(MessageBox, _('For Stream Youtube coming soon!'), MessageBox.TYPE_INFO, timeout=5)
            # return
        if Utils.isStreamlinkAvailable():
            streamtypelist.append("5002") #ref = '5002:0:1:0:0:0:0:0:0:0:http%3a//127.0.0.1%3a8088/' + url
            streaml = True
        if os.path.exists("/usr/bin/gstplayer"):
            streamtypelist.append("5001")
        if os.path.exists("/usr/bin/exteplayer3"):
            streamtypelist.append("5002")
        '''
        if os.path.exists("/usr/bin/apt-get"):
            streamtypelist.append("8193")
        for index, item in enumerate(streamtypelist, start=0):
            if str(item) == str(self.servicetype):
                currentindex = index
                break
        nextStreamType = islice(cycle(streamtypelist), currentindex + 1, None)
        self.servicetype = str(next(nextStreamType))
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
