#!/usr/bin/env python

from distutils.log import warn as printf 
from json import dumps
from pprint import pprint

BOOKS={
        '0132269937':{
            'title':'Core Python Programming',
            'edition':2,
            'year':2017,
            },
        '0132356139':{
            'totle':'Python Web Development with Django',
            'authors':['Jeff Forcier','Paul Bissex','Wesley Chun'],
            'year':2009
            },
        '0137143419':{
            'title':'Python Fundamentals',
            'year':2009,
            },
        }
printf('*** RAW DICT ***')
printf(BOOKS)

printf('\n*** PRETTY_PRINTED DICT ***')
pprint(BOOKS)

printf('\n*** RAW JSON')
printf(dumps(BOOKS))

printf('\n *** PRETTY_PRINTED JSON ***')
printf(dumps(BOOKS,indent=4))

