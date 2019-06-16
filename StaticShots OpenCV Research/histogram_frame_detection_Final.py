#Copyright Luke Ding
#All Rights Reserved


import cv2
import numpy as np
import csv
import glob
import math
from collections import defaultdict
from matplotlib import pyplot as plt
import pickle

#takes two image files, and stacks the RGB channels on top of each other. Then compares the number of pixels where their frame by frame difference is greater than two.
def compare_roi(before,after):
    #creates arrays of RBG color differences
    blue1, green1, red1 = before[:,:,0],before[:,:,1],before[:,:,2]
    blue2, green2, red2 = after[:,:,0],after[:,:,1],after[:,:,2]
    matrix1 = np.row_stack((blue1,green1,red1))
    matrix2 = np.row_stack((blue2,green2,red2))
    matrix1 = matrix1.astype(int)
    matrix2 = matrix2.astype(int)

    #calculates the difference between the two matrices
    matrix3 = (np.absolute(matrix1 - matrix2) > 2)
    return matrix3.sum()

# Given a video file, four coordinates(region of interest), and a the number pieces the border should be split into, returns an array of arrays
# Return values are four arrays for differences between frames for top, bot, left right. bSize is number of pieces the borders are split up into
def find_static_shots(vFile,x1,y1,x2,y2,bSize):
    #each border thickness is 5% of the border, hence /20
    horzBorderThickness = int(math.floor((x2-x1)/20))
    vertBorderThickness = int(math.floor((y2-y1)/20))
    horzBorderLen = int(math.floor((y2-y1)/bSize))
    vertBorderLen = int(math.floor((x2-horzBorderThickness-x1-horzBorderThickness)/bSize))

    #read first image
    cap = cv2.VideoCapture(vFile)
    ret, startFrame = cap.read()

    #initialize lists
    frameDifferenceTop = [[] for i in range(bSize)]
    frameDifferenceBot = [[] for i in range(bSize)]
    frameDifferenceLeft = [[] for i in range(bSize)]
    frameDifferenceRight = [[] for i in range(bSize)]
    roiTopStart = [[] for i in range(bSize)]
    roiBotStart = [[] for i in range(bSize)]
    roiRightStart = [[] for i in range(bSize)]
    roiLeftStart = [[] for i in range(bSize)]
    roiBotEnd = [[] for i in range(bSize)]
    roiTopEnd = [[] for i in range(bSize)]
    roiLeftEnd = [[] for i in range(bSize)]
    roiRightEnd = [[] for i in range(bSize)]

    for i in range(bSize):
        #segment initial image into regions of interests based off of bSize
        roiTopStart[i] = startFrame[x1:x1 + horzBorderThickness , y1 + (i * horzBorderLen) : y1 + (i+1) * horzBorderLen - 1]
        roiBotStart[i] = startFrame[x2- horzBorderThickness:x2 , y1 + (i * horzBorderLen) : y1 + (i+1) * horzBorderLen - 1]
        roiLeftStart[i] = startFrame[x1 + horzBorderThickness + i * vertBorderLen : x1 + (i+1) * vertBorderLen - 1, y1: y1 + vertBorderThickness]
        roiRightStart[i] = startFrame[x1 + horzBorderThickness + i * vertBorderLen : x1 + (i+1) * vertBorderLen - 1, y2 - vertBorderThickness:y2]


    # open the file and record the frame differences
    while (cap.isOpened()):
        ret, endFrame = cap.read()
        if ret:
            for i in range(bSize):
                #segment the second frame
                roiTopEnd[i] = endFrame[x1:x1 + horzBorderThickness, y1 + i * horzBorderLen: y1 + (i + 1) * horzBorderLen - 1]
                roiBotEnd[i] = endFrame[x2 - horzBorderThickness:x2, y1 + i * horzBorderLen: y1 + (i + 1) * horzBorderLen - 1]
                roiLeftEnd[i] = endFrame[x1 + horzBorderThickness + i * vertBorderLen: x1 + (i + 1) * vertBorderLen - 1, y1: y1 + vertBorderThickness]
                roiRightEnd[i] = endFrame[x1 + horzBorderThickness + i * vertBorderLen: x1 + (i + 1) * vertBorderLen - 1, y2 - vertBorderThickness:y2]

                #find the difference between the two frames, and append to the differences list
                frameDifferenceTop[i].append(compare_roi(roiTopStart[i], roiTopEnd[i]))
                frameDifferenceBot[i].append(compare_roi(roiBotStart[i], roiBotEnd[i]))
                frameDifferenceLeft[i].append(compare_roi(roiLeftStart[i], roiLeftEnd[i]))
                frameDifferenceRight[i].append(compare_roi(roiRightStart[i], roiRightEnd[i]))

                #set the first frame to the second frame, cycle repeats
                roiTopStart[i] = roiTopEnd[i]
                roiBotStart[i] = roiBotEnd[i]
                roiLeftStart[i] = roiLeftEnd[i]
                roiRightStart[i] = roiRightEnd[i]

        if not ret:
            cap.release()

    return frameDifferenceTop,frameDifferenceBot,frameDifferenceLeft,frameDifferenceRight

