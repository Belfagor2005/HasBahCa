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

# Python standard libraries
import codecs
import sys
from datetime import datetime
from json import loads
from os import listdir, path as os_path, remove, rename, stat, walk
from re import DOTALL, compile, findall, sub
from time import sleep

from six import ensure_str, text_type

# Enigma2 Components
from Components.ActionMap import ActionMap
from Components.Button import Button
from Components.Label import Label
from Components.MenuList import MenuList
from Components.MultiContent import (
    MultiContentEntryPixmapAlphaTest,
    MultiContentEntryText,
)
from Components.config import config
from Components.ProgressBar import ProgressBar
from Components.ServiceEventTracker import InfoBarBase, ServiceEventTracker
from Components.Sources.StaticText import StaticText

# Enigma2 Screens
from Screens.ChoiceBox import ChoiceBox
from Screens.InfoBarGenerics import (
    InfoBarAudioSelection,
    InfoBarMenu,
    InfoBarNotifications,
    InfoBarSeek,
    InfoBarSubtitleSupport,
)
from Screens.MessageBox import MessageBox
from Screens.Screen import Screen

# Enigma2 Tools
from Tools.Directories import SCOPE_PLUGINS, resolveFilename
from Tools.Downloader import downloadWithProgress

# Enigma2 Enigma core
from enigma import (
    RT_HALIGN_LEFT,
    RT_VALIGN_CENTER,
    eListboxPythonMultiContent,
    eServiceReference,
    eTimer,
    gFont,
    getDesktop,
    iPlayableService,
    loadPNG,
)

# Plugin internals
from .__init__ import _, isDreamOS
from .lib import Utils, html_conv
from .lib.Console import Console as xConsole

global downloadhasba

try:
    from urllib2 import urlopen, Request, URLError, HTTPError
except BaseException:
    from urllib.error import URLError, HTTPError
    from urllib.request import urlopen, Request

try:
    from Components.UsageConfig import defaultMoviePath
    downloadhasba = defaultMoviePath()
except BaseException:
    if os_path.exists("/usr/bin/apt-get"):
        downloadhasba = ('/media/hdd/movie/')

if sys.version_info >= (2, 7, 9):
    try:
        import ssl
        sslContext = ssl._create_unverified_context()
    except BaseException:
        sslContext = None


currversion = '2.0'
PY3 = sys.version_info.major >= 3
hostcategoryes = 'https://github.com/HasBahCa/IPTV-LIST/'
github = 'https://raw.githubusercontent.com/HasBahCa/IPTV-LIST/main/'
tyurl1 = 'http://eviptv.com/m3u/'
tyurl2 = 'https://hasbahca.net/hasbahca_m3u/'
tyurl3 = tyurl1 + 'M3U_Listeleri/'
plugin_path = resolveFilename(
    SCOPE_PLUGINS,
    "Extensions/{}".format('HasBahCa'))
enigma_path = '/etc/enigma2'
path_playlist = os_path.join(plugin_path, 'Playlists')
installer_url = 'aHR0cHM6Ly9yYXcuZ2l0aHVidXNlcmNvbnRlbnQuY29tL0JlbGZhZ29yMjAwNS9IYXNCYWhDYS9tYWluL2luc3RhbGxlci5zaA=='
developer_url = 'aHR0cHM6Ly9hcGkuZ2l0aHViLmNvbS9yZXBvcy9CZWxmYWdvcjIwMDUvSGFzQmFoQ2E='
aspect_manager = Utils.AspectManager()
downloadhasba = None


def ssl_urlopen(url):
    if sslContext:
        return urlopen(url, context=sslContext)
    else:
        return urlopen(url)


