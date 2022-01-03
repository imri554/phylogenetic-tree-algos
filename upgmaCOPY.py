
import sys
import copy

def getSmallest(dictMatrix):
    small = float('inf')
    smallestKeyFirst = None
    smallestKeySecond = None
    for key in dictMatrix.keys():
        for each in dictMatrix[key].keys():
            if dictMatrix[key][each] < small:
                small = dictMatrix[key][each]
                smallestKeyFirst = key
                smallestKeySecond = each
    return small, smallestKeyFirst, smallestKeySecond

def newDistance(i, j, k, oldMatrix):
    options = [i, k]

    #lexicographical sorting of the letters and column heads for function purposes
    options.sort()
    part1 = oldMatrix[options[0]][options[1]]

    options = [j, k]
    options.sort()
    part2 = oldMatrix[options[0]][options[1]]

    dist = (part1 + part2) * 0.5

    return dist

def groupAnswer(previousAnswer, i, j):
    if previousAnswer is None:
        newAnswer = "(" + i + "," + j + ")"
        return newAnswer
    else:
        newAnswer = "(" + i + "," + j + ")"
        return newAnswer

def addToDot(i, j, currentAnswer, outputWriter, heightList):
    i = i.replace("(","").replace(")","")
    j = j.replace("(","").replace(")","")
    heightList[i + "," + j] = heightList[i] + 1

    # depth = 0
    # depthI = 0
    # depthJ = 0
    # for each in i:
    #     if each == "(":
    #         depthI += 1
    # for each in j:
    #     if each == "(":
    #         depthJ += 1
    # for each in currentAnswer:
    #     if each == ",":
    #         depth += 1
    iEntry = ''.join(filter(str.isalnum, i))
    jEntry = ''.join(filter(str.isalnum, j))


    #outputWriter.write( str(iEntry) + str(heightList[i]) + " -- " + str(iEntry) + str(jEntry)+str(heightList[i + "," + j]) + ";" + "\n")
    outputWriter.write( "\"" + str(iEntry) + str(jEntry)+str(heightList[i + "," + j]) + "\"" + " -- " +  "\"" + str(iEntry) + str(heightList[i]) + "\"" + "\n")
    outputWriter.write( "\"" + str(iEntry) + str(jEntry)+str(heightList[i + "," + j]) + "\"" + " -- " + "\"" + str(jEntry) + str(heightList[j]) + "\"" + "\n")# addnumber of parenthases gives the tree height situation)


def newDMatrix(i, j, matrix, currentAnswer, outputWriter, heightList):
    oldMatrix = copy.deepcopy(matrix)
    addToDot(i, j, currentAnswer, outputWriter, heightList)
    #first column
    matrix["(" +i + ',' + j + ")"] = matrix[i]
    #merging these add to the file

    del matrix[i]
    del matrix["(" + i + ',' + j + ")"][j]

    for each in matrix.keys():
        if i in matrix[each].keys():
            matrix[each]["(" +i + ',' + j+ ")"] = matrix[each][i]
            del matrix[each][i]
        if j in matrix[each].keys():
            del matrix[each][j]
    if j in matrix.keys():
        del matrix[j]

    for each in matrix.keys():
        lexico = ["(" +i + ',' + j+ ")", each]
        lexico.sort()
        if each != ("(" + i + ',' + j+ ")"):
            matrix[lexico[0]][lexico[1]] = newDistance(i, j, each, oldMatrix)
    return matrix

#reading in the necessary parameters
distanceMatrixPath = sys.argv[1]
outputFilePath = sys.argv[2]

#initialize important factors
matrixXIndices = {}
smallest = float("inf")


file_object = open(distanceMatrixPath, "r")
leafs = []

#creating the dictionary of dictionaries that represents the distance matrix
for line in file_object:
    if line is None:
        print("empty")
        quit()
for line in file_object:
    elements = line.split()
    toSort = [elements[0], elements[1]]
    toSort.sort()
    elements[0] = toSort[0]
    elements[1] = toSort[1]
    if elements[0] not in matrixXIndices.keys():
        leafs.append(elements[0])
        matrixXIndices[elements[0]] = {elements[1]: float(elements[2])}
    elif elements[0] in matrixXIndices.keys():
        if elements[1] not in matrixXIndices[elements[0]].keys():
            leafs.append(elements[1])
            matrixXIndices[elements[0]][elements[1]] = float(elements[2])

leafs = list(set(leafs))
heightList = {}
for each in leafs:
    heightList[each] = 0

treeHeight = 0

#beginning of the output answer text
answer = None

#make a deep copy so that the new distance matrix can be calculated easily
newDistanceMatrix = matrixXIndices.copy()

outputFile = open(outputFilePath, 'w')

outputFile.write("graph mytree {" + "\n")

while len(newDistanceMatrix.keys()) > 1:
    smallestValue, i, j = getSmallest(newDistanceMatrix)
    options = [i, j]
    options.sort()
    answer = groupAnswer(answer, options[0], options[1])
    newDistanceMatrix = newDMatrix(i, j, newDistanceMatrix, answer, outputFile, heightList)

    treeHeight = treeHeight + 1

#smallestValue, i, j = getSmallest(newDistanceMatrix)
if i is not None and len(newDistanceMatrix[list(newDistanceMatrix.keys())[0]]) != 0:
    answer += "," + str(list(newDistanceMatrix[list(newDistanceMatrix.keys())[0]].keys())[0]) + ")"
    #HAVE TO ALSO WRITE IN SOMETHING FOR THE LAST ONE
outputFile.write("}")

#key =
#key = list(newDistanceMatrix[key[0]].keys())
#answer += "," + str(key[0]) + ")"
print(answer)



#def UPGMA():
    #while len(matrixXIndices.keys()) >  0: