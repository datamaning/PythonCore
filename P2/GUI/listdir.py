import os
from time import  sleep
from Tkinter import *

class DirList(object):
    def __init__(self):
        self.top=Tk()
        self.label=Label(self.top,text='Directory Lister v1.1')
        self.label.pack()
        self