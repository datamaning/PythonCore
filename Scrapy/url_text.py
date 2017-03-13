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
reload(sys)
sys.setdefaultencoding('utf-8')

host='www.ximalaya.com' 
albums_error = 0
sound_error  = 0 
start_dir=os.getcwd()
sound_dir='data/'
album_url_dir='Album/data/'
def albumGetSounds(ab_url): 

    try:
        html = urllib.urlopen(ab_url).read().decode('utf-8')
        tree = etree.HTML(html)
        sound_urls = tree.xpath("//div[@class='miniPlayer3']/a/@href")
        album_title = tree.xpath("//div[@class='detailContent_title']/h1")[0].text
        album_title=re.sub('//',"",album_title)
    
        if sound_urls:
            for sound_url in sound_urls:
                sound_url = host + sound_url
                print sound_url
                soundpage(ab_url, album_title, sound_url)
            
                
    except Exception as e:
        print ">>> albumGetSounds error,error %s,album url is %s" % (e,ab_url)
        print traceback.print_exc()
        global albums_error
        albums_error+=1
        if albums_error < 3:
            print "time sleep 15s"
            time.sleep(15)
            albumGetSounds(ab_url)

def soundpage(a_url, a_title, s_url):
    try:
        s_url="http://"+s_url
        html = urllib.urlopen(s_url).read()
        tree = etree.HTML(html)
        title = tree.xpath("//div[@class='detailContent_title']/h1")[0].text
        music_type = tree.xpath("//div[@class='detailContent_category']/a")[0].text
        tags = tree.xpath("//div[@class='tagBtnList']/a[@class='tagBtn2']/span")
        tagString = ','.join(i.text for i in tags)
        #playcount = tree.xpath("//div[@class='soundContent_playcount']")[0].text
        #likecount = tree.xpath("//a[@class='likeBtn link1 ']/span[@class='count']")[0].text
        #commentcount = tree.xpath("//a[@class='commentBtn link1']/span[@class='count']")[0].text
        #forwardcount = tree.xpath("//a[@class='forwardBtn link1']/span[@class='count']")[0].text
        #mp3duration = tree.xpath("//div[@class='sound_titlebar']/div[@class='fr']/span[@class='sound_duration']")[0].text
        #username = tree.xpath("//div[@class='username']")[0].text
        #username = username.split()[0]
    
        
        music_f=urllib.urlopen(("http://www.ximalaya.com/tracks/"+s_url.split('/')[5]+'.json'))    
        music_json=json.loads(music_f.read().decode('utf-8'))

        result=str(str(a_url)+','+str(a_title)+','+str(s_url)+','+str(title)+','+str(music_type)+','+str(tagString)+','+music_json['play_path'])
        #print result
        file1=open(a_title+'.txt','a')
        file1.write(result+'\n')
        file1.close()
        #return result

    except Exception as e:
        print "*** soundpage error :%s,album url :%s,sound url" %(e,a_url,s_url)
        print trackbakc.print_exc()
        global sound_error
        sound_error+=1
        if sound_error < 3:
            print "time sleep 15s"
            time.sleep(15)
            soundpage(a_url,a_title,s_url)
 
if __name__ == '__main__':
    
    times=int(input())
    album_file_list=[]
    while times>0:
        res=input()
        album_file_list.append(res)
        times-=1
    for filename in album_file_list:
        print filename
        
    
    if not os.path.exists(start_dir+sound_dir):
        os.mkdir(start_dir+sound_dir)
    else:
        print "You have the directory of sound"
    #album_file_list=os.listdir(os.curdir+'/'+album_url_dir) 
    
    #处理数据
    
    for filename in album_file_list:     
        
        os.chdir(os.curdir+'/data/')

        album_url=[]
        album_title=[]
        print str(os.getcwd()+'/'+filename)
        f=open(os.getcwd()+'/'+filename,'r')
        ff=filename.split('.')[0]
        if not os.path.exists(os.curdir+'/'+ff):
            os.mkdir(os.curdir+'/'+ff)
        os.chdir(os.curdir+'/'+ff)
        
        for line in f:
            l=line.strip()
            l=line.split(',')
            album_url.append(l[2])
            album_file_name=l[0]+"_"+l[1]
            album_title.append(album_file_name)
            album_dir=os.getcwd()+'/'+album_file_name 
            res=l[3].decode('utf-8')
            r=re.sub(r"/",'',res)
            #print os.getcwd()
            albums_error=0
            sound_error=0
            albumGetSounds(l[2])

            #if not os.path.exists(r):
                
               # os.mkdir(r)
                #print l[3].decode('utf-8').strip(), os.getcwd()
        os.chdir('..')
        '''
        
    

    
