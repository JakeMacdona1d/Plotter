from tracemalloc import start
import matplotlib
import numpy as np
from numpy import *
import matplotlib.pyplot as plt

from fileSelect import startSel
from paramSet import startPSet,ParamReturn
from functions import *


import math


df = startSel()
pr = startPSet(df)


sizeVal = int(pr.size) 
iterVal = int((df.shape[0]-1)/sizeVal)

if sizeVal>df.shape[0] :
    raise ("size exceeds range of data")
    
X = np.zeros((sizeVal,sizeVal))


equation = pr.equ

maxColor = -1000000
minColor = 10000000
# for i in range(sizeVal) :
maxColor = getMax( df[pr.c1].tolist()[1:])
minColor = getMin( df[pr.c1].tolist()[1:])
minY = getMin(df[pr.s].tolist()[1:])
maxY = getMax(df[pr.s].tolist()[1:])
minG = getMin(df[pr.x].tolist()[1:])
maxG = getMax(df[pr.x].tolist()[1:])


#For the data I am using, this is makes things better
maxG = 6
minY = 1.5


#overestimates number of bins
numBin = int(round((maxG - minG)/0.25))

numOfData = int((df.shape[0]-1))

listPoints =  seperateLists(df[pr.s].tolist()[1:], numOfData, numBin) 


for i in range(numBin) :
    if listPoints[i] == 0:
        numBin = i+1
        break


refiguredList = buildList(df[pr.s].tolist()[1:],df[pr.x].tolist()[1:],df[pr.c1].tolist()[1:],listPoints,numOfData)

print (refiguredList)



usedPosit = np.zeros((pow(sizeVal,2), 3))

positCount = 0


#Simpy, this serves as the mapping process.
#Assigns color value to location in graph. 
for i in range(numOfData) :
    xVal = refiguredList[i][1]
    yVal = refiguredList[i][0]
    xVal-=minG
    yVal-=minY
    percentX = xVal/(maxG-minG)
    xVal= int(round(percentX * sizeVal)) -1
    percenty = yVal/(maxY-minY)
    yVal = int(round(percenty * sizeVal)) -1

    if xVal >= sizeVal : continue
    if yVal < minY: continue

    value = eval(equation.replace("x", str(refiguredList[i][2])))

    if X[yVal][xVal] == 0:
        X[yVal][xVal] = value
        usedPosit[positCount][0] = yVal
        usedPosit[positCount][1] = xVal
        usedPosit[positCount][2] = 1
        positCount+=1
    else: 
        num = getPosit (usedPosit, positCount, yVal, xVal)
        if num == None : continue
        X[yVal][xVal] += value
        usedPosit[num][2] +=1

for i in range (positCount) : 
    y = int(usedPosit[i][0])
    x = int(usedPosit[i][1])
    X[y][x] /= usedPosit[i][2]


#Functions to manipulate apearance
################################################################
# function replaces unfilled elements in matrix with min or max color value
# X = fillRest(X, sizeVal, minColor, maxColor)

#
# X = smooth (X, usedPosit, positCount, sizeVal, maxColor, minColor)
# X = averaging (X, sizeVal)
#################################################################

# Will worry about the line plot after the contour
# numOfPoints = numBin
# iterValForPoints = int((df.shape[0]-1)/numOfPoints)
# G = np.zeros(numOfPoints)
# Y = np.zeros(numOfPoints)


# # for i in range(numOfPoints) : 
# #     G[i] = df[pr.x].tolist()[(i*iterValForPoints)+1]
# #     Y[i] = df[pr.s].tolist()[(i*iterValForPoints)+1]

# for i in range(numBin-1) : 
#     pos = listPoints[i]
#     G[i] = refiguredList[pos][1]
#     Y[i] = refiguredList[pos][0]


# numOfxTicks = numOfPoints
# xticLab = [""] * numOfxTicks
# xticVal = [0.0] * numOfxTicks

# difG = maxG - minG
# increaseFacx = difG/numOfxTicks
# increaseFacxVal = sizeVal/numOfxTicks
# for i in range(numOfxTicks):
#     xticVal[i] = i*increaseFacxVal
#     xticLab[i] = str(round((increaseFacx*i) +minG,2))


# ######################### 

# numOfyTicks = numOfPoints
# yticLab = [""] * numOfyTicks
# yticVal = [0.0] * numOfyTicks

# difY = maxY - minY
# increaseFacy = difY/numOfyTicks
# increaseFacyVal = sizeVal/numOfyTicks
# for i in range(numOfyTicks):
#     yticVal[i] = i*increaseFacyVal
#     yticLab[i] = str(round((increaseFacy*i) +minY,2))

# ######################### 

# for i in range(numOfPoints) : 
#     G[i]-=minG
#     Y[i]-=minY

#     percentG = G[i]/(maxG-minG)
#     G[i] = percentG * sizeVal
#     percentY = Y[i]/(maxY-minY)
#     Y[i] = percentY * sizeVal

  
matplotlib.rcParams['font.family'] = 'Arial'

c = plt.imshow(X, cmap ='viridis',
                 extent =[minG, maxG, minY, maxY],
                    interpolation ='lanczos', origin ='lower')
                    #                 extent =[1.5, 4.5, 1.5, 3],


plt.xlabel(pr.indLab, labelpad = 5 )
plt.ylabel(pr.depLab, labelpad= 5)
a = plt.colorbar(c)
a.set_label(pr.colorLab, labelpad = 10)
  
plt.title(pr.title)

plt.show()


#color mesh achieves similar func. Imshow just holds your hand more. 
#Imshow will deduce dimensions automatically, decide ticks, etc

# plt.xlabel(pr.indLab, labelpad = 5 )
# plt.ylabel(pr.depLab, labelpad= 5)
# plt.xticks(xticVal,xticLab, rotation = 45)
# plt.yticks(yticVal,yticLab)

# plt.scatter(G,Y, color = 'white', s = 50)
# plt.plot(G, Y, '-o', color = 'white')

# plt.pcolormesh(X,cmap="viridis")
# plt.title(pr.title)

# a = plt.colorbar()
# a.set_label(pr.colorLab, labelpad = 10)


# plt.show()