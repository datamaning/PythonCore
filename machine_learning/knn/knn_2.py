#!/usr/bin/python
from numpy import *
import kNN
def file2matrix(filename):
    fr=open(filename)
    arrayOLines=fr.readlines()
    numberOfLines=len(arrayOLines)
    returnMat=zeros((numberOfLines,3))
    print numberOfLines,"\n"
    print returnMat,"1111"
    classLabelVector=[]
    index=0
    for line in arrayOLines:
        line=line.strip()
        listFromLine=line.split('\t')
        returnMat[index,:]=listFromLine[0:3]
        classLabelVector.append(int(listFromLine[-1]))
        index+=1
    return returnMat,classLabelVector
#reload(kNN)
datingDataMat,datingLabels=file2matrix("datingTestSet2.txt")
print datingDataMat
