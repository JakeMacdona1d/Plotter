# Jake Macdonald, 8/2/2022
# This program serves as a means to rapidly plot
# superconducting transitions within a data set.
# Was primarily developed for use by LabEQ, a research 
# organization studying quantum systems @ Clemson University.  

import numpy as np
from numpy import *
import matplotlib.pyplot as plt
from fileSelect import startSel
from paramSet import startPSet
from functions import *


df = startSel()
pr = startPSet(df)

sizeVal = int(pr.size) 
iterVal = int((df.shape[0]-1)/sizeVal)

if sizeVal>df.shape[0] :
    raise ("size exceeds range of data")
    
X = np.zeros((sizeVal,sizeVal))
XChange = np.ones((sizeVal,sizeVal), dtype=bool)

equation = pr.equ

maxColor = -1000000
minColor = 10000000
maxColor = getMax( df[pr.c1].tolist()[1:])
minColor = getMin( df[pr.c1].tolist()[1:])
miny = getMin(df[pr.s].tolist()[1:])
maxy = getMax(df[pr.s].tolist()[1:])
minx = getMin(df[pr.x].tolist()[1:])
maxx = getMax(df[pr.x].tolist()[1:])

#overestimates number of bins
numOfData = int((df.shape[0]-1))
numBin = numOfData


# Reassigning value to the below variables 
# Acts as a means to define a scope for the plot
maxx = 4.5
minx = 2
miny = 1.9
maxy = 4.5

# scope values for two transition data
# maxx = 3
# minx = 1.75
# miny = 3.35
# maxy = 4.6

listPoints =  seperateLists(df[pr.s].tolist()[1:], numOfData, numBin) 

for i in range(numBin) :
    if listPoints[i] == 0:
        numBin = i+1
        break

refiguredList = buildList(df[pr.s].tolist()[1:],df[pr.x].tolist()[1:],df[pr.c1].tolist()[1:],listPoints,numOfData)

print (refiguredList)

usedPosit = np.zeros((pow(sizeVal,2), 3))

positCount = 0

#Simply, this serves as the mapping process.
#Assigns color value to location in graph. 
for i in range(numOfData) :
    xVal = refiguredList[i][1]
    yVal = refiguredList[i][0]

    # Do not want points outside set scope
    if xVal < minx : continue
    if yVal < miny: continue
    if xVal > maxx : continue
    if yVal > maxy: continue

    xVal-=minx
    yVal-=miny
    percentX = xVal/(maxx-minx)
    xVal= int(round(percentX * sizeVal)) -1
    percenty = yVal/(maxy-miny)
    yVal = int(round(percenty * sizeVal)) -1

    if xVal >= sizeVal : continue
    if yVal >= sizeVal : continue

    value = eval(equation.replace("a", str(refiguredList[i][2])))

    if X[yVal][xVal] == 0:
        X[yVal][xVal] = value
        XChange[yVal][xVal] = False

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


#Functions to manipulate apearance/ interpolating
################################################################
# X = smooth (X, XChange ,usedPosit, positCount, sizeVal, maxColor, minColor)
X = assignHighest(X, sizeVal)
X = pseudoFill(X, sizeVal) # Means of interpolation may need to vary per data set 
X = averaging (X, sizeVal)

#################################################################

#Superconducting transition points
#####################################################
#Points that will even be considered. 

numOfPoints = 50

G = np.zeros(sizeVal)
Y = np.zeros(sizeVal)

devAccept = .05
targetPoint = (maxColor/4)
pointsFound = 0

# Finding transition points. Only accepts points within specified deviaiton
for i in range (sizeVal) :
    for j in range (sizeVal) :
        if inTargetDeviation (X[j][i], targetPoint, devAccept):
            G[i] = i
            Y[i] = j
            pointsFound+=1

# The point mapping process
yrange = maxy - miny
minY = getMin(Y)
maxY = getMax(Y)
minG = getMin(G)
maxG = getMax(G)
Yrange = maxY - minY
Yscale = yrange/Yrange
xrange = maxx - minx
Grange = maxG - minG
Gscale = xrange/Grange

iterValForPoints = int(pointsFound/numOfPoints)
G = reduceList(G, iterValForPoints, pointsFound, numOfPoints)
Y = reduceList(Y, iterValForPoints, pointsFound, numOfPoints)

for i in range(numOfPoints) : 
    G[i] *= Gscale
    Y[i] *= Yscale
    G[i] += minx
    Y[i] += miny

# I have found that a lot of noisy data exists on the cusps of the matrix.
# This removes such points.
G = np.delete(G, np.where(Y <= miny))
Y = np.delete(Y, np.where(Y <= miny))

#View
########################################################
plt.rcParams['font.family'] = 'Arial'

c = plt.imshow(X, cmap ='viridis',
                 extent =[minx, maxx, miny, maxy],
                    interpolation ='lanczos', origin ='lower')
                   
plt.xlabel(pr.indLab, labelpad = 5 )
plt.ylabel(pr.depLab, labelpad= 5)
a = plt.colorbar(c)
a.set_label(pr.colorLab, labelpad = 10)
plt.scatter(G,Y, color = 'white', s = 25)
plt.plot(G, Y, '-o', color = 'white')
plt.title(pr.title)
plt.show()