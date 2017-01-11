#!/usr/bin/env python

from time import ctime
from urllib2 import urlopen

TICKs=('yhoo','dell','cost','abde','intc')
URL='http://quote.yahoo.com/d/quotes.csv?s=%s&f=sllclp2'

print '\nPrices quoted as of :%s PDT\n' % ctime()
print 'TICKER','PRICE','CHANGE','%ACE'
print '------','------','-------','-------'
u=urlopen(URL% ','.join(TICKs))

for row in u :
    tick,price,chg,per=row.split(',')
    print tick,'%.2f' % float(price),chg,per,
u.close()

