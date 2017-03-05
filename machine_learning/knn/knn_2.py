#!/usr/bin/python
def file2matrix(filename):
    fr=open(filename)
    arrayOLines=fr.readlines()
    numberOfLines=len(arrayOLines)
    returnMat=zeros((numberOfLines),3)
    print numberOfLines,"\n"
    print returnMat
    classLabelVector=[]
    index=0
    for line in arrayOLines:
        line=line.strip()
        listFromLine=line.split('\t')
        returnMat[index,:]=listFromLine[0:3]
        classLabelVector.append(int(listFromLine[-1]))
        index+=1
    return returMat,classLabelVector
reload(kNN)
datingDataMat,datingLabels=kNN.file2matrix("datingTestMatrix.txt")
