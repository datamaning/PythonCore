#!/usr/bin/python
from numpy import *
import operator

def createDateset():
    group=([[1.0,1.1],[1.0,1.0],[1.0,1.0],[0,0],[0,0.1]])
    labels=['A','A','B','B']
    return groups,labels

import kNN
groups,labels=createDateset()

