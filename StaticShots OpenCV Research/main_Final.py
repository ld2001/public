#Copyright Luke Ding
#Usage prohibited except by explicit written permission to lukeding3@gmail.com

import cv2
import numpy as np
import csv
import glob
from matplotlib import pyplot as plt
from histogram_frame_detection_Final import *
import glob

drawing = False # true if mouse is pressed
mode = True # if True, draw rectangle. Press 'm' to toggle to curve
ix,iy = -1,-1
fx,fy = -1,-1

# mouse callback function
def draw_square(event,x,y,flags,param):
    global ix,iy,drawing,mode,fx,fy

    if event == cv2.EVENT_LBUTTONDOWN:
        ix,iy = x,y

    elif event == cv2.EVENT_LBUTTONUP:
        fx,fy = x,y
        cv2.rectangle(img,(ix,iy),(x,y),(0,255,0),-1)
        print(ix," ",iy," ",fx," ",fy)

fileList = []
startDict = dict()
endDict = dict()

# Opens every mp4 in root directory and executes algorithm.
# Starts by having user manually crop out letterboxes, and stores the regions of interests in a list
for filenames in glob.glob('*.mp4'):
    cap = cv2.VideoCapture(filenames)
    cv2.namedWindow('image')
    cv2.setMouseCallback('image', draw_square)
    fileList.append(filenames)

    for i in range(600):
        ret, img = cap.read()

    while (1):
        cv2.imshow('image', img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        elif cv2.waitKey(1) & 0xFF == ord('r'):
            for j in range(10):
                ret, img = cap.read()

    startDict[filenames] = (ix,iy)
    endDict[filenames] = (fx,fy)

    cv2.destroyAllWindows()

#With ROIs finalized, begin calculating the frame differences
for filenames in fileList:

    #Find the regions of interest
    startY, startX = startDict[filenames]
    endY, endX = endDict[filenames]
    top,bot,left,right = find_static_shots(str(filenames),startX,startY,endX,endY,8)

    #Calculate whether each edge of the border is static
    threshold = .00015 * (endY - startY) * (endX - startX)
    staticTop = find_static_edge(top,8,threshold,1)
    staticBot = find_static_edge(bot,8,threshold,1)
    staticLeft = find_static_edge(left,8,threshold,1)
    staticRight = find_static_edge(right,8,threshold,1)

    #Calculate the frames that are static
    staticList = find_static_frames(staticTop,staticBot,staticLeft,staticRight,3,20)

    #If the list of static frames is not empty, pull out the credits
    if staticList:
        staticList = pullBlack(str(filenames),staticList,20)

    #Save the list to pickle file and CSV of your choice
    saveList(staticList,str(filenames))
    saveListCSV(staticList,str(filenames),'test06_6_2019.csv',startX, startY, endX, endY,len(staticList))

# All code above is used to determine the static shots. To play the video back, comment out above code and uncomment out code below.
# staticList = readList('Break.mp4.pickle')
# play_video('Break.mp4',staticList)
