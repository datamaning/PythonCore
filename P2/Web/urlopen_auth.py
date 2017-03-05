#/usr/bin/env python 

import urllib2

LOGIN='welsey'
PASSWORD="you'IINever Guess"
URL="http://localhost"
REALM='Secure Archile'

def hadnler_version(url):
    from urlparse import urlparse
    hdlr=urllib2.HTTPBasicAuthHandler()
    hdlr.add_password(REALM,urlparse(url)[1],(LOGIN,PASSWORD))[:-1]
    opener=urllib2.build_opener(opener)
    urllib2.install_opener(opener)
    return url

def request_version(url):

