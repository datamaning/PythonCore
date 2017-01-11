#!/usr/bin/env python

from xml.etree.ElementTree import Element,SubElement,tostring
from xml.dom.minidom import parseString

BOOKS={
        '0132269937':{
            'title':'Core Python Programming',
            'edition':2,
            'yead':2006,
            },
        '0132356139':{
            'title':'Python Web Development with Django',
            'authors':'Jeff Forcier:Paul Bissex:Wesley Chun',
            'year':2009,
            },
        '0137143419':{
            'title':'Python Fundamentals',
            'year':2009,
            },
        }

books=ELEMENT('books')
for isbn,info in BOOKs.iteritems():
    book=SubElement(books,'book')
    info=setdefault('authors','Wesley Chun')
    info=setdefault('edition',1)
    for key,val n info.iteritems():
        SubElement(book,key).text=','.join(str(val)).split(':'))

    xml=tostring(books)
    print '*** RAW XML ***'
    print xml


