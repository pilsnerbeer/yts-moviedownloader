# logs history of downloaded movies.

from datetime import datetime
import logging

now = datetime.today()
now = now.strftime('%d.%m.%y')

logging.basicConfig(filename='trace.log',
                    filemode='a',
                    format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                    datefmt='%H:%M:%S',
                    level=logging.INFO)


def writemov(moviename, dllink):
    try:
        with open('history.txt', 'a') as file:
            logging.info('open history.txt OK')
            file.write(now + ' ' + moviename + ' ' + '\n')
            logging.info('wrote movie to history OK')

    except:
        print('Error writing to history.')
        logging.error(
            'Can\'t write to history. Tried {}, {}'.format(moviename, dllink))
