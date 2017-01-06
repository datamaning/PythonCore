#!/usr/bin/env python

import os
from random import randrange as rand

COLSIZ=10
FIELDS=('login','userid','projid')
RDBMS={'s':'sqlite','m':'mysql','g':'gadfly'}
DBNAME='TEST'
DBUSER='root'
DB_EXEC=None
NAMELEN=16

tformat=lambda s: str(s).title().ljust(COLSIZ)
cformat=lambda s: s.upper().ljust(COLSIZ)

def setup():
    return RDBMS[raw_input('''
    choose a database system:
    (M)ySQL
    (G)adfly
    (S)QLite
    
    Enter choice:''').strip().lower()[0]]
def connect(db):
    global DB_EXC
    dbDir='%s_%s' % (db,DBNAME)
    if db=='sqlite':
        try:
            import sqlite3
    elif db=='mysql':
        try:
            import MySQLdb
            import _mysql_exceptions as DB_EXC
        eccept ImportError:
            return None
        
        try:
            cxn=MySQLdb.connect(db=DBNAME)
        except DB_EXC.OperationalError:
            try:
                cxn=MySQLdb.connect(user=DNUSER)
                cxn.query('CREATE DATABSE %s' % DBNAME)
                cxn.commit()
                cxn.close()
                cxn=MySQLdb.connect(db=DBNAME)
            except DB_EXC.OperationalError:
                return NONE
def create(cur):
    try:
        cur.execute('''
        login varchar(%d),
        userid INTEGER,
        projid INTEGER
        ''' % NAMELEN)
    except DB_EXC.OperationalError:
        drop(cur)
        create(cur)
drop=lambda cur:cur.execute("Drop table users")

NAMES={
        ('arron',8312) 
        }
        )


