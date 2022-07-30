import numpy as np

#y = field(t), x= temp, g = resistance
def buildList(y, x, g, difPoints, size ) :
    composite = np.zeros((size,3))
    iteration = 0
    lastVal = 0
    for i in range(size):
        composite[i][0] = float(y[i])
        composite[i][1] = float(x[i])
        composite[i][2] = float(g[i])
        if i == difPoints[iteration]:
            composite[lastVal:i] = sort(composite[lastVal:i])
            lastVal = i
        # if composite[i][1] > 5.99: 
        #             np.delete(composite, i)
        #             print ("woag")
    return composite


#Sorting arrays by ascending value of y, for this instance, field
# Just bubble sort currently, if wanted, could use quicksort instead
def sort(array):
    n = len(array)
    for i in range(n):
        sorted = True
        for j in range(n - i - 1):
            if array[j][1] > array[j + 1][1]:
                array[j+1][0], array[j][0] = array[j][0], array[j+1][0]
                array[j+1][1], array[j][1] = array[j][1], array[j+1][1]
                array[j+1][2], array[j][2] = array[j][2], array[j+1][2]
                sorted = False
        if sorted:
            break
    return array

#Checks when the function flips growth
def dirChange(list) :
    tracking = 10
    sum = 0
    for i in range (tracking) :
        try:
            sum += float(list[i])
        except: return 

    if float(list[0]) > (sum) / tracking :
        return False

    return True

def seperateLists(list, size, numBins) :
    dataSep = [0] * numBins
    seps = 0
    positiveChange = True
    startCheck = False

    sinceLast = 0
    for i in range(size) :
        if (round(float(list[i]),2) <= -0.499) and sinceLast > 100:
            startCheck = True
        if startCheck:
            newPosChange = dirChange(list[i:])
            if not (positiveChange == newPosChange) :
                dataSep[seps] = i
                seps += 1
                startCheck = False
                sinceLast = 0
                if positiveChange : positiveChange = False
                else: positiveChange = True
        sinceLast +=1

    return dataSep


        
        

# before
##########################
def fillRest(matrix, size, min, max): 
    for i in range(size) :
        below = True
        for j in range(size) :
            if not matrix[j][i] == 0: 
                below = False
                continue
            if below:
                matrix[j][i] = min
            else: matrix[j][i] = max
    return matrix


def spread(matrix, val, size, change, x, y, initY, max, min):
    if size < 0 : return matrix
    matrix = spread(matrix, val, size -1, change, x, y+1, initY, max, min)
    negY = initY + (initY - y)

    for i in range (2*size):
        curX = x + (i - size)
        addVal = val * pow (change, abs(i - size))
        try: # bad practice, ik
            if not(i - size == 0 or matrix[y][curX] + addVal > max or matrix[y][curX] + addVal < min): 
                matrix[y][curX] += addVal
        except: pass

        try: 
            if not(i - size == 0 or matrix[negY][curX] + addVal > max or matrix[negY][curX] + addVal < min): 
                matrix[negY][curX] += addVal
        except: pass
            
    return matrix


def averaging (matrix, size) : 
    X = np.zeros((size,size))
    for i in range (size):
        for j in range (size):
            sum = 0
            count = 1
            sum += matrix[i][j]
            if i > 1 and not matrix[i-1][j] ==0 :
                sum += matrix[i-1][j]
                count+=1
            if size - i -1 > 1 and not matrix[i+1][j] ==0:
                sum += matrix[i+1][j]
                count+=1

            if j > 1 and not matrix[i][j-1] ==0:
                sum += matrix[i][j-1]
                count+=1
         
            if size - j > 1 and not matrix[i][j+1] ==0:
                sum += matrix[i][j+1]
                count+=1
         
            if i > 1 and j > i and not matrix[i-1][j-1] ==0 :
                sum += matrix[i-1][j-1]
                count+=1

            if size - i -1  and size - j -1 and not matrix[i+1][j+1] ==0:
                sum += matrix[i+1][j+1]
                count+=1

            if j > 1 and size - i -1 and not matrix[i+1][j-1] ==0:
                sum += matrix[i][j-1]
                count+=1
         
            if j > 1 and size - j -1 and not matrix[i-1][j+1] ==0:
                sum += matrix[i][j+1]
                count+=1

            X[i][j] = sum / count
    return X


def smooth (matrix, positions, posCount, size, max, min) :
    for i in range (posCount):
        x = int(positions[i][0])
        y = int(positions[i][1])
        steps = int(positions[i][2] * 5)
        change = 1 -1/steps
        matrix = spread(matrix, matrix[x][y], steps, change, y, x, x, max, min)
    
    return matrix


# Find deviants in color value
#####################################
def getMean (matrix, positions, posCount) :
    sum = 0
    for i in range (posCount):
        x = int(positions[i][0])
        y = int(positions[i][1])
        sum += matrix[x][y]
    return sum/posCount


def getStd (matrix, positions, posCount, mean):
    sumVal = 0
    for i in range (posCount):
        x = int(positions[i][0])
        y = int(positions[i][1])
        sumVal+= pow((matrix[x][y] - mean),2)
    return pow((sumVal/posCount),1/2)


def removeOutlier (matrix, positions, posCount):
    mean = getMean(matrix, positions, posCount)
    std = getStd(matrix, positions, posCount, mean)
    for i in range (posCount):
        x = int(positions[i][0])
        y = int(positions[i][1])
        dif = matrix[x][y] - mean
        if abs(dif) > 2.5 * std :
            matrix[x][y] = 0

    return matrix

#######################################################


# Find deviants in pos value
#####################################
def findClosestVal (positions, posCount, val, target) :
    min = 1000000000
    for i in range(posCount):
        cur = abs(target - positions[i][val])
        if cur == target: continue
        if cur < min: min = cur
    return min
            


def removeOutlierPos (matrix, positions, posCount, size):
    for i in range (posCount): 
        x = int(positions[i][0])   
        y = int(positions[i][1])

        if (findClosestVal(positions, posCount, 0, x) / size) > 0.1 :
            if (findClosestVal(positions, posCount, 1, y) / size) > 0.1 :
                matrix[x][y] = 0
      
    return matrix

#######################################################


def getPosit (list, size, x, y) :
    for i in range(size) :
        if list[i][0] == x :
            if list[i][1] == y :
                return i

def getMin(list) :
    min = 10000000000
    for i in list :
        if min > float(i): 
            min = float(i)
    return min

def getMax(list) :
    max = -10000000000
    for i in list :
        if max < float(i): 
            max = float(i)
    return max