import os
import logging
from os.path import exists
from configparser import ConfigParser

config = ConfigParser()


def runchecks():
    logging.basicConfig(filename='trace.log',
                        filemode='a',
                        format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                        datefmt='%H:%M:%S',
                        level=logging.INFO)

    conffile = exists('config.ini')

    if conffile:
        return True

    else:
        logging.info('config.ini does not exist. running init now')

        usr = str(
            input('Welcome to YTSDownloader. Specify your QBitTorrent WebUI username: '))
        pwd = str(
            input('Specify your QBitTorrent WebUI password: '))
        path = os.getcwd()
        dlpath = str(input('Current download location: ' +
                           str(path) + ' ' + 'Okay? (y/n) '))
        choice = ['y', '', 'yes']
        if dlpath in choice:
            dlpath = path
        else:
            dlpath = str(input('Specify your new download location: '))
        seq = str(input('Download movies sequentially by default? (Recommended) '))
        if seq in choice:
            seq = 'yes'
        else:
            seq = 'no'

        print('------------')
        print('Create config file OK. To change it, edit config.ini via text editor.')

        config.add_section('main')
        config.set('main', 'username', usr)
        config.set('main', 'password', pwd)
        config.set('main', 'savelocation', dlpath)
        config.set('main', 'ytssource', 'https://yts.mx/')
        config.set('main', 'networkaddr', 'http://127.0.0.1:8080')
        config.set('main', 'sequentialdownload', seq)
        config.set('main', 'allow4K', 'no')

        with open('config.ini', 'w') as f:
            config.write(f)

        return True


def retrievesetting():
    """0:username, 1:password, 2:savelocation, 3:ytssource, 4:networkaddr, 5:sequentialdownload, 6:allow4k"""
    config.read('config.ini')
    l = []
    for opt in config.options('main'):
        l.append(config.get('main', opt))
    #logging.info('returned {}'.format(l))

    if not l[3].endswith('/'):
        l[3] += '/'

    return l
