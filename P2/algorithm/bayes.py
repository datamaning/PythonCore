#!/usr/bin/env python
# encoding: utf-8
from numpy import *
def loadDataSet():
    postingList=[['my','dog','has','flea','problems','help','please'],\
            ['maybe','not','take','him','to','dog','park','stupid'],
            ['my','dalmation','is','so','cute','I','love','him'],
            ['stop','posting','stupid','worthless','garbage',],
            ['mr','licks','ate','my','steak','how','to','stop','him'],
            ['quit','buying','worthless','dog','food','stupid']
            ]
    classVec=[0,1,0,1,0,1]
    return postingList,classVec

def createVocabList(dataSet):
    vocabSet=set([])
    for document in dataSet:
        vocabSet=vocabSet|set(document)
    return list(vocabSet)

def setOfWordsVec(vocabList,inputSet):
    returnVec=[0]*len(vocabList)
    for word in inputSet:
        if word in vocabList:
            returnVec[vocabList.index(word)]=1
        else:
            print "the word : %s is not in my Vocabulary!" %word
    return returnVec
listPosts,listClasses=loadDataSet()
myVocabList=createVocabList(listPosts)
print myVocabList
print setOfWordsVec(myVocabList,listPosts[0])
trainMat=[]
for postinDoc in listPosts:
    trainMat.append(setOfWordsVec(myVocabList,postinDoc))
print trainMat


def trainNB0(trainMatrix,trainCategory):
    numTrainDocs=len(trainMatrix)
    print numTrainDocs
    numWords=len(trainMatrix[0])
    print numWords
    pAbusive=sum(trainCategory)/float(numTrainDocs)
    print pAbusive

    p0Num=zeros(numWords)
    p1Num=zeros(numWords)
    print p0Num,len(p0Num)
    p1Denom=0.0;p0Denom=0.0
    for i in range(numTrainDocs):
        if trainCategory[i]==1:
            p1Num+=trainMatrix[i]
            p1Denom+=sum(trainMatrix[i])
        else:
            p0Num+=trainMatrix[i]
            p0Denom+=sum(trainMatrix[i])
    p1Vect=p1Num/p1Denom
    p0Vect=p0Num/p0Denom
    print  p0Vect,p1Vect
    return p0Vect,p1Vect,pAbusive
trainNB0(trainMat,listClasses)
