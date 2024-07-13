#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
****************************************
*        coded by Lululla              *
*             skin by MMark            *
*             09/08/2022               *
*   Thank's                            *
*      HasBahCa, Levi45, KiddaC, Pcd   *
****************************************
'''
from __future__ import absolute_import
from Plugins.Plugin import PluginDescriptor
from Tools.Directories import SCOPE_PLUGINS, resolveFilename
from . import main
from . import Utils
import os

currversion = '1.5'
title_plug = 'HasBahCa '
desc_plugin = ('..:: HasBahCa by Lululla %s ::.. ' % currversion)
plugin_path = resolveFilename(SCOPE_PLUGINS, "Extensions/{}".format('HasBahCa'))
_firstStarthbc = True


class AutoStartTimerhbc:

    def __init__(self, session):
        self.session = session
        global _firstStarthbc
        print("*** running AutoStartTimerhbc ***")
        if _firstStarthbc:
            self.runUpdate()

    def runUpdate(self):
        print("*** running update ***")
        try:
            from . import Update
            Update.upd_done()
            _firstStarthbc = False
        except Exception as e:
            print('error Fxy', str(e))


def autostart(reason, session=None, **kwargs):
    print("*** running autostart autoStartTimerhbc ***")
    global autoStartTimerhbc
    global _firstStarthbc
    if reason == 0:
        if session is not None:
            _firstStarthbc = True
            autoStartTimerhbc = AutoStartTimerhbc(session)
    return


def mainw(session, **kwargs):
    try:
        from six.moves import reload_module
        reload_module(Utils)
        reload_module(main)
        session.open(main.MainHasBahCa)
    except:
        import traceback
        traceback.print_exc()


def Plugins(**kwargs):
    ico_path = 'logo.png'
    if not os.path.exists('/var/lib/dpkg/status'):
        ico_path = os.path.join(plugin_path, 'res/pics/logo.png')
    # extensions_menu = PluginDescriptor(name=title_plug + ' ' + currversion, description=desc_plugin, where=PluginDescriptor.WHERE_EXTENSIONSMENU, fnc=mainw, needsRestart=True)
    result = [PluginDescriptor(name=title_plug + ' ' + currversion, description=desc_plugin, where=[PluginDescriptor.WHERE_SESSIONSTART], fnc=autostart),
              PluginDescriptor(name=title_plug + ' ' + currversion, description=desc_plugin, where=PluginDescriptor.WHERE_PLUGINMENU, icon=ico_path, fnc=mainw)]
    # result = [PluginDescriptor(name=title_plug + ' ' + currversion, description=desc_plugin, where=PluginDescriptor.WHERE_PLUGINMENU, icon=ico_path, fnc=mainw)]
    # result.append(extensions_menu)
    return result
