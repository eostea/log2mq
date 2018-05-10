import sys
import os
import logging
from http.client import HTTPConnection, HTTPSConnection
from urllib.parse import urlparse
from inotify import adapters, constants


logger = logging.getLogger('log2mq')
logger.level = logging.INFO
client: HTTPConnection = None
uri = None

USAGE = """
Usage: log2mq log-dir-or-file-path nsq-url
Example: log2mq /tmp/log http://127.0.0.1:4151/pub?topic=test
"""


class HandlerFile(object):
    def __init__(self):
        #  {'filename': where}
        self.pos = dict()
        #  {'filename': file object}
        self.file = dict()

    def get_change(self, filename, from_start=False):
        if filename not in self.file:
            f = open(filename)
            self.file[filename] = f
            if from_start:
                self.pos[filename] = f.seek(0)
            else:
                self.pos[filename] = f.seek(0, 2)
        else:
            f = self.file[filename]
        while 1:
            line = f.readline()
            if line:
                yield line
            else:
                break


handler = HandlerFile()


def handler_event(event):
    _event, event_type, path, file = event
    if file:
        fn = os.path.join(path, file)
    else:
        fn = path
    for change in handler.get_change(fn):
        try:
            post_event(change)
        except Exception as err:
            logger.error(err)


def post_event(message):
    client.request('POST', uri, body=message)
    r = client.getresponse()
    r.read()


def main():
    global client
    global uri
    notify = adapters.Inotify()
    args = sys.argv
    if len(args) != 3:
        logger.warning(USAGE)
        exit(1)
    path, url = args[1], args[2]
    if not os.path.exists(path):
        logger.error('{} does not exist'.format(path))
        exit(1)
    uo = urlparse(url)
    host, port = uo.netloc.split(':')[0], uo.netloc.split(':')[1]
    if uo.scheme == 'https':
        client = HTTPSConnection(host, port, timeout=5)
    else:
        client = HTTPConnection(host, port, timeout=5)
    uri = uo.path + '?' + uo.query
    notify.add_watch(path, mask=constants.IN_MODIFY)
    try:
        for event in notify.event_gen(yield_nones=False):
            handler_event(event)
    except KeyboardInterrupt:
        exit(0)
    except Exception as err:
        logger.error(err)
        print(err)
    finally:
        notify.remove_watch(path)
        logger.warning('Stop...')