#Plot the number of borders that are determined to be non-static
def plot_differences (top,bot,left,right):
    runningList = []
    for i, value in enumerate(top):
        runningList.append(0)
        if top[i] > 0:
            runningList[i] += 1
        if bot[i] > 0:
            runningList[i] += 1
        if left[i] > 0:
            runningList[i] += 1
        if right[i] > 0:
            runningList[i] += 1
    plt.plot(runningList)
    plt.show()


#Given a differences list, number of pieces the border is divided into(pieceNum), threshold for pixels to be different(pieceThreshold)
#and number of border pieces that can be non-static before the entire edge is determined to be non static, computer whether this edge is static
def find_static_edge (edge, pieceNum, pieceThreshold, piecesBad):

    listLen = len(edge[0])

    sumList = np.zeros(listLen,dtype = int)
    returnList = [True for i in range(listLen)]

    for j in range(pieceNum):
        for i in range(listLen):
            if edge[j][i] > pieceThreshold:
                sumList[i] = sumList[i] + 1

    for k in range(listLen):
        if sumList[k] > piecesBad:
            returnList[k] = False
        else:
            returnList[k] = True

    return returnList

# Returns a dictionary of static shots with starting frames (keys), ending frames (values)
# Takes in four lists of true/false information for each static frame, how many of the 4 lists can be static (borderThreshold), and how many consecutive static frames needed
def find_static_frames (top, bot, left, right, borderThreshold, frameThreshold):
    counter = 0
    staticFrames = dict()
    for i, value in enumerate(top):
        if (top[i] + bot[i] + left[i] + right[i]) >= borderThreshold:
            counter = counter + 1
        elif(counter >= frameThreshold):
            staticFrames[i-counter] = i-1
            counter = 0
        else:
            counter = 0

    if counter >= frameThreshold:
        staticFrames[len(top) - 1 - counter] = len(top) - 1

    return staticFrames

def play_video (vFile, staticFile):
    startingList = list(staticFile)
    print(startingList)
    cap = cv2.VideoCapture(vFile)

    firstFrame = startingList[0]
    for i in range(firstFrame):
        cap.read()

    # open the file
    for i in range(len(startingList)):
        if len(startingList) == 0:
            break
        firstFrame = startingList[i]
        lastFrame = staticFile[startingList[i]]
        for j in range(lastFrame-firstFrame):
            ret, frame = cap.read()
            if ret:
                cv2.imshow('Window',frame)
                cv2.waitKey(12)
            else:
                cap.release()
        if cv2.waitKey(0) & 0xFF == ord('q'):
            exit()
        if i == len(startingList)-1:
            break
        else:
            skipFrames = startingList[i+1]-lastFrame
            for k in range(skipFrames):
                cap.read()
    cv2.destroyAllWindows()

#saves to pickle file
def saveList (list, name):
    with open(str(name)+'.pickle', 'wb') as handle:
        pickle.dump(list, handle, protocol=pickle.HIGHEST_PROTOCOL)

#saves to csv
def saveListCSV (list, listName,filename,ix,iy,fx,fy,count):
    with open(filename, 'a') as f:
        f.write('%s|(%s,%s)|(%s,%s)|%s|' % (listName, ix, iy, fx, fy, count))
        for key in sorted(list.keys()):
            f.write("(%s,%s)|" % (key, list[key]))
        f.write('\n')

#read lists
def readList (filename):
    with open(filename, 'rb') as handle:
        return pickle.load(handle)

#read CSV
def readListCSV (filename):
    with open(filename, 'r') as f:
        f1 = csv.reader(f,delimiter = '|')
        list = [line for i,line in enumerate(f1)]

#removes credits (which were determined to be static shots by the algorithm)
def pullBlack (vFile, staticFile,borderlength):
    staticFile = dict(sorted(staticFile.items()))
    startingList = sorted(list(staticFile))

    cap = cv2.VideoCapture(vFile)

    firstFrame = startingList[0]
    for i in range(firstFrame):
        cap.read()

    # open the file
    for i in range(len(startingList)):
        if len(startingList) == 0:
            break
        firstFrame = startingList[i]
        lastFrame = staticFile[startingList[i]]

        for j in range(lastFrame-firstFrame):
            ret, frame = cap.read()
            if j == 4:
                if float((frame[:,0:borderlength,0] < 5).sum()/frame[:,0:borderlength,0].size) > 0.9:
                    staticFile.pop(firstFrame)
            if ret:
                pass
            else:
                cap.release()

        if cv2.waitKey(0) & 0xFF == ord('q'):
            exit()
        if i == len(startingList)-1:
            break
        else:
            skipFrames = startingList[i+1]-lastFrame
            for k in range(skipFrames):
                cap.read()
    return staticFile