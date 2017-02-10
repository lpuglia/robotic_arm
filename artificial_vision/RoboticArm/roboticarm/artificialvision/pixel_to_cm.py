### DA INTEGRARE ###
# Conversione da pixels in cm

import cv2
import numpy as np
import pickle
from time import sleep

def load_obj (name):
    with open(name + '.pkl', 'rb') as f:
        return pickle.load(f)


def pxTOcm (toConv, ratioIndex):
    return (1/ratioIndex)*toConv

pi = np.pi

# TEST COLORE - BGR -> HSV
cap = cv2.VideoCapture(0)
sleep(2)
mtx = load_obj("mtx")
dist = load_obj("dist")
newcameramtx = load_obj("newcameramtx")
roi = load_obj("roi")

# VERDE [cartoncino]

#lower_green = np.array([30,128,0], dtype=np.uint8)
#upper_green = np.array([90,255,255], dtype=np.uint8)
    
# ARANCIONE [cartoncino]
    
lower_yellow = np.array([5,192,0], dtype=np.uint8)
upper_yellow = np.array([30,255,255], dtype=np.uint8)

myHeight = 6.5
myWidth = 4.5

for jjj in range(1,3):
    #centerGreen = np.array([-1,-1]);
    centerYellow = np.array([-1,-1]);
    # Take each frame
    _, frame = cap.read()
    
    ##### Calibrazione
    h,  w = frame.shape[:2]
    
    #cv2.imshow('Pre-calib',frame)
    #cv2.waitKey(1)

    ##### Method 2: Remapping
    # undistort
    mapx,mapy = cv2.initUndistortRectifyMap(mtx,dist,None,newcameramtx,(w,h),5)
    dst = cv2.remap(frame,mapx,mapy,cv2.INTER_LINEAR)
    
    # crop the image
    x,y,w,h = roi
    dst = dst[y:y+h, x:x+w]

    frame = dst
    ##### FINE CALIBRAZIONE
    
    # Convert BGR to HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    """
    Come settare i colori in HSV:
    http://colorizer.org/
    Valori consigliati:
        x = x/2 (IMPORTANTE!)
        y = 100
        z = 255
    """

    # Threshold the HSV image to get only green and yellow colors
    yellowMask = cv2.inRange(hsv, lower_yellow, upper_yellow)
    
    # Bitwise-AND mask and original image
    res2 = cv2.bitwise_and(frame,frame, mask= yellowMask)

    #Get rid of background noise using erosion and fill in the holes using dilation and erode the final image on last time
    element = cv2.getStructuringElement(cv2.MORPH_RECT,(3,3)) # ex:(3,3)
    
    #idem per Arancione
    yellowMask = cv2.erode(yellowMask,element, iterations=2) # ex:2
    yellowMask = cv2.dilate(yellowMask,element,iterations=2) # ex:2
    yellowMask = cv2.erode(yellowMask,element)
    
    #Create Contours for all YELLOW objects
    _, contours, hierarchy = cv2.findContours(yellowMask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    maximumArea = 0
    bestContour = None
    for contour in contours:
        currentArea = cv2.contourArea(contour)
        if currentArea > maximumArea:
            bestContour = contour
            maximumArea = currentArea
    #Create a bounding box around the biggest yellow object
    if bestContour is not None:
        x,y,w,h = cv2.boundingRect(bestContour)
        cv2.rectangle(frame, (x,y),(x+w,y+h), (0,100,255), 1)
        centerYellow = np.array([int(x+w/2),int(y+h/2)]);
        cv2.circle(frame,(int(centerYellow[0]),int(centerYellow[1])), 5, (255,0,0), -1)

    print("larghezza (px): ", str(w))
    print("Altezza (px): "+ str(h))

    # index to convert from px to cm
    convIndex1 = w/myWidth
    convIndex2 = h/myHeight

    print("larghezza (INDICE): "+ str(convIndex1))
    print("Altezza (INDICE): "+ str(convIndex2))

    #Show the original camera feed with a bounding box overlayed 
    cv2.imshow('frame',frame)

    #Use this command to prevent freezes in the feed
    k = cv2.waitKey(5) & 0xFF
    #If escape is pressed close all windows
    if k == 27:
        break

    #from time import sleep
    #sleep(0.5) # Time in seconds

cv2.destroyAllWindows()