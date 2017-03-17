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
host='www.ximalaya.com' 

def albumGetSounds(ab_url):
        
    html = urllib.urlopen(ab_url).read()
    tree = etree.HTML(html)
    sound_urls = tree.xpath("//div[@class='miniPlayer3']/a/@href")
    album_title = tree.xpath("//div[@class='detailContent_title']/h1")[0].text
    if sound_urls:
        for sound_url in sound_urls:
            sound_url = host + sound_url
            soundpage(ab_url, album_title, sound_url)
def soundpage(a_url, a_title, s_url):
    s_url="http://"+s_url
    html = urllib.urlopen(s_url).read()
    tree = etree.HTML(html)
    title = tree.xpath("//div[@class='detailContent_title']/h1")[0].text
    music_type = tree.xpath("//div[@class='detailContent_category']/a")[0].text
    tags = tree.xpath("//div[@class='tagBtnList']/a[@class='tagBtn2']/span")
    tagString = ','.join(i.text for i in tags)
    playcount = tree.xpath("//div[@class='soundContent_playcount']")[0].text
    likecount = tree.xpath("//a[@class='likeBtn link1 ']/span[@class='count']")[0].text
    commentcount = tree.xpath("//a[@class='commentBtn link1']/span[@class='count']")[0].text
    forwardcount = tree.xpath("//a[@class='forwardBtn link1']/span[@class='count']")[0].text
    mp3duration = tree.xpath("//div[@class='sound_titlebar']/div[@class='fr']/span[@class='sound_duration']")[0].text
    username = tree.xpath("//div[@class='username']")[0].text
    username = username.split()[0]
    
    
    music_f=urllib.urlopen(("http://www.ximalaya.com/tracks/"+s_url.split('/')[5]+'.json')) 
    
    music_json=json.loads(music_f.read().decode('utf-8'))
   # print music_json['play_path'],music_json['title'],tagString
    print 'title',title,"_________________"
                        
        



 
if __name__ == '__main__':
    
    sound_url_dir='sound_url_info'
    sound_id_file=os.getcwd()+'/'+'Album'+'/sound_url_info'
    #shutil.rmtree(sound_id_file)
    if not os.path.exists(sound_id_file):
        os.mkdir(sound_id_file)
    else:
        print "You have the directory of sound"
    print os.getcwd() 
    current_dir=os.getcwd()+'/'+'Album'
    album_file_list=os.listdir('Album/data/')
    for filename in album_file_list:     
        os.chdir(current_dir)
        album_url=[]
        album_title=[]
        #album_type=[]
        print str(os.getcwd()+'/'+filename)
        f=open(os.getcwd()+'/data/'+filename,'r')
        for line in f:
            l=line.strip()
            l=line.split(',')

            album_url.append(l[2])
            #chinese_name=unicode(l[3],'GB2312')
            album_file_name=l[0]+"_"+l[1]
            album_title.append(album_file_name)
            #album_dir=os.getcwd()+'/'+album_file_name
            os.chdir(sound_id_file)
            album_dir=os.getcwd()+'/'+album_file_name 
            #print l[3]
            res=l[3].decode('utf-8')
            r=re.sub(r"/",'',res)
            print r,res
            if not os.path.exists(r):
                
                os.mkdir(r)
                #print l[3].decode('utf-8').strip(), os.getcwd()

            albumGetSounds(l[2])



    
