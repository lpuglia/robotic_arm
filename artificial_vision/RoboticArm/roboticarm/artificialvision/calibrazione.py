import cv2
import numpy as np
import pickle
from time import sleep

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
    _, frame = cap.read()

    gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
 
    ret, corners = cv2.findCirclesGrid(gray, (5,4), None)
    
    if ret == True:
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
'''
objpoints = load_obj("objpoints"+str(numPickle))
imgpoints = load_obj("imgpoints"+str(numPickle))
gray = cv2.imread("img/image_1.png",0)
ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, gray.shape[::-1],None,None)

save_obj(mtx, "mtx")
save_obj(dist, "dist")
save_obj(rvecs, "rvecs")
save_obj(tvecs, "tvecs")
'''
############################ CAMERA CALIBRATION - UNDISTORTION
'''
cap = cv2.VideoCapture(0)

sleep(3)

mtx = load_obj("mtx")
dist = load_obj("dist")
rvecs = load_obj("rvecs")
tvecs = load_obj("tvecs")

_, images = cap.read()

h,  w = images.shape[:2]

newcameramtx, roi=cv2.getOptimalNewCameraMatrix(mtx,dist,(w,h),1,(w,h))

save_obj(newcameramtx, "newcameramtx")
save_obj(roi, "roi")
'''
############################ CAMERA CALIBRATION - IMAGE REMAPPING
cap = cv2.VideoCapture(0)

sleep(3)
_, images = cap.read()

mtx = load_obj("mtx")
dist = load_obj("dist")
newcameramtx = load_obj("newcameramtx")
roi = load_obj("roi")

h,  w = images.shape[:2]

cv2.imshow('Pre-calib',images)
cv2.imwrite('Pre_calib.png',images)
cv2.waitKey(1)
'''
##### 1. Using cv2.undistort()
# undistort
dst = cv2.undistort(images, mtx, dist, None, newcameramtx)

# crop the image
x,y,w,h = roi
dst = dst[y:y+h, x:x+w]

cv2.imwrite('calibresult.png',dst)
'''
##### 2. Using remapping
# undistort
mapx,mapy = cv2.initUndistortRectifyMap(mtx,dist,None,newcameramtx,(w,h),5)
dst = cv2.remap(images,mapx,mapy,cv2.INTER_LINEAR)

# crop the image
x,y,w,h = roi
dst = dst[y:y+h, x:x+w]

cv2.imshow('Post-calib',dst)
cv2.imwrite('Post-calib.png',dst)
cv2.waitKey(1)