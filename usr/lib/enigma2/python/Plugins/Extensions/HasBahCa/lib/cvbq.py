#!/usr/bin/python
# -*- coding: utf-8 -

# convert bouquet m3u url
# from . import cvbq
# service = '4097'
# ch = 0
# ch = cvbq.convert_bouquet(url, name, service)
# if ch:
    # _session.open(MessageBox, _('bouquets reloaded..\nWith %s channel' % ch), MessageBox.TYPE_INFO, timeout=5)
# by lululla 20230830
import os
import sys
from . import html_conv
PY2 = False
PY3 = False
PY34 = False
PY39 = False
PY2 = sys.version_info[0] == 2
PY3 = sys.version_info[0] == 3
PY34 = sys.version_info[0:2] >= (3, 4)
PY39 = sys.version_info[0:2] >= (3, 9)
print("sys.version_info =", sys.version_info)
downloadm3u = '/media/hdd/movie/'
try:
    from Components.UsageConfig import defaultMoviePath
    downloadm3u = defaultMoviePath()
except:
    if os.path.exists("/usr/bin/apt-get"):
        downloadm3u = ('/media/hdd/movie/')


def downloadFile(url, target):
    import socket
    try:
        from urllib.error import HTTPError, URLError
        from urllib.request import urlopen
    except:
        from urllib2 import HTTPError, URLError
        from urllib2 import urlopen
    try:
        response = urlopen(url, None, 5)
        with open(target, 'wb') as output:
            # print('response: ', response)
            if PY3:
                output.write(response.read().decode('utf-8'))
            else:
                output.write(response.read())
            # output.write(response.read())
        response.close()
        return True
    except HTTPError:
        print('Http error')
        return False
    except URLError:
        print('Url error')
        return False
    except socket.timeout:
        print('sochet error')
        return False


def convert_bouquet(url, namex, service):
    bouquet_type = 'tv'
    if "radio" in namex.lower():
        bouquet_type = "radio"

    name_file = re.sub(r'[<>:"/\\|?*, ]', '_', str(namex))  # Sostituisce anche gli spazi e le virgole con "_"
    name_file = re.sub(r'\d+:\d+:[\d.]+', '_', name_file)  # Sostituisce i pattern numerici con "_"
    nf = re.sub(r'_+', '_', name_file)  # Sostituisce sequenze di "_" con un singolo "_"

    if os.path.exists(downloadm3u):
        xxxname = downloadm3u + nf + '.m3u'
    else:
        xxxname = '/tmp/' + nf + '.m3u'
    print('path m3u: ', xxxname)
    '''
    # response = urlopen(url, None, 5)
    # with open(xxxname, 'wb') as output:
        # # print('response: ', response)
        # # if PY3:
            # # output.write(response.read().decode('utf-8'))
            # # # output.write(response.read().decode('utf-8'))
        # # else:
        # output.write(response.read())
    # response.close()
    '''
    if downloadFile(url, xxxname):
        bouquet_name = 'userbouquet.%s.%s' % (nf.lower(), bouquet_type.lower())
        print("Converting Bouquet %s" % nf)
        path1 = '/etc/enigma2/' + str(bouquet_name)
        path2 = '/etc/enigma2/bouquets.' + str(bouquet_type.lower())
        ch = 0
        if os.path.exists(xxxname) and os.stat(xxxname).st_size > 0:
            try:
                tplst = []
                tplst.append('#NAME %s (%s)' % (nf.upper(), bouquet_type.upper()))
                tplst.append('#SERVICE 1:64:0:0:0:0:0:0:0:0::%s CHANNELS' % nf)
                tplst.append('#DESCRIPTION --- %s ---' % nf)
                namel = ''
                svz = ''
                dct = ''
                for line in open(xxxname):

                    if line.startswith("#EXTINF"):
                        namel = '%s' % line.split(',')[-1]
                        dsna = ('#DESCRIPTION %s' % namel).splitlines()
                        dct = ''.join(dsna)

                    elif line.startswith('http'):
                        tag = '1'
                        if bouquet_type.upper() == 'RADIO':
                            tag = '2'

                        svca = ('#SERVICE %s:0:%s:0:0:0:0:0:0:0:%s' % (service, tag, line.replace(':', '%3a')))
                        svz = (svca + ':' + namel).splitlines()
                        svz = ''.join(svz)

                    if svz not in tplst:
                        tplst.append(svz)
                        tplst.append(dct)
                        ch += 1

                with open(path1, 'w+') as f:
                    for item in tplst:
                        if item not in f.read():
                            f.write("%s\n" % item)
                            print('item  -------- ', item)

                in_bouquets = False
                for line in open('/etc/enigma2/bouquets.%s' % bouquet_type.lower()):
                    if bouquet_name in line:
                        in_bouquets = True
                if in_bouquets is True:
                    '''
                    Rename unlinked bouquet file /etc/enigma2/userbouquet.webcam.tv to /etc/enigma2/userbouquet.webcam.tv.del
                    '''
                    with open(path2, 'a+') as f:
                        bouquetTvString = '#SERVICE 1:7:1:0:0:0:0:0:0:0:FROM BOUQUET "' + str(bouquet_name) + '" ORDER BY bouquet\n'
                        f.write(str(bouquetTvString).encode("utf-8"))
                try:
                    from enigma import eDVBDB
                    dbr = eDVBDB.getInstance()
                    dbr.reloadBouquets()
                    dbr.reloadServicelist()
                    print('all bouquets reloaded...')
                except:
                    eDVBDB = None
                    os.system('wget -qO - http://127.0.0.1/web/servicelistreload?mode=2 > /dev/null 2>&1 &')
                    print('bouquets reloaded...')
                    ReloadBouquets()
            except Exception as error:
                print(error)
            return ch
