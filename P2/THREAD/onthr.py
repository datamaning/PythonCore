#!/usr/bin/python
from time import sleep,ctime
def loop0():
    print("start loop 0 at:",ctime())
    sleep(4)
    print("start loop 0 at:",ctime())
def loop1():
    print("start loop 1 at:",ctime())
    sleep(2)
    print("start loop 1 at:",ctime())
def main():
    print("starting at :",ctime())
    loop0()
    loop1()
    print("all done at:",ctime())
if __name__=='__main__':
    main()