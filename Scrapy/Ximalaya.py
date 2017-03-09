import urllib
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

socket.setdefaulttimeout(20)
queue=Queue(200)

