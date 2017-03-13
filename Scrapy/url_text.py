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
import urllib
import json
import re
import urllib2
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
album_dir='album_test'
url_text=os.getcwd()+'/txt/'
def albumGetSounds(ab_url): 

    try:
        #print 'ab_url',ab_url,'os-cwd',os.getcwd()
        request=urllib2.Request(ab_url)
        request.add_header('User-Agent','fake-client')
        
        html = urllib2.urlopen(request).read().decode('utf-8')
        tree = etree.HTML(html)
        sound_urls = tree.xpath("//div[@class='miniPlayer3']/a/@href")
        album_title = tree.xpath("//div[@class='detailContent_title']/h1")[0].text
        album_title=re.sub('//',"",album_title)
        #print "ab_url",ab_url
        if sound_urls:
            for sound_url in sound_urls:
                sound_url = host + sound_url
                print sound_url
                soundpage(str(ab_url), str(album_title), str(sound_url))
            
                
    except Exception as e:
        #print ">>> albumGetSounds error,error %s,album url is %s" % (e,ab_url)
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
        request=urllib2.Request(s_url)

        request.add_header('User-Agent','fake-client')
        html = urllib2.urlopen(request).read()
        tree = etree.HTML(html)
        json_url='http://www.ximalaya.com/tracks/'+s_url.split('/')[5]+'.json'
        request1=urllib2.Request(json_url)
        request1.add_header('User-Agent','fake-client')
        music_f=urllib2.urlopen(request1)

        music_json=json.loads(music_f.read().decode('utf-8'))
        download_url=music_json['play_path']

        #sound_file.write(download_url+'\n')

        channel_id=a_url.split('/')[3]
        album_id=a_url.split('/')[5]
        sound_id=s_url.split('/')[5]
        print music_json['play_path']
        #filename=channel_id+"_"+album_id+"_"+sound_id
        url_sub=re.sub('/','',music_json['play_path'])

        filename=channel_id+"_"+album_id+"_"+sound_id+url_sub
        print filename,'filename***********' 
        sound_file=open(url_text+filename+'.txt','w+')
        a_title='album_title='+a_title
        title = 'sound_title='+tree.xpath("//div[@class='detailContent_title']/h1")[0].text
        music_type ='music_type='+tree.xpath("//div[@class='detailContent_category']/a")[0].text
        tags = tree.xpath("//div[@class='tagBtnList']/a[@class='tagBtn2']/span")
        tagString = 'tagString='+','.join(i.text for i in tags)
        playcount = 'playcount='+tree.xpath("//div[@class='soundContent_playcount']")[0].text
        likecount = 'likecount='+tree.xpath("//a[@class='likeBtn link1 ']/span[@class='count']")[0].text
        commentcount = 'commentcount='+tree.xpath("//a[@class='commentBtn link1']/span[@class='count']")[0].text
        forwardcount = 'forwardcount='+tree.xpath("//a[@class='forwardBtn link1']/span[@class='count']")[0].text
        mp3duration = 'md3duration='+tree.xpath("//div[@class='sound_titlebar']/div[@class='fr']/span[@class='sound_duration']")[0].text    
        username = tree.xpath("//div[@class='username']")[0].text
        username = 'username='+username.split()[0]

        sound_file.write(str(a_title+'\n'))
        sound_file.write(str(title+'\n'))
        sound_file.write(str(music_type+'\n'))
        sound_file.write(str(tagString+'\n'))
        sound_file.write(str(playcount+'\n'))
        sound_file.write(str(likecount+'\n'))
        sound_file.write(str(commentcount+'\n'))
        sound_file.write(str(forwardcount+'\n'))
        sound_file.write(str(mp3duration+'\n'))
        sound_file.write(str("albumurl="+a_url+'\n'))
        sound_file.write(str('soundurl='+s_url+'\n'))
        sound_file.write(str('downloadurl='+download_url)+'\n')
        sound_file.write(str(username+'\n'))
        
        sound_file.close()
        #return result

    except Exception as e:
        #print "*** soundpage error :%s,album url :%s,sound url" %(e,a_url,s_url)
        print traceback.print_exc()
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
        res=str(input())
        res=os.getcwd()+'/'+album_dir+'/'+res+'.txt'
        album_file_list.append(res)
        times-=1
        
       

    txt_dir=start_dir+'/txt/' 
    if not os.path.exists(txt_dir):
        os.mkdir(txt_dir)
    else:
        print "You have the directory of sound"
    #处理数据
    for filename in album_file_list:     
        os.chdir(start_dir+'/'+album_dir)
       # print os.getcwd(),filename
        album_url=[]
        album_title=[]
        #按声音类型建立文件夹
        f=open(filename,'r')
        '''
        ff=filename.split('.')[0]
        if not os.path.exists(ff):
            os.mkdir(ff)
        os.chdir(ff)
        '''
        for line in f:
            l=line.strip()
            l=line.split(',')
            album_url.append(l[2])
            album_file_name=l[0]+"_"+l[1]
            album_title.append(album_file_name)
            #album_dir=os.getcwd()+'/'+album_file_name 
            res=l[3].decode('utf-8')
            r=re.sub(r"/",'',res)
            #print os.getcwd()
            albums_error=0
            sound_error=0
            
            a_url=l[2]+'?page=1'
            request=urllib2.Request(a_url)
            request.add_header('User-Agent','fake-client')
            html = urllib2.urlopen(request).read()
            tree = etree.HTML(html)
            pages = tree.xpath("//div[@class='pagingBar_wrapper']/a/text()")
        #print len(pages),"len pages"
            pages =[ int(i) for i in pages if i.isdigit()]     #判断是数字，只保留数字        
            if len(pages)==0:
                max_page=1
            else:
                max_page = max(pages)
            print max_page
            for page in xrange(1, max_page+1):    
                albumGetSounds(l[2]+'?page='+str(page))

            #if not os.path.exists(r):               
               # os.mkdir(r)
                #print l[3].decode('utf-8').strip(), os.getcwd()
        
        
    

    
