#coding=utf-8

from html.parser import HTMLParser
from urllib import request
import json
import os
import sys
import re
#提取sound id，提取专辑名称用于创建该专辑文件夹
class TypeEventHtmlParser(HTMLParser):
    album_type_title=""
    title_flag=False
    album_ids=set()
    
    def __init__(self):
        HTMLParser.__init__(self):
        self.ablum_ids=[]
        self.album_type_title=""
        title_flag=False
    def handle_starttag(self,tag,attrs):
        if tag == 'a':
            for name,value in attrs:
                if name=='href' and attrs.['class']=='albumface' and value.startswith('http'):
                    album_ids.add(value)
                    print value
        if tag == 'title':
            self.title_flag=True

    def handle_data(self,data):
        if self.title_flag:
            rstr_list = re.findall(r"【(.*)】", data)
            self.album_type_title=rstr_list[0]
            print(self.album_type_title)
            self.title_flag=False

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

    type_folder=""
    type_addrs=[]
    #本地文件存储专辑链接地址，可以一次下载多个专辑
    #with open('albumaddr.txt','r') as addr_file:
        #album_addrs = addr_file.readlines()
    with open('sound_type.txt','r') as type_file:
        type_addrs=type_file.readline()
    for type in type addrs:
        
        album_addrs=[]
        album_folder=""
        type_parser=TypeEventHtmlParser()
        with request.urlopen(addr) as type_file:
            html1=type_file.read().decode('utf-8')
            
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

            for sound_id in sound_ids:       
                with request.urlopen(('http://www.ximalaya.com/tracks/' + sound_id + '.json')) as music_f:
                    music_json = json.loads(music_f.read().decode('utf-8'))
                print(music_json['title']+'downloding...')
                request.urlretrieve(music_json['play_path'], './' + album_folder + '/' + music_json['title'] + '.mp3')
                print(music_json['title']+'downloaded')    

parse_python_events()
