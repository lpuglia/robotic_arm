import cv2
import numpy as np
#import glob
from time import sleep

# termination criteria
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

# prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
objp = np.zeros((6*7,3), np.float32)
objp[:,:2] = np.mgrid[0:7,0:6].T.reshape(-1,2)

# Arrays to store object points and image points from all the images.
objpoints = [] # 3d point in real world space
imgpoints = [] # 2d points in image plane.

#images = glob.glob('*.jpg')
cap = cv2.VideoCapture(0)

#for fname in images:
    #img = cv2.imread(fname)
    #gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

#for i in range(1, 2):
while(1):
    _, images = cap.read()

    gray = cv2.cvtColor(images,cv2.COLOR_BGR2GRAY)
    
    
    '''
    # DA CANCELLARE SICURO
    thresh = 127
    gray = cv2.threshold(gray, thresh, 255, cv2.THRESH_BINARY)[1]
    '''
    cv2.imshow('pok',gray)
    k = cv2.waitKey(5) & 0xFF
    #If escape is pressed close all windows
    if k == 27:
        break
    # Find the chess board corners
    ret, corners = cv2.findChessboardCorners(gray, (5,5),None)
    print(ret)
    # If found, add object points, image points (after refining them)
    if ret == True:
        objpoints.append(objp)

        cv2.cornerSubPix(gray,corners,(11,11),(-1,-1),criteria) # EX: 6,6
        imgpoints.append(corners)
        cv2.imshow('imgoooo',gray)
        # Draw and display the corners
        #cv2.drawChessboardCorners(img, (7,6), corners,ret) # EX: corners2
        #cv2.imshow('img',img)
        cv2.drawChessboardCorners(images, (5,5), corners,ret) # EX: corners2
        cv2.imshow('img',images)

    sleep(0.2)
    k = cv2.waitKey(5) & 0xFF
    #If escape is pressed close all windows
    if k == 27:
        break
cv2.destroyAllWindows()