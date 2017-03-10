#coding:utf-8


from lxml import etree
import re
from pymongo import MongoClient
import socket
import threading
from Queue import Queue
import time
import random
import sys
import traceback
import os
import shutil
from html.parser import HTMLParser
from urllib2 import Request
import urllib
import json
import re
socket.setdefaulttimeout(20)
PgEr = 0
queue = Queue(200)
queue_in = Queue(100)
reload(sys)
sys.setdefaultencoding('utf-8')
    
def albumGetSounds(ab_url):
    pass
    



 
if __name__ == '__main__':
    sound_url_dir='sound_url_info'
    if not os.path.exists(os.curdir+'/'+sound_url_dir):
        os.mkdir(os.curdir+'/'+sound_url_dir)
    else:
        print "You have the directory of sound"

    album_file_list=os.listdir('Album')
    print album_file_list

    
