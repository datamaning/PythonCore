from html.parser import HTMLParser
import urllib
import json
import os 
import sys
import re
#from lxml import etree
import traceback
import random
import socket
import Queue
socket.setdefaulttimeout(20)
queue_url=Queue(200)
queue_comment=Queue(100)
type_addrs=[]
class Ximalaya(threading.Thread):
    def __init__(self,queue_url,queue_comment,start,end):
        self.queue_url=queue_url
        self.queue_comment=queue_comment
        self.start=start
        self.end=end
        self.headers={'Accept-Language':'zh-CN',
                'User-Agent':'Mozilla/5.0(compatible;MSIE 9.0;Windows NT 6.1;WOW64;Trident/5.0)',
                'Content-type':'application/x-www-form-urlencoded',
                'Host':'www.introducer.westpac.net.nu',
                'Connection':'Keep-Alive',
                }

if __name__=='__main__':
    with open('sound_type.txt','r') as type_file:
        type_addrs=type_file.readline()
    print (type(type_addrs))
    exit_flag=threading.Event()
    exit_flag.clear()
    start=0;
    for i in range(10):
        xi=Ximalaya(queue_url,queue_comment,start,start+1)
        start+=2
    
    exit_flag.set()

    print ("All Downloaded!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
