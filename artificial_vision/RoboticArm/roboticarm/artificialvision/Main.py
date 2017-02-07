import cv2
import numpy as np
import pickle

def save_obj (obj, name):
    with open(name + '.pkl', 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)

def load_obj (name):
    with open(name + '.pkl', 'rb') as f:
        return pickle.load(f)

numPickle = 50

numberOfSamples = numPickle
counter = 1

############################ CAMERA CALIBRATION - PARAMETERS
'''
# prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
objp = np.zeros((4*5,3), np.float32)
objp[:,:2] = np.mgrid[0:5,0:4].T.reshape(-1,2)

# Arrays to store object points and image points from all the images.
objpoints = [] # 3d point in real world space
imgpoints = [] # 2d points in image plane.

while(1):
    centerGreen = np.array([-1,-1]);
    centerYellow = np.array([-1,-1]);
    # Take each frame
    _, frame = cap.read()
    
    gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
 
    ret, corners = cv2.findCirclesGrid(gray, (5,4), None)
    
    if ret == True:
        ### to DELETE
        cv2.imwrite("image_"+str(counter)+".png", gray)
        objpoints.append(objp)
        imgpoints.append(corners)
        cv2.drawChessboardCorners(frame, (5,4), corners,ret)
        if counter >= numberOfSamples:
            break
        counter = counter + 1
        print(counter)
        cv2.imwrite("image_" + str(counter) + ".png", gray)
    cv2.imshow('grid', frame)
    cv2.waitKey(1)
cv2.destroyAllWindows()
save_obj(objpoints, "objpoints"+str(numPickle))
save_obj(imgpoints, "imgpoints"+str(numPickle))
'''
############################ CAMERA CALIBRATION - MATRIX CALCULATION

objpoints = load_obj("objpoints"+str(numPickle))
imgpoints = load_obj("imgpoints"+str(numPickle))
gray = cv2.imread("image_1.png")
ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, gray.shape[::-1],None,None)

#cap = cv2.VideoCapture(0)