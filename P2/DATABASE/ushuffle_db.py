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
            import sqlite3
    elif db == 'mysql':
        try:
            import MySQLdb
            import _mysql_exceptions as DB_EXC
        except ImportError:
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
    return cxn
def create(cur):
    try:
        cur.execute('''
        
   CREATE TABLE USERS (    login varchar(%d),
        userid INTEGER,
        projid INTEGER)
        ''' % NAMELEN)
    except DB_EXC.OperationalError:
        drop(cur)
        create(cur)
drop=lambda cur:cur.execute("Drop table users")

NAMES=(('arron',8312),('Angela',7603),('dave',7306),('davina',7902),('elliot',7911),('ernie',7410),('jess',7912),('jim',7512),('larry',7311),('leslie',7808),('melissa',8602),('pat',7711),('serena',7003),('stan',7607),('faye',6812),('amy',7209),('mona',7404),('jennifer',7608),)

def randName():
    pick=set(NAMES)
    while pick:
        yield pick.pop()
def insert(cur,db):
    if db=='mysql':
        cur.executemany("INSERT INTO USERS VALUES(%s,%s,%s)",[(who,uid,rand(1,5))for who,uid in randName()])

getRC=lambda cur:cur.rowcount if hasattr(cur,'rowcount') else -1

def update(cur):
    fr=rand(1,5)
    to=rand(1,5)
    cur.execute("UPDATE USERS SET projid=%d where projid=%d" % (to,fr))
    return fr,to,getRC(cur)

def delete(cur):
    rm=rand(1,5)
    cur.execute("DELETE FROM USERS WHERE projid=%d" %rm)
    return rm,getRC(cur)

def dbDump(cur):
    cur.execute("SELECT * FROM USERS")
    print '\n%s' % ''.join(map(cformat,FIELDS))
    for data in cur.fetchall():
        print ''.join(map(tformat,data))

def main():
    db=setup()
    print '***Connect to %r database ' % db
    cxn=connect(db)
    if not cxn:
        print 'Error: %r not supported or unreachable,existing' % db 
        return
    cur=cxn.cursor()
   
    print '\n***Create users table (drop old one if appl.)'
    create(cur)
    print '\n***Insert names into table'
    insert(cur,db)
    dbDump(cur)

    print '\n***Move users to a random group'
    fr,to,num=update(cur)
    print '\t(%d users moved) from (%d) to (%d)' % (num,fr,to)
    dbDump(cur)

    print '\n*** Randomly delete group'
    rm,num=delete(cur)
    print '\t(group #%d; %d users removed)' % (rm,num)
    dbDump(cur)

    print '\n*** Drop users table'
    drop(cur)
    print '\n*** Close cxns'
    cur.close()
    cxn.commit()
    cxn.close()

if __name__=='__main__':
    main()


