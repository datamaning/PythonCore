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
class Ximalaya(threading.Thread):
    def __init__(self, queue, queue_in):
        threading.Thread.__init__(self)
        self.queue = queue
        self.queue_in = queue_in
        self.host = 'http://www.ximalaya.com'
        self.client = MongoClient()
        self.db = self.client.test
        self.musicInfo = self.db.music
        self.commentInfo = self.db.bookcomment
        self.AgsEr = 0
        self.SdEr = 0
        self.ClgEr = 0
        
        self.headers = {'Accept-Language': 'zh-CN',
                       'User-Agent': 'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0)',
                       'Content-Type': 'application/x-www-form-urlencoded',
                       'Host': 'www.introducer.westpac.net.au',
                       'Connection': 'Keep-Alive',
                        }
        
    def run(self):
        while not exit_flag.is_set():
            time.sleep(random.uniform(1,3))
            album_url = self.queue_in.get()
            self.albumGetSounds(album_url)
            self.queue_in.task_done()
            print '*** Album done, url: %s, Queue: %s, Queue_in: %s, Page: %s ***' % (album_url, self.queue.qsize(), self.queue_in.qsize(), page)
            
            
    def albumGetSounds(self, ab_url):
        try:
            html = urllib.urlopen(ab_url).read()
            tree = etree.HTML(html)
            sound_urls = tree.xpath("//div[@class='miniPlayer3']/a/@href")
            album_title = tree.xpath("//div[@class='detailContent_title']/h1")[0].text
            if sound_urls:
                for sound_url in sound_urls:
                    sound_url = self.host + sound_url
                    #print 'Sound url is: ', sound_url
                    
                    #如果在数据库找到声音url地址，就不再解析声音
                    exists_flag = self.Musicinfo_find(sound_url)
                    if not exists_flag:                    
                        print '>>> Sound put %s, Queue: %s, Queue_in: %s, Page: %s' % (sound_url, self.queue.qsize(), self.queue_in.qsize(), page)
                        self.soundpage(ab_url, album_title, sound_url)
                    else:
                        pass
                        #print 'Sound %s already exists, goto next >>>' % sound_url
                    
        except Exception as e:
            print '***albumGetSounds error, error: %s, album url: %s' % (e, ab_url)
            print traceback.print_exc()
            self.AgsEr += 1
            if self.AgsEr < 3:
                print 'time sleep 15s.'
                time.sleep(15)
                self.albumGetSounds(ab_url)
    
    def soundpage(self, a_url, a_title, s_url):
        try:
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
            track_id = re.search(r'track_id="(\d+)"', html)
            track_id = track_id.group(1) if track_id else None
            comment_url = 'http://www.ximalaya.com/sounds/'+ track_id + '/comment_list'
            print likecount, commentcount, forwardcount, mp3duration, username, track_id, comment_url
            
            info_sound = {}
            info_sound['album_title'] = a_title
            info_sound['album_url'] = a_url
            info_sound['title'] = title
            info_sound['music_type'] = music_type
            info_sound['tags'] = tagString
            info_sound['music_id'] = track_id
            info_sound['playcount'] = playcount
            info_sound['likecount'] = likecount
            info_sound['commentcount'] = commentcount
            info_sound['forwardcount'] = forwardcount
            info_sound['mp3duration'] = mp3duration
            info_sound['user'] = username
            info_sound['url'] = s_url
                
            #把声音信息插入数据库
            self.Musicinfo_insert(info_sound)
            #把生成评论url地址，交给commenlistGet处理
            #self.CommenlistGet(comment_url)
            print a_title,a_url,title,username,music_type
        except Exception as e:
            print '***soundpage error: %s, Album url: %s, sound url: %s' % (e, a_url, s_url)
            print traceback.print_exc()
            self.SdEr += 1
            if self.SdEr < 3:
                print 'Time sleep 15s'
                time.sleep(15)
                self.soundpage(a_url, a_title, s_url)
        
        
        
    def Musicinfo_insert(self, infoData):
        music_id = self.musicInfo.insert(infoData)
        return music_id
    
    def Musicinfo_find(self, url):
        count = self.musicInfo.find_one({"url": url})
        return count
        
    def CommentInfo_find(self, url):
        comCount = self.commentInfo.find_one({"url": url})
        return comCount
    
#提取sound id，提取专辑名称用于创建该专辑文件夹
class AlbumEventHtmlParser(HTMLParser):
    sound_ids = []
    album_title = "";
    title_flag = False

    def __init__(self):  
        HTMLParser.__init__(self)
        self.sound_ids = []
        self.album_title = ""

    def handle_starttag(self, tag, attrs):
        if tag == 'li': 
            for name, value in attrs: 
                if name == 'sound_id': 
                    self.sound_ids.append(value)

        if tag == 'title':
            self.title_flag = True

    def handle_data(self, data):
        if self.title_flag:
            rstr_list = re.findall(r"【(.*)】", data)
            self.album_title = rstr_list[0]
            print(self.album_title)
            self.title_flag = False

