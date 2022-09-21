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
from Components.PluginComponent import plugins
from Tools.Directories import SCOPE_PLUGINS, resolveFilename
from . import main
from . import Utils
import os

currversion = '1.5'
title_plug = 'HasBahCa '
desc_plugin = ('..:: HasBahCa by Lululla %s ::.. ' % currversion)
plugin_path = resolveFilename(SCOPE_PLUGINS, "Extensions/{}".format('HasBahCa'))


try:
    if Utils.zCheckInternet(1):
        from . import Update
        Update.upd_done()
    else:
        from Screens.MessageBox import MessageBox
        from Tools.Notifications import AddPopup
        AddPopup(_("Sorry but No Internet :("), MessageBox.TYPE_INFO, 10, 'Sorry')

except:
    import traceback
    traceback.print_exc()


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
        ico_path = plugin_path + '/res/pics/logo.png'
    # extensions_menu = PluginDescriptor(name=title_plug + ' ' + currversion, description=desc_plugin, where=PluginDescriptor.WHERE_EXTENSIONSMENU, fnc=mainw, needsRestart=True)
    result = [PluginDescriptor(name=title_plug + ' ' + currversion, description=desc_plugin, where=PluginDescriptor.WHERE_PLUGINMENU, icon=ico_path, fnc=mainw)]
    # result.append(extensions_menu)
    return result
