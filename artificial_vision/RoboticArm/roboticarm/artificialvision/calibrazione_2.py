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

#---------------------------------------------------------------

### Calcolare prima 'objpoints'e 'imgpoints' con lo script "calibrazione"

cap = cv2.VideoCapture(0)

numPickle = 50

objpoints = load_obj("objpoints"+str(numPickle))
imgpoints = load_obj("imgpoints"+str(numPickle))

print(objpoints.__sizeof__())
print(imgpoints.__sizeof__())

print('VIA')
#sleep(2)

_, images = cap.read()

sleep(2)

gray = cv2.cvtColor(images,cv2.COLOR_BGR2GRAY)

print("- Camera calibration")
ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, gray.shape[::-1],None,None)


_, images = cap.read()

###
cv2.imshow('Pre-calib',images)
cv2.imwrite('before_calib.png',images)
cv2.waitKey(1)
###

#img = cv2.imread('left12.jpg')
h,  w = images.shape[:2]

print("- getOptimalNewCameraMatrix")

newcameramtx, roi=cv2.getOptimalNewCameraMatrix(mtx,dist,(w,h),1,(w,h))



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
print("- remapping")
# undistort
mapx,mapy = cv2.initUndistortRectifyMap(mtx,dist,None,newcameramtx,(w,h),5)
dst = cv2.remap(images,mapx,mapy,cv2.INTER_LINEAR)

# crop the image
x,y,w,h = roi
dst = dst[y:y+h, x:x+w]

###
cv2.imshow('calibresult',dst)
cv2.imwrite('calibresult.png',dst)
cv2.waitKey(1)
###

# Calcolo errore
'''
print("- error calculation")
mean_error = 0
tot_error = 0
print(imgpoints.__len__())
for i in range(imgpoints.__len__()):
    imgpoints2, _ = cv2.projectPoints(objpoints[i], rvecs[i], tvecs[i], mtx, dist)
    error = cv2.norm(imgpoints[i],imgpoints2, cv2.NORM_L2)/len(imgpoints2)
    print(error)
    tot_error = error + tot_error

print("total error: ", mean_error/len(objpoints))
'''