def parse_python_events():

    album_addrs = []
    album_folder = ""

    #本地文件存储专辑链接地址，可以一次下载多个专辑
    with open('albumaddr.txt','r') as addr_file:
        album_addrs = addr_file.readlines()

    for addr in album_addrs:
        sound_ids = []
        parser = AlbumEventHtmlParser()

        with request.urlopen(addr) as album_file:
            html = album_file.read().decode('utf-8')

        parser.feed(html)

        sound_ids = parser.sound_ids;

        if len(sound_ids)>0:
            album_folder = parser.album_title;
            if not os.path.exists(os.curdir + '/' + album_folder):
                os.mkdir(os.curdir + '/' + album_folder)
            else:
                print("You have already downloaded the album: %s" % album_folder)
                continue
        else:
            print("There is no sound: %s" % addr)
            continue

        #for sound_id in sound_ids:       
        #   with request.urlopen(('http://www.ximalaya.com/tracks/' + sound_id + '.json')) as music_f:
        #        music_json = json.loads(music_f.read().decode('utf-8'))
        #    print(music_json['title']+'downloding...')
        #    request.urlretrieve(music_json['play_path'], './' + album_folder + '/' + music_json['title'] + '.mp3')
        #    print(music_json['title']+'downloaded')  
        #
#把每一页的各专辑地址放入queue_in队列
def pageGetAlbums(url,sound_type,page):
    try:
        html = urllib.urlopen(url).read()
        tree = etree.HTML(html)
        #print url,"url is .............."
        album_urls = tree.xpath("//div[@class='albumfaceOutter']/a/@href")
        album_title=tree.xpath("//img/@alt")[1:]
        #print len(album_title),album_title
        #print len(album_title)
        album_list=[]
        count=(page-1)*12+1
        if album_urls:
            for index in range(len(album_urls)):
                # 'Album url is: ', album_url
                #global queue_in
                #global queue
                #queue_in.put(album_url)
                insert=str(sound_type+","+str(count)+','+album_urls[index]+","+ album_title[index]+"\n")
                album_list.append(insert)
                count+=1
                #print 'Queue_in: %s, Queue: %s, Page: %s' % (queue_in.qsize(), queue.qsize(), page)
        album_file=open(sound_type+".txt",'a')
        album_file.writelines(album_list)
        album_file.close() 
    except Exception as e:
        print url,'url is .......'
        print '****pageGetAlbums %s get error, error: %s' % (url, e)

        print traceback.print_exc()
        global PgEr
        PgEr += 1
        if PgEr < 5:
            print 'time sleep 15s'
            time.sleep(15)
            pageGetAlbums(url,sound_type,page)    
    



 
if __name__ == '__main__':
    #exit_flag = threading.Event()
    #exit_flag.clear()
    
    #for i in range(10):
        #xi = Ximalaya(queue, queue_in)
        #xi.start()
    album_folder_name='Album'
    shutil.rmtree(album_folder_name) 
    if not os.path.exists(os.curdir+'/'+album_folder_name):
        os.mkdir(os.curdir+'/'+album_folder_name)
    else:
        print "You have already make the album "
    #print os.getcwd()
    #url_type=['book','music','entertainment','comic','kid','3Dfell2','news','talk2','emotion','culture','renwen','chair','english','xiaoyuzhong','radioplay','opera','radio','finance','it','health','lvyou','qiche','youxi','openclass2','ccp','dianying','shishangshenghuo','poem']
    
    #url_type=['entertainment','comic','kid','3Dfell2','news','talk2','emotion','culture','renwen','chair','english','xiaoyuzhong','radioplay','opera','radio','finance','it','health','lvyou','qiche','youxi','openclass2','ccp','dianying','shishangshenghuo','poem']
    url_type=['music','kid','talk2']
    
   # url_type=['book','music','entertainment','comic','kid','news','talk2','emotion','culture','renwen','chair','english','xiaoyuzhong','radioplay','opera','radio','finance','it','health','lvyou','qiche','youxi','openclass2','ccp','dianying','poem']
    url_start = 'http://www.ximalaya.com/dq/'
    url_host=[]
    for i in range(len(url_type)):
        url = url_start + url_type[i]+"/"
        url_host.append(url)
    #对热门页面分析后，把每一页的各专辑地址放入queue_in队列
    
    for num in range(len(url_host)):
        html = urllib.urlopen(url_host[num]).read()
        tree = etree.HTML(html)
        pages = tree.xpath("//div[@class='pagingBar_wrapper']/a/text()")
        #print len(pages),"len pages"
        pages =[ int(i) for i in pages if i.isdigit()]     #判断是数字，只保留数字        
        if len(pages)==0:
            max_page=4
        else:
            max_page = max(pages)
        #    print pages
        #max_pages =5 
        
        os.chdir(os.getcwd()+'/'+album_folder_name)
        for page in xrange(1, max_page+1):
            print 'Page No: %s, type_name %s' % (page,url_host[num])
            #print url_host.index(num)
            url = '%s%s' % (url_host[num], page)
            #print url,"url----------------------"
            pageGetAlbums(url,url_type[num],page)
        os.chdir('..')
    #queue_in.join()
    #queue.join()
    #exit_flag.set()
    
    print 'All downloaded!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!'
    
