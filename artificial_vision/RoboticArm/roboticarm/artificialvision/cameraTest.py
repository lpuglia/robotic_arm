# Script veloce per testare la videocamera

import cv2
import pickle

def load_obj (name):
    with open(name + '.pkl', 'rb') as f:
        return pickle.load(f)

cap = cv2.VideoCapture(0)

mtx = load_obj("mtx")
dist = load_obj("dist")
newcameramtx = load_obj("newcameramtx")
roi = load_obj("roi")

while(1):
    _, frame = cap.read()
    
    ##### Calibrazione
    h,  w = frame.shape[:2]
    
    h2 = int(h/2)
    w2 = int(w/2)
    
    cv2.circle(frame,(w2,h2), 5, (0,255,255), -1)

    ##### Method 2: Remapping
    # undistort
    mapx,mapy = cv2.initUndistortRectifyMap(mtx,dist,None,newcameramtx,(w,h),5)
    dst = cv2.remap(frame,mapx,mapy,cv2.INTER_LINEAR)
    
    # crop the image
    x,y,w,h = roi
    dst = dst[y:y+h, x:x+w]

    frame = dst
    ##### FINE CALIBRAZIONE
    
    cv2.imshow('Post-calib',frame)
    cv2.waitKey(1)