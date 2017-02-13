# Script veloce per testare la videocamera
import cv2
import support as s

cap = cv2.VideoCapture(0)
'''
mtx = load_obj("mtx")
dist = load_obj("dist")
newcameramtx = load_obj("newcameramtx")
roi = load_obj("roi")
'''

mtx, dist, newcameramtx, roi = s.calibParam()

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
    
    k = cv2.waitKey(5) & 0xFF

    if k == 27:
        break

cv2.destroyAllWindows()