def downloadFilest(url, target):
    try:
        req = Request(url)
        req.add_header(
            'User-Agent',
            'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
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


sslverify = False
try:
    from twisted.internet import ssl
    from twisted.internet._sslverify import ClientTLSOptions
    sslverify = True
except ImportError:
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
    path_skin = os_path.join(plugin_path, 'res/skins/uhd')
elif screenwidth.width() == 1920:
    path_skin = os_path.join(plugin_path, 'res/skins/fhd')
else:
    path_skin = os_path.join(plugin_path, 'res/skins/hd')
if isDreamOS:
    path_skin = os_path.join(path_skin, 'dreamOs')

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
    png = os_path.join(plugin_path, 'res/pics/tv.png')
    if any(s in name.lower() for s in EXTCAM):
        png = os_path.join(plugin_path, 'res/pics/webcam.png')
    elif any(s in name.lower() for s in EXTRAD):
        png = os_path.join(plugin_path, 'res/pics/radio.png')
    elif any(s in name.lower() for s in EXTXXX):
        png = os_path.join(plugin_path, 'res/pics/xxx.png')
    elif any(s in name.lower() for s in EXTMUS):
        png = os_path.join(plugin_path, 'res/pics/music.png')
    elif any(s in name.lower() for s in EXTRLX):
        png = os_path.join(plugin_path, 'res/pics/relax.png')
    elif any(s in name.lower() for s in EXTMOV):
        png = os_path.join(plugin_path, 'res/pics/movie.png')
    elif any(s in name.lower() for s in EXTSPOR):
        png = os_path.join(plugin_path, 'res/pics/sport.png')
    elif 'pluto' in name.lower():
        png = os_path.join(plugin_path, 'res/pics/plutotv.png')
    elif 'tvplus' in name.lower():
        png = os_path.join(plugin_path, 'res/pics/tvplus.png')
    elif '~~~~' in name.lower():
        png = os_path.join(plugin_path, 'res/pics/mark.png')
    else:
        png = os_path.join(plugin_path, 'res/pics/tv.png')

    if screenwidth.width() == 2560:
        res.append(
            MultiContentEntryPixmapAlphaTest(
                pos=(
                    5, 5), size=(
                    50, 50), png=loadPNG(png)))
        res.append(
            MultiContentEntryText(
                pos=(
                    90,
                    0),
                size=(
                    1200,
                    60),
                font=0,
                text=name,
                color=0xa6d1fe,
                flags=RT_HALIGN_LEFT | RT_VALIGN_CENTER))
    elif screenwidth.width() == 1920:
        res.append(
            MultiContentEntryPixmapAlphaTest(
                pos=(
                    5, 5), size=(
                    40, 40), png=loadPNG(png)))
        res.append(
            MultiContentEntryText(
                pos=(
                    70,
                    0),
                size=(
                    1000,
                    50),
                font=0,
                text=name,
                color=0xa6d1fe,
                flags=RT_HALIGN_LEFT | RT_VALIGN_CENTER))
    else:
        res.append(
            MultiContentEntryPixmapAlphaTest(
                pos=(
                    3, 5), size=(
                    40, 40), png=loadPNG(png)))
        res.append(
            MultiContentEntryText(
                pos=(
                    50,
                    0),
                size=(
                    500,
                    50),
                font=0,
                text=name,
                color=0xa6d1fe,
                flags=RT_HALIGN_LEFT | RT_VALIGN_CENTER))

    return res


def showlisthasba(data, list_widget):
    icount = 0
    plist = []
    for line in data:
        name = data[icount]
        plist.append(hasbaSetListEntry(name))
        icount += 1
    list_widget.setList(plist)


def returnIMDB(text_clear):
    text = html_conv.html_unescape(text_clear)

    if Utils.is_TMDB and Utils.TMDB:
        try:
            _session.open(Utils.TMDB.tmdbScreen, text, 0)
        except Exception as e:
            print("[XCF] TMDB error:", str(e))
        return True

    elif Utils.is_tmdb and Utils.tmdb:
        try:
            _session.open(Utils.tmdb.tmdbScreen, text, 0)
        except Exception as e:
            print("[XCF] tmdb error:", str(e))
        return True

    elif Utils.is_imdb and Utils.imdb:
        try:
            Utils.imdb(_session, text)
        except Exception as e:
            print("[XCF] IMDb error:", str(e))
        return True

    _session.open(MessageBox, text, MessageBox.TYPE_INFO)
    return True


def decodename(name, fallback=''):
    import unicodedata
    if isinstance(name, text_type):
        name = name.encode('utf-8')
    name = unicodedata.normalize(
        'NFKD', text_type(
            name, 'utf_8', errors='ignore')).encode(
        'ASCII', 'ignore')
    name = sub(b'[^a-z0-9-_]', b' ', name.lower())
    if not name:
        name = fallback
    return ensure_str(name)


def saveM3u(dwn, url):
    with open(dwn, 'w') as f:
        f.write(url.read())
        f.flush()
        f.close()
        file_size = os_path.getsize(dwn)
        if file_size == 0:
            remove(dwn)
        else:
            print('downlaoded:', dwn)
    return


class MainHasBahCa(Screen):
    def __init__(self, session):
        Screen.__init__(self, session)
        self.session = session
        skin = os_path.join(path_skin, 'settings.xml')
        with codecs.open(skin, "r", encoding="utf-8") as f:
            self.skin = f.read()
        self.setup_title = ('Main HasBahCa')
        self.setTitle('HasBahCa')
        self['text'] = hasList([])
        self['title'] = Label('HasBahCa')
        self['info'] = Label(_('Give me a few seconds ... loading the data'))
        self['key_red'] = Button(_('Exit'))
        self['key_green'] = Button(_('Select'))
        self['key_yellow'] = Button(_('Options'))
        self["key_blue"] = Button(_('Remove'))
        self['key_green'].hide()
        # self['key_yellow'].hide()
        self['key_blue'].hide()
        self['progress'] = ProgressBar()
        self['progresstext'] = StaticText()
        self["progress"].hide()
        self['live'] = Label()
        self.Update = False
        self['actions'] = ActionMap(
            [
                'OkCancelActions',
                'DirectionActions',
                'HotkeyActions',
                'InfobarEPGActions',
                'ChannelSelectBaseActions'
            ],
            {
                'ok': self.okRun,
                'back': self.closerm,
                'cancel': self.closerm,
                # 'yellow': self.update_me,  # update_me,
                'yellow': self.onYellowPressed,
                'green': self.okRun,
                'blue': self.msgdeleteBouquets,
                'yellow_long': self.update_dev,
                'info_long': self.update_dev,
                'infolong': self.update_dev,
                'showEventInfoPlugin': self.update_dev,
                'red': self.closerm
            },
            -1
        )
        self.timer = eTimer()
        if os_path.exists("/usr/bin/apt-get"):
            self.timer_conn = self.timer.timeout.connect(self.check_vers)
        else:
            self.timer.callback.append(self.check_vers)
        self.timer.start(500, 1)
        self.onLayoutFinish.append(self.updateMenuList)
        self.onLayoutFinish.append(self.__layoutFinished)

    def onYellowPressed(self):
        """Handle yellow button press - show update choice menu"""
        menu = [
            (_("Update M3U Playlists from GitHub"), "playlists"),
            (_("Update Plugin to new version"), "plugin"),
            (_("Force Update (Developer)"), "developer")
        ]

        self.session.openWithCallback(
            self.onUpdateChoice,
            ChoiceBox,
            title=_("Select update type:"),
            list=menu
        )

    def onUpdateChoice(self, choice):
        """Handle update choice selection"""
        if choice is not None:
            if choice[1] == "playlists":
                self.update_playlists_from_github()
            elif choice[1] == "plugin":
                self.update_me()
            elif choice[1] == "developer":
                self.update_dev()

    def check_vers(self):
        """
        Check the latest version and changelog from the remote installer URL.
        If a new version is available, notify the user.
        """
        remote_version = '0.0'
        remote_changelog = ''
        try:
            req = Utils.Request(
                Utils.b64decoder(installer_url), headers={
                    'User-Agent': 'Mozilla/5.0'})
            page = Utils.urlopen(req).read()
            data = page.decode("utf-8") if PY3 else page.encode("utf-8")
            if data:
                lines = data.split("\n")
                for line in lines:
                    if line.startswith("version"):
                        remote_version = line.split(
                            "'")[1] if "'" in line else '0.0'
                    elif line.startswith("changelog"):
                        remote_changelog = line.split(
                            "'")[1] if "'" in line else ''
                        break
        except Exception as e:
            self.session.open(
                MessageBox, _('Error checking version: %s') %
                str(e), MessageBox.TYPE_ERROR, timeout=5)
            return
        self.new_version = remote_version
        self.new_changelog = remote_changelog
        if currversion < remote_version:
            self.Update = True
            # self['key_yellow'].show()
            self.session.open(
                MessageBox,
                _('New version %s is available\n\nChangelog: %s\n\nPress info_long or yellow_long button to start force updating.') %
                (self.new_version,
                 self.new_changelog),
                MessageBox.TYPE_INFO,
                timeout=5)

    def update_me(self):
        if self.Update is True:
            self.session.openWithCallback(
                self.install_update,
                MessageBox,
                _("New version %s is available.\n\nChangelog: %s \n\nDo you want to install it now?") %
                (self.new_version,
                 self.new_changelog),
                MessageBox.TYPE_YESNO)
        else:
            self.session.open(
                MessageBox,
                _("Congrats! You already have the latest version..."),
                MessageBox.TYPE_INFO,
                timeout=4)

    def update_dev(self):
        """
        Check for updates from the developer's URL and prompt the user to install the latest update.
        """
        try:
            req = Utils.Request(
                Utils.b64decoder(developer_url), headers={
                    'User-Agent': 'Mozilla/5.0'})
            page = Utils.urlopen(req).read()
            data = loads(page)
            remote_date = data['pushed_at']
            strp_remote_date = datetime.strptime(
                remote_date, '%Y-%m-%dT%H:%M:%SZ')
            remote_date = strp_remote_date.strftime('%Y-%m-%d')
            self.session.openWithCallback(
                self.install_update,
                MessageBox,
                _("Do you want to install update ( %s ) now?") %
                (remote_date),
                MessageBox.TYPE_YESNO)
        except Exception as e:
            print('error xcons:', e)

    def install_update(self, answer=False):
        if answer:
            cmd1 = 'wget -q "--no-check-certificate" ' + \
                Utils.b64decoder(installer_url) + ' -O - | /bin/sh'
            self.session.open(
                xConsole,
                'Upgrading...',
                cmdlist=[cmd1],
                finishedCallback=self.myCallback,
                closeOnSuccess=False)
        else:
            self.session.open(
                MessageBox,
                _("Update Aborted!"),
                MessageBox.TYPE_INFO,
                timeout=3)

    def myCallback(self, result=None):
        print('result:', result)
        return

    def __layoutFinished(self):
        self.setTitle(self.setup_title)

    def update_playlists_from_github(self):
        """Download ALL M3U files from GitHub Playlists folder"""
        self.session.openWithCallback(
            self._download_all_m3u_files,
            MessageBox,
            _("Do you want to download ALL M3U playlists from GitHub?\n\nThis will download all .m3u files from HasBahCa repository."),
            MessageBox.TYPE_YESNO)

    def _download_all_m3u_files(self, answer):
        if not answer:
            return

        # Show progress
        self['info'].setText(_("Downloading ALL playlists..."))
        self['key_green'].hide()
        self['key_yellow'].hide()
        self['key_blue'].hide()

        try:
            # Use GitHub API to get ALL files from the folder
            api_url = "https://api.github.com/repos/Belfagor2005/HasBahCa/contents/usr/lib/enigma2/python/Plugins/Extensions/HasBahCa/Playlists"

            req = Request(api_url)
            req.add_header('User-Agent', 'Mozilla/5.0')
            req.add_header('Accept', 'application/vnd.github.v3+json')

            if sslContext:
                response = urlopen(req, context=sslContext)
            else:
                response = urlopen(req)

            if PY3:
                content = response.read().decode('utf-8')
            else:
                content = response.read()

            response.close()

            files_data = loads(content)

            # Create Playlists directory if it doesn't exist
            if not os_path.exists(path_playlist):
                try:
                    from os import makedirs
                    makedirs(path_playlist)
                except Exception as e:
                    print("Error creating directory:", str(e))

            download_count = 0
            failed_count = 0
            # skipped_count = 0

            # Download each .m3u file
            for item in files_data:
                try:
                    if item['type'] == 'file' and item['name'].lower().endswith(
                            '.m3u'):
                        download_url = item['download_url']
                        local_path = os_path.join(path_playlist, item['name'])

                        print("Downloading:", item['name'])

                        # Download the file
                        file_req = Request(download_url)
                        file_req.add_header('User-Agent', 'Mozilla/5.0')

                        if sslContext:
                            file_response = urlopen(
                                file_req, context=sslContext)
                        else:
                            file_response = urlopen(file_req)

                        if PY3:
                            file_data = file_response.read()
                        else:
                            file_data = file_response.read()

                        # Save file
                        with open(local_path, 'wb') as f:
                            f.write(file_data)

                        file_response.close()
                        download_count += 1
                        print("Downloaded:", item['name'])

                except Exception as e:
                    print(
                        "Failed to download", item.get(
                            'name', 'unknown'), ":", str(e))
                    failed_count += 1

            # Show result
            message = _("Download completed!\n\n")
            message += _("Successfully downloaded: %d files\n") % download_count
            message += _("Failed: %d files\n") % failed_count

            if download_count == 0 and failed_count > 0:
                message += _("\nTrying alternative method...")
                self.session.open(
                    MessageBox,
                    message,
                    MessageBox.TYPE_INFO,
                    timeout=3)
                # Try alternative method
                self._alternative_download_method()
            else:
                self.session.open(
                    MessageBox,
                    message,
                    MessageBox.TYPE_INFO,
                    timeout=5)

            # Reload lists
            self.updateMenuList()

        except Exception as e:
            print("GitHub API failed:", str(e))
            # Try alternative method
            self._alternative_download_method()

    def _alternative_download_method(self):
        """Alternative method using web scraping if API fails"""
        try:
            # GitHub raw folder URL
            import urllib

            # First, get the directory listing
            github_url = "https://github.com/Belfagor2005/HasBahCa/tree/main/usr/lib/enigma2/python/Plugins/Extensions/HasBahCa/Playlists"

            req = Request(github_url)
            req.add_header('User-Agent', 'Mozilla/5.0')

            if sslContext:
                response = urlopen(req, context=sslContext)
            else:
                response = urlopen(req)

            if PY3:
                html_content = response.read().decode('utf-8')
            else:
                html_content = response.read()

            response.close()

            # Simple pattern to find .m3u files in GitHub HTML
            # Pattern for GitHub file links
            pattern = r'<a[^>]*href="[^"]*/Playlists/([^"]+\.m3u)"[^>]*>'
            m3u_files = findall(pattern, html_content)

            # If pattern doesn't work, try another
            if not m3u_files:
                pattern = r'[^/"\']+\.m3u'
                all_matches = findall(pattern, html_content)
                m3u_files = [f for f in all_matches if f.endswith('.m3u')]

            # Remove duplicates
            unique_files = []
            for file in m3u_files:
                if file not in unique_files and file.endswith('.m3u'):
                    unique_files.append(file)

            raw_base = "https://raw.githubusercontent.com/Belfagor2005/HasBahCa/main/usr/lib/enigma2/python/Plugins/Extensions/HasBahCa/Playlists/"
            download_count = 0

            # Ensure directory exists
            if not os_path.exists(path_playlist):
                try:
                    from os import makedirs
                    makedirs(path_playlist)
                except BaseException:
                    pass

            for m3u_file in unique_files:
                try:
                    # URL encode the filename for special characters
                    if PY3:
                        import urllib.parse
                        encoded_file = urllib.parse.quote(m3u_file)
                    else:
                        import urllib
                        encoded_file = urllib.quote(m3u_file)

                    raw_url = raw_base + encoded_file
                    local_path = os_path.join(path_playlist, m3u_file)

                    print("Trying to download:", m3u_file)

                    # Try to download
                    req = Request(raw_url)
                    req.add_header('User-Agent', 'Mozilla/5.0')

                    if sslContext:
                        file_response = urlopen(req, context=sslContext)
                    else:
                        file_response = urlopen(req)

                    if PY3:
                        file_data = file_response.read()
                    else:
                        file_data = file_response.read()

                    # Check if it's a valid file
                    if len(file_data) > 50:  # At least 50 bytes
                        with open(local_path, 'wb') as f:
                            f.write(file_data)
                        download_count += 1
                        print("Downloaded:", m3u_file)

                    file_response.close()

                except Exception as e:
                    print("Failed:", m3u_file, "-", str(e))
                    continue

            # Show final result
            message = _("Alternative method completed!\n\n")
            message += _("Downloaded: %d files") % download_count
            self.session.open(
                MessageBox,
                message,
                MessageBox.TYPE_INFO,
                timeout=5)

            # Reload lists
            self.updateMenuList()

        except Exception as e:
            error_msg = _("Both methods failed!\n\nError: %s") % str(e)
            self.session.open(
                MessageBox,
                error_msg,
                MessageBox.TYPE_ERROR,
                timeout=10)

        finally:
            # Always restore buttons
            self['key_green'].show()
            self['key_blue'].show()
            if self.Update:
                self['key_yellow'].show()
            self['info'].setText(_('Please now select ...'))

    def closerm(self):
        Utils.deletetmp()
        self.close()

    def updateMenuList(self):
        self.names = []
        self.urls = []
        idx = 0
        try:
            urlx = 'http://eviptv.com/m3u8/'
            print('urlx  ', urlx)
            content = Utils.make_request(urlx)

            n1 = content.find('Directory</a>', 0)
            n2 = content.find('</body', n1)
            content2 = content[n1:n2]

            if PY3:
                content2 = ensure_str(content2)
            else:
                content2 = content2.encode("utf-8")

            if content2:
                regexvideo = 'href="(.*?).m3u">(.*?)</a>.*?align.*?">(.*?)</td><td.*?</tr>'
                match = compile(regexvideo, DOTALL).findall(content2)
                for url, name, date in match:
                    name = name.replace('..', '').replace('HasBahCa_', '')
                    name = name.replace(
                        '&gt;',
                        '').replace(
                        '_',
                        ' ').replace(
                        '.m3u',
                        '')
                    # name = decodename(name)
                    name = '{}{}{}'.format(name, ' ', date)
                    url = '{}{}'.format(urlx, url + '.m3u')
                    self.names.append(name.strip())
                    self.urls.append(url.strip())
                    idx += 1
                print(len(self.names))

            # local files to playlist folder
            for root, dirs, files in walk(path_playlist):
                for name in files:
                    if '.m3u' not in name:
                        continue
                    # print('name ', name)
                    namex = '(Local) ' + name.replace('.m3u', '').capitalize()
                    self.names.append(namex)
                    self.urls.append(path_playlist + '/' + name)
                    idx += 1

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
            self.session.openWithCallback(
                self.adultonly,
                MessageBox,
                _("These streams may contain Adult content\n\nare you sure you want to continue?"),
                MessageBox.TYPE_YESNO)
        else:
            self.session.open(HasBahCa1, name, url)
        return

    def okRun(self):
        i = len(self.names)
        print('Count = ', i)
        if i < 0:
            return

        idx = self["text"].getSelectionIndex()
        name = self.names[idx]
        url = self.urls[idx]

        # Adult content check
        adult_keywords = [
            'xxx', 'porn', 'adult', 'sex', 'erotic', '18+', 'adults',
            'porno', 'nsfw', 'xxx-adult', 'xxx-adults', 'adult-only',
            'adultxxx', 'xxxadult', 'pornxxx', 'xxxporn'
        ]

        # Also check without spaces or punctuation
        def clean_name(name):
            """Removes spaces and punctuation"""
            import re
            return re.sub(r'[^\w]', '', name.lower())

        name_clean = clean_name(name)
        is_adult = any(keyword in name_clean for keyword in adult_keywords)

        if is_adult:
            # Check if parental control is configured
            try:
                # Check various possible configurations
                parental_configured = False

                # Method 1: standard check
                if hasattr(config.ParentalControl, 'configured'):
                    parental_configured = config.ParentalControl.configured.value

                # Method 2: alternative check
                elif hasattr(config.ParentalControl, 'servicepinactive'):
                    parental_configured = config.ParentalControl.servicepinactive.value

                # Method 3: check if any parental PIN section exists
                elif hasattr(config.ParentalControl, 'config_sections'):
                    # If there are configured sections, parental control is
                    # probably active
                    parental_configured = len(
                        config.ParentalControl.config_sections) > 0

                if parental_configured:
                    # Parental control active - ask for PIN
                    from Screens.ParentalControlSetup import ParentalControl
                    parental_control = ParentalControl(self.session)
                    parental_control.verifyPin(
                        callback=self._adult_verified,
                        callback_args=(name, url)
                    )
                else:
                    # Parental control not configured - ask confirmation
                    self.adultonly()

            except Exception as e:
                print('Parental control error:', str(e))
                # Fallback to simple confirmation
                self.adultonly()

            return

        # Existing checks...
        if 'parent' in name.lower():
            return
        elif 'hasbahcanetlink' in url:
            return
        elif '.txt' in name.lower():
            return
        elif 'category' in name.lower():
            self.session.open(HasBahCaC, name, url)
            print('HasBahCa C URL: ', url)
        else:
            self.session.open(HasBahCa1, name, url)
            print('HasBahCa 1 URL: ', url)

    def _adult_verified(self, result, name, url):
        """Callback after parental control PIN verification"""
        if result:
            # Correct PIN - open content
            self.session.open(HasBahCa1, name, url)
        else:
            # Wrong PIN or operation cancelled
            self.session.open(
                MessageBox,
                _("Access denied or wrong PIN"),
                MessageBox.TYPE_ERROR,
                timeout=3
            )

    def msgdeleteBouquets(self):
        self.session.openWithCallback(
            self.deleteBouquets,
            MessageBox,
            _("Remove all HasBahCa Favorite Bouquet ?"),
            MessageBox.TYPE_YESNO,
            timeout=5,
            default=True)

    def deleteBouquets(self, result):
        """
        Clean up routine to remove any previously made changes
        """
        if result:
            try:
                for fname in listdir(enigma_path):
                    if 'userbouquet.hbc_' in fname:
                        Utils.purge(enigma_path, fname)
                    elif 'bouquets.tv.bak' in fname:
                        Utils.purge(enigma_path, fname)
                rename(
                    os_path.join(
                        enigma_path, 'bouquets.tv'), os_path.join(
                        enigma_path, 'bouquets.tv.bak'))
                with open(os_path.join(enigma_path, 'bouquets.tv.bak'), 'r') as bakfile:
                    with open(os_path.join(enigma_path, 'bouquets.tv'), 'w+') as tvfile:
                        for line in bakfile:
                            if '.hbc_' not in line:
                                tvfile.write(line)
                self.session.open(
                    MessageBox,
                    _('HasBahCa Favorites List have been removed'),
                    MessageBox.TYPE_INFO,
                    timeout=5)
                Utils.ReloadBouquets()
            except Exception as ex:
                print(str(ex))
                raise
        return


class HasBahCaC(Screen):
    def __init__(self, session, name, url):
        Screen.__init__(self, session)
        self.session = session
        skin = os_path.join(path_skin, 'settings.xml')
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
        self['actions'] = ActionMap(
            [
                'OkCancelActions',
                'HotkeyActions',
                'ButtonSetupActions',
                'WizardActions'
            ],
            {
                'ok': self.okRun,
                'green': self.okRun,
                'red': self.close,
                # 'yellow': self.convert,
                # 'back': self.close(),
                'cancel': self.close
            },
            -2
        )
        self.timer = eTimer()
        if isDreamOS:
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
        try:
            content = Utils.make_request(url)
            n1 = content.find('js-details-container Details">', 0)
            n2 = content.find(
                '<div class="Details-content--shown Box-footer', n1)
            content2 = content[n1:n2]

            regexvideo = 'title="HasBahCa_(.*?).m3u.*?href="/HasBahCa/IPTV-LIST/blob/main/(.*?).m3u">.*?</a></span.*?</div>'
            match = compile(regexvideo, DOTALL).findall(content2)
            for name, url in match:
                if 'readme' in name.lower():
                    continue
                if 'enigma2' in name.lower():
                    continue
                url1 = '{}{}{}'.format(github, str(url), '.m3u')
                name = name.replace(
                    'HasBahCa',
                    '°').replace(
                    '-',
                    ' ').replace(
                    '_',
                    ' ')
                # name = decodename(name)
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
        i = len(self.names)
        if i < 0:
            return
        idx = self["text"].getSelectionIndex()
        name = self.names[idx]
        url = self.urls[idx]
        self.session.open(HasBahCa1, name, url)


class HasBahCa1(Screen):
    def __init__(self, session, sel, url):
        self.session = session
        Screen.__init__(self, session)
        skin = os_path.join(path_skin, 'settings.xml')
        with codecs.open(skin, "r", encoding="utf-8") as f:
            self.skin = f.read()
        self.setup_title = ('HasBahCa TV')
        global search_ok
        self.search = ''
        search_ok = False
        self.list = []
        self.name = sel
        self.url = url
        self.type = None
        self.currentList = 'list'

        self.srefInit = self.session.nav.getCurrentlyPlayingServiceReference()
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
        self['actions'] = ActionMap(
            [
                'OkCancelActions',
                'ColorActions',
                'ButtonSetupActions',
                'WizardActions'
            ],
            {
                'ok': self.okRun,
                'green': self.okRun,
                'red': self.cancel,
                'yellow': self.convert,
                'blue': self.search_m3u,
                'cancel': self.cancel
            },
            -2
        )
        self.timer = eTimer()
        if isDreamOS:
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
                regexcat = '#EXTINF.*?,(.*?)\\n(.*?)\\n'
                match = compile(regexcat, DOTALL).findall(content)
                for name, url in match:
                    name = name.replace(
                        '"', '').replace(
                        '-', ' ')  # .replace('-', ' ')
                    if str(search).lower() in name.lower():
                        search_ok = True
                        self.names.append(str(name))
                        self.urls.append(str(url))

                if search_ok is True:
                    showlisthasba(self.names, self['text'])
            except BaseException:
                self._gotPageLoad()
        else:
            self._gotPageLoad()

    def _gotPageLoad(self):
        global search_ok
        search_ok = False
        url = self.url
        self.names = []
        self.urls = []
        try:
            if plugin_path in url:
                try:
                    with open(url, "r") as f1:
                        content = f1.read()
                except IOError as e:
                    print("Error opening file %s: %s" % (url, str(e)))
                    content = ""
            else:
                content = Utils.make_request(url)

            content = content.replace('$BorpasFileFormat="1"', "")

            regexcat = '#EXTINF.*?,(.*?)\\n(.*?)\\n'
            match = compile(regexcat, DOTALL).findall(content)
            for name, url in match:
                name = name.replace('_', ' ').replace('-', ' ')
                self.names.append(str(name))
                self.urls.append(str(url))

            self["live"].setText('N.' + str(len(self.names)) + " STREAM")
            self['info'].setText(_('Please now select ...'))
            self['key_green'].show()
            self['key_yellow'].show()
            self['key_blue'].show()
            showlisthasba(self.names, self['text'])

            self.currentList = [(name, url)
                                for name, url in zip(self.names, self.urls)]

            print('self names=', self.names)
            print('self currentlist=', self.currentList)
            Utils.MemClean()
        except Exception as e:
            print('error HasBahCa', str(e))

    def okRun(self):
        try:
            i = self['text'].getSelectedIndex()
            self.currentindex = i
            selection = self['text'].l.getCurrentSelection()
            if selection is not None:
                item = self.currentList[i]
                name = item[0]
                url = item[1]
            self.play_that_shit(
                url,
                name,
                self.currentindex,
                item,
                self.currentList)
        except Exception as error:
            print('error as:', error)

    def play_that_shit(self, url, name, index, item, currentList):
        self.session.open(Playgo, name, url, index, item, currentList)

    def convert(self, answer=None):
        i = len(self.names)
        if i < 0:
            return
        if answer is None:
            self.session.openWithCallback(
                self.convert,
                MessageBox,
                _("Do you want to Convert %s\nto Favorite Bouquet ?\n\nAttention!! Wait while converting !!!") %
                self.name)
        elif answer:
            self.type = 'tv'
            name_file = self.name.replace(
                '/',
                '_').replace(
                ',',
                '').replace(
                'hasbahca',
                'hbc')
            cleanName = sub(r'[\<\>\:\"\/\\\|\?\*]', '_', str(name_file))
            cleanName = sub(r' ', '_', cleanName)
            cleanName = sub(r'\d+:\d+:\d+(?:\.\d+)*', '_', cleanName)
            name_file = sub(r'_+', '_', cleanName)
            bouquetname = 'userbouquet.hbc_%s.%s' % (
                name_file.lower(), self.type.lower())
            print("Converting Bouquet %s" % name_file)
            if plugin_path in self.url:
                self.file = self.url
            else:
                self.file = "/tmp/tempm3u.m3u"
                if os_path.isfile(self.file):
                    remove(self.file)
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
            if os_path.isfile(self.file) and stat(self.file).st_size > 0:
                print('ChannelList is_tmp exist in playlist')
                desk_tmp = ''
                in_bouquets = 0
                with open('%s' % path1, 'w+') as outfile:
                    outfile.write('#NAME %s\r\n' % name_file.capitalize())
                    for line in open(self.file):
                        if line.startswith(
                                'http://') or line.startswith('https'):
                            outfile.write(
                                '#SERVICE %s:0:1:1:0:0:0:0:0:0:%s' %
                                (service, line.replace(
                                    ':', '%3a')))
                            outfile.write('#DESCRIPTION %s' % desk_tmp)
                        elif line.startswith('#EXTINF'):
                            desk_tmp = '%s' % line.split(',')[-1]
                        elif '<stream_url><![CDATA' in line:
                            outfile.write('#SERVICE %s:0:1:1:0:0:0:0:0:0:%s\r\n' % (
                                service, line.split('[')[-1].split(']')[0].replace(':', '%3a')))
                            outfile.write('#DESCRIPTION %s\r\n' % desk_tmp)
                        elif '<title>' in line:
                            if '<![CDATA[' in line:
                                desk_tmp = '%s\r\n' % line.split(
                                    '[')[-1].split(']')[0]
                            else:
                                desk_tmp = '%s\r\n' % line.split(
                                    '<')[1].split('>')[1]
                        ch += 1
                    outfile.close()
                if os_path.isfile(path2):
                    for line in open(path2):
                        if bouquetname in line:
                            in_bouquets = 1
                    if in_bouquets == 0:
                        if os_path.isfile(
                            '%s/%s' %
                            (enigma_path,
                             bouquetname)) and os_path.isfile('/etc/enigma2/bouquets.tv'):
                            Utils.remove_line(path2, bouquetname)
                            with open(path2, 'a+') as outfile:
                                outfile.write(
                                    '#SERVICE 1:7:1:0:0:0:0:0:0:0:FROM BOUQUET "%s" ORDER BY bouquet\r\n' %
                                    bouquetname)
                                outfile.close()
                                in_bouquets = 1
                    Utils.ReloadBouquets()
                self.session.open(
                    MessageBox,
                    (_('Shuffle Favorite %s List in Progress') %
                     ch) +
                    '\n' +
                    _('Wait please ...'),
                    MessageBox.TYPE_INFO,
                    timeout=5)

    '''add for future'''

    def download_m3u(self):
        try:
            self.download = downloadWithProgress(self.url, self.file)
            self.download.addProgress(self.downloadProgress)
            self.download.start().addCallback(self.check).addErrback(self.showError)
        except BaseException:
            self.session.open(
                MessageBox,
                _('Download Failed!!!'),
                MessageBox.TYPE_INFO,
                timeout=5)
            pass

    def downloadProgress(self, recvbytes, totalbytes):
        self["progress"].show()
        self['progress'].value = int(100 * recvbytes / float(totalbytes))
        self['progresstext'].text = '%d of %d kBytes (%.2f%%)' % (
            recvbytes / 1024, totalbytes / 1024, 100 * recvbytes / float(totalbytes))

    def check(self, fplug):
        if os_path.exists(self.file):
            self['progresstext'].text = ''
            self.progclear = 0
            self['progress'].setValue(self.progclear)
            self["progress"].hide()

    def showError(self, error):
        self.session.open(
            MessageBox,
            _('Download Failed!!!'),
            MessageBox.TYPE_INFO,
            timeout=5)

# remove bouquet  'hbc'
    def msgdeleteBouquets(self):
        self.session.openWithCallback(
            self.deleteBouquets,
            MessageBox,
            _("Remove all HasBahCa Favorite Bouquet ?"),
            MessageBox.TYPE_YESNO,
            timeout=5,
            default=True)

    def deleteBouquets(self, result):
        """
        Clean up routine to remove any previously made changes
        """
        if result:
            try:
                for fname in listdir(enigma_path):
                    if 'hbc_' in fname:
                        Utils.purge(enigma_path, fname)
                    elif 'bouquets.tv.bak' in fname:
                        Utils.purge(enigma_path, fname)

                rename(
                    os_path.join(
                        enigma_path, 'bouquets.tv'), os_path.join(
                        enigma_path, 'bouquets.tv.bak'))
                tvfile = open(os_path.join(enigma_path, 'bouquets.tv'), 'w+')
                bakfile = open(os_path.join(enigma_path, 'bouquets.tv.bak'))
                for line in bakfile:
                    if 'hbc_' not in line:
                        tvfile.write(line)
                bakfile.close()
                tvfile.close()
                self.session.open(
                    MessageBox,
                    _('HasBahCa Favorites List have been removed'),
                    MessageBox.TYPE_INFO,
                    timeout=5)
                Utils.ReloadBouquets()
            except Exception as ex:
                print(str(ex))
                raise

    def cancel(self):
        if search_ok is True:
            self._gotPageLoad()
        else:
            self.close()


class TvInfoBarShowHide():
    """ InfoBar show/hide control, accepts toggleShow and hide actions, might start
    fancy animations. """
    STATE_HIDDEN = 0
    STATE_HIDING = 1
    STATE_SHOWING = 2
    STATE_SHOWN = 3
    FLAG_CENTER_DVB_SUBS = 2048
    skipToggleShow = False

    def __init__(self):
        self["ShowHideActions"] = ActionMap(["InfobarShowHideActions"], {
            "toggleShow": self.OkPressed,
            "hide": self.hide
        }, 0)

        self.__event_tracker = ServiceEventTracker(screen=self, eventmap={
            iPlayableService.evStart: self.serviceStarted,
        })
        self.__state = self.STATE_SHOWN
        self.__locked = 0
        self.hideTimer = eTimer()
        try:
            self.hideTimer_conn = self.hideTimer.timeout.connect(
                self.doTimerHide)
        except BaseException:
            self.hideTimer.callback.append(self.doTimerHide)
        self.hideTimer.start(5000, True)
        self.onShow.append(self.__onShow)
        self.onHide.append(self.__onHide)

    def OkPressed(self):
        self.toggleShow()

    def __onShow(self):
        self.__state = self.STATE_SHOWN
        self.startHideTimer()

    def __onHide(self):
        self.__state = self.STATE_HIDDEN

    def serviceStarted(self):
        if self.execing:
            self.doShow()

    def startHideTimer(self):
        if self.__state == self.STATE_SHOWN and not self.__locked:
            self.hideTimer.stop()
            self.hideTimer.start(3000, True)
        elif hasattr(self, "pvrStateDialog"):
            self.hideTimer.stop()
        self.skipToggleShow = False

    def doShow(self):
        self.hideTimer.stop()
        self.show()
        self.startHideTimer()

    def doTimerHide(self):
        self.hideTimer.stop()
        if self.__state == self.STATE_SHOWN:
            self.hide()

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

    def lockShow(self):
        try:
            self.__locked += 1
        except BaseException:
            self.__locked = 0
        if self.execing:
            self.show()
            self.hideTimer.stop()
            self.skipToggleShow = False

    def unlockShow(self):
        try:
            self.__locked -= 1
        except BaseException:
            self.__locked = 0
        if self.__locked < 0:
            self.__locked = 0
        if self.execing:
            self.startHideTimer()


class Playgo(
    InfoBarBase,
    InfoBarMenu,
    InfoBarSeek,
    InfoBarAudioSelection,
    InfoBarSubtitleSupport,
    InfoBarNotifications,
    TvInfoBarShowHide,
    Screen
):
    STATE_IDLE = 0
    STATE_PLAYING = 1
    STATE_PAUSED = 2
    ENABLE_RESUME_SUPPORT = True
    ALLOW_SUSPEND = True
    screen_timeout = 5000

    def __init__(self, session, name, url, index, item, currentList):
        global streaml, _session
        Screen.__init__(self, session)
        self.session = session
        _session = session
        self.skinName = 'MoviePlayer'
        self.currentindex = index
        self.item = item
        self.itemscount = len(currentList)
        self.list = currentList
        streaml = False
        for cls in (
            InfoBarBase,
            InfoBarMenu,
            InfoBarSeek,
            InfoBarAudioSelection,
            InfoBarSubtitleSupport,
            InfoBarNotifications,
            TvInfoBarShowHide
        ):
            cls.__init__(self)

        self.url = url
        self.name = html_conv.html_unescape(name)
        self.state = self.STATE_PLAYING
        self.srefInit = self.session.nav.getCurrentlyPlayingServiceReference()
        self['actions'] = ActionMap(
            [
                'ButtonSetupActions',
                'ChannelSelectBaseActions',
                'ColorActions',
                'DirectionActions',
                'EPGSelectActions',
                'InfobarActions',
                'InfobarSeekActions',
                'InfobarShowHideActions',
                'MediaPlayerActions',
                'MediaPlayerSeekActions',
                'MoviePlayerActions',
                'MovieSelectionActions',
                'OkCancelActions',
            ],
            {
                'epg': self.showIMDB,
                'info': self.showIMDB,
                'stop': self.cancel,
                'leavePlayer': self.cancel,
                'back': self.cancel,
                'prevBouquet': self.previousitem,
                'nextBouquet': self.nextitem,
                'channelDown': self.previousitem,
                'channelUp': self.nextitem,
                'down': self.previousitem,
                'up': self.nextitem,
                'cancel': self.cancel,
            },
            -1
        )

        if '8088' in str(self.url):
            streaml = True
            self.onFirstExecBegin.append(self.slinkPlay)
        else:
            self.onFirstExecBegin.append(self.openTest)
        self.onClose.append(self.cancel)

    def nextitem(self):
        try:
            currentindex = int(self.currentindex) + 1
            if currentindex == self.itemscount:
                currentindex = 0
            self.currentindex = currentindex
            i = self.currentindex
            item = self.list[i]
            self.name = item[0]
            self.url = item[1]
            self.openTest()
        except Exception as e:
            print("Error in nextitem:", str(e))

    def previousitem(self):
        try:
            currentindex = int(self.currentindex) - 1
            if currentindex < 0:
                currentindex = self.itemscount - 1
            self.currentindex = currentindex
            i = self.currentindex
            item = self.list[i]
            self.name = item[0]
            self.url = item[1]
            self.openTest()
        except Exception as e:
            print("Error in previousitem:", str(e))

    def doEofInternal(self, playing):
        print('doEofInternal', playing)
        Utils.MemClean()
        if self.execing and playing:
            self.openTest()

    def __evEOF(self):
        print('__evEOF')
        self.end = True
        Utils.MemClean()
        self.openTest()

    def nextAV(self):
        message = self.av()
        self.session.open(
            MessageBox,
            message,
            type=MessageBox.TYPE_INFO,
            timeout=1)

    def showIMDB(self):
        text_clear = self.name
        if returnIMDB(text_clear):
            print('show imdb/tmdb')

    def slinkPlay(self):
        name = self.name
        url = self.url
        ref = "{0}:{1}".format(
            url.replace(
                ":", "%3a"), name.replace(
                ":", "%3a"))
        print('final reference:   ', ref)
        sref = eServiceReference(ref)
        sref.setName(str(name))
        self.session.nav.stopService()
        self.session.nav.playService(sref)

    def openTest(self):
        servicetype = '4097'
        name = self.name
        url = self.url

        if isinstance(url, tuple):
            url = url[0] if len(url) > 0 and isinstance(url[0], str) else None

        if not isinstance(url, str):
            print("Error: URL is not valid. Found:", type(url), "Value:", url)
            return

        try:
            ref = "{0}:0:1:0:0:0:0:0:0:0:{1}:{2}".format(
                servicetype,
                url.replace(":", "%3a"),
                name.replace(":", "%3a")
            )
            print('reference:', ref)

            if streaml is True:
                url = 'http://127.0.0.1:8088/' + str(url)
                ref = "{0}:0:0:0:0:0:0:0:0:0:{1}:{2}".format(
                    servicetype,
                    url.replace(":", "%3a"),
                    name.replace(":", "%3a")
                )
            print('final reference:', ref)

            sref = eServiceReference(ref)
            sref.setName(name)
            self.session.nav.stopService()
            self.session.nav.playService(sref)
        except Exception as e:
            print("Error in openTest:", str(e))
            print("url =", url, "name =", name)

    def showAfterSeek(self):
        if isinstance(self, TvInfoBarShowHide):
            self.doShow()

    def cancel(self):
        if os_path.isfile('/tmp/hls.avi'):
            remove('/tmp/hls.avi')
        self.session.nav.stopService()
        self.session.nav.playService(self.srefInit)
        aspect_manager.restore_aspect
        self.close()

    def leavePlayer(self):
        self.cancel()
