# encoding: utf-8
from numpy import *
def loadExData():
    return [[1,1,1,0,0],
            [2,2,2,0,0],
            [1,1,1,0,0],
            [5,5,5,0,0],
            [1,1,0,2,2],
            [0,0,0,3,3],
            [0,0,0,1,1]
            ]
data=loadExData()
U,Sigma,VT=linalg.svd(data)
'''
print 'U',U
print 'Sigma',Sigma
print 'VT',VT
'''

from numpy import linalg as la

def ecludSim(inA,inB):
    #print la.norm(inA-inB)
    return 1.0/(1.0+la.norm(inA-inB))

def pearsSim(inA,inB):
    if len(inA) <3 :return 1.0
    return 0.5+0.5*corrcoef(inA,inB,rowvar=0)[0][1]

def cosSim(inA,inB):
    num=float(inA.T*inB)
    denom=la.norm(inA)*la.norm(inB)
    return 0.5+0.5*(num/denom)

myMat=mat(data)
'''
print ecludSim(myMat[:,0],myMat[:,4])
print ecludSim(myMat[:,0],myMat[:,0])

print cosSim(myMat[:,0],myMat[:,4])
print cosSim(myMat[:,0],myMat[:,0])
'''

def standEst(dataMat,user,simMeas,item):
    n=shape(dataMat)[1]
    simTotal=0.0
    ratSimTotal=0.0
    for j in range(n):
        userRating=dataMat[user,j]
        if userRating ==0: continue
        overLap=nonzero(logical_and(dataMat[:,item].A>0,
            dataMat[:,j].A>0))[0]
        if len(overLap)==0:similarity=0
        else:similarity=simMeas(dataMat[overLap,item],dataMat[overLap,j])
        #print similarity,simTotal,overLap
        simTotal+=similarity

        ratSimTotal+=similarity*userRating
    if simTotal==0:return 0
    else: return ratSimTotal/simTotal

def recommend(dataMat,user,N=3,simMeas=cosSim,estMethod=standEst):
    unratedItems=nonzero(dataMat[user,:].A==0)[1]
    #print type(unratedItems),len(unratedItems),unratedItems
    if len(unratedItems)==0: return 'you rated everything'
    itemScores=[]
    for item in unratedItems:
        estimatedScore=estMethod(dataMat,user,simMeas,item)
        itemScores.append((item,estimatedScore))
    return sorted(itemScores,key=lambda jj:jj[1],reverse=True)[:N]

myMat[0,1]=myMat[0,0]=myMat[1,0]=myMat[2,0]=4
myMat[3,3]=2
myMat=mat([[4,4,0,2,2],
           [4,0,0,3,3],
           [4,0,0,1,1],
           [1,1,1,2,0],
           [2,2,2,0,0],
           [1,1,1,0,0],
           [5,5,5,0,0]
    ])
print myMat[[0,3,4,5,6],2]
print recommend(myMat,2)
