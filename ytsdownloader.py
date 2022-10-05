from shutil import ExecError
import requests
import pandas
from client import Client
import datahandler
import logmaker
import logging
import time


def connect(file=None, torrhash=None, tryprompt=False):
    configdata = datahandler.retrievesetting()

    try:
        qb = Client(configdata[4])
        qb.login(configdata[0], configdata[1])
        if tryprompt:
            print('Connection established.')
        logging.info('Connected to QBit')
    except requests.exceptions.ConnectionError:
        logging.warning('QbitTorrent not running, unable to connect')
        logging.warning(
            'attempting connect @ {}, {}, {}'.format(configdata[0], configdata[1], configdata[4]))
        print("QBitTorrent is not running! @ {}".format(configdata[4]))
    if file:
        try:
            qb.download_from_link(file, savepath=configdata[2])
            time.sleep(1)
            if configdata[5] == 'yes':
                qb.toggle_sequential_download(torrhash)
            print("Movie is being downloaded ..")
            logging.info('Downloading movie..')
        except:
            logging.error(
                'couldnt connect to QBIT while trying to download movie.')
            logging.error('{}, {}, {}'.format(
                configdata[0], configdata[1], configdata[2]))
            print(
                'Couldn\'t connect to QbitTorrent. Check that your password is correct.')
            print('Tried: {}, {}'.format(configdata[0], configdata[1]))
            print('If the password is correct, try restarting your QBitTorrent client.')
            q = input('Press enter to try again..')
            connect(file, torrhash)


def parse(jsondata):
    configdata = datahandler.retrievesetting()
    fourkay = configdata[6]

    if fourkay == 'yes':
        fourkayoption = '2160p'
    else:
        fourkayoption = '1080p'

    df = pandas.DataFrame()
    title, year, rating, link, helper = [], [], [], [], []

    for datapoint in jsondata['data']['movies']:
        title.append(datapoint['title'])
        year.append(datapoint['year'])
        rating.append(datapoint['rating'])

        for torr in datapoint['torrents']:
            helper.append(torr['quality'])

        def lookfor(quality, type="bluray"):
            for i in datapoint['torrents']:
                if i['quality'] == quality and i['type'] == type:
                    link.append(i['url'])
                    return True
            return False

        if not lookfor(fourkayoption):
            if not lookfor('1080p'):
                if not lookfor('1080p', type='web'):
                    if not lookfor('720p'):
                        if not lookfor('720p', type='web'):
                            link.append('')  # ran out of options :-)

    for movie in zip(title, year, rating):
        df = pandas.concat([df, pandas.DataFrame([movie])])
        dfcolumns = ['Title', 'Year', 'Rating']
        df = df.rename(columns={0: dfcolumns[0], 1: dfcolumns[1], 2: dfcolumns[2]})
        df.index = df.index + 1

    print(df)

    def loadurl():
        tld = configdata[3]
        fourkayallow = configdata[6]
        id = input("Download which one? (q to go back) ")
        logging.info('user input: {}'.format(id))
        if id == "q":
            main(init=False)
        else:
            try:
                id = int(id)
            except ValueError:
                print('Error.')
                loadurl()
            try:
                moviehash = link[id -
                                 1].replace(f'{tld}torrent/download/', '').lower()
                logging.debug('generated movie hash OK')
                logmaker.writemov(title[id - 1], link[id - 1])
                connect(link[id - 1], moviehash)
            except IndexError:
                print("Wrong ID..")
                loadurl()

    loadurl()


def search(term):
    configdata = datahandler.retrievesetting()
    tld = configdata[3]
    try:
        result = requests.get(
            f'{tld}api/v2/list_movies.json?query_term=%22{term}%22&limit=50')
        logging.info('requested {}, result {}'.format(
            term, result.status_code))
    except:
        print(
            f"Failed to request title. Problems with server probably. Is {tld} working?")
        logging.error('Failed to request URL.')
        x = input(' ')
        quit()

    fresult = result.json()

    if fresult['status'] == 'ok':
        foundnumber = fresult['data']['movie_count']
        if foundnumber > 0:
            print(f"Found {str(foundnumber)} movies:")
            parse(fresult)
        else:
            print("No movies found.")
            main()

    else:
        print("Invalid request.", fresult['status'])


def main(init=True):

    logging.basicConfig(filename='trace.log',
                        filemode='a',
                        format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                        datefmt='%H:%M:%S',
                        level=logging.INFO)
    if init:
        if datahandler.runchecks():
            connect()
            mov = str(input("Search for movie: "))
            logging.info('Searched {}'.format(mov))
            search(mov)
        else:
            print('Some files were found missing & I tried re-creating them ..')
            main()
    else:
        mov = str(input("Search for movie: "))
        logging.info('Searched {}'.format(mov))
        search(mov)


if __name__ == "__main__":
    print('YTSDownloader 1.3.9 64bit')
    try:
        main()
    except KeyboardInterrupt:
        logging.info('KeyboardInterrupt, clean exit')
        print("\n")
        print('Exiting..')
    except Exception as e:
        print(e)
        logging.error('Exception: {}'.format(e))
