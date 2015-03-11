#!/usr/bin/env python3

import urllib.request
from html.parser import HTMLParser
import subprocess
import os

sublimeFolder = os.path.expanduser('~/software')  # Where your sublime_text_3 folder is.
updateUrl = 'http://www.sublimetext.com/3dev'  # What webpage to scrub for the update url.


class MyHTMLParser(HTMLParser):
    catchUrl = False
    url = None

    def handle_starttag(self, tag, attrs):
        if tag == 'li' and ('id', 'dl_linux_64') in attrs:
            self.catchUrl = True
        if self.catchUrl and tag == 'a':
            for attr, val in attrs:
                if attr == 'href' and val.endswith('bz2'):
                    self.url = val

    def handle_endtag(self, tag):
        if self.catchUrl and tag == 'li':
            self.catchUrl = False

f = urllib.request.urlopen(updateUrl)
parser = MyHTMLParser()
parser.feed(str(f.read()))

if parser.url is None:
    raise Exception('Failed to find 64-bit linux update url to bz2 file on {updateUrl}.'.format(updateUrl=updateUrl))

local_filename, headers = urllib.request.urlretrieve(parser.url)
print('Downloaded {url} to {file}'.format(url=parser.url, file=local_filename))
subprocess.call(['tar', 'xf', local_filename, '-C', sublimeFolder])

try:
    os.unlink(local_filename)
except:
    pass  # Temp file, so essentially we don't care.
