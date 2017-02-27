import cv2
import numpy as np
import support as s

cap = cv2.VideoCapture(0)
s.sleep(3)

mtx, dist, newcameramtx, roi = s.calibParam()

# ARANCIONE [cartoncino]
    
lower_yellow = np.array([5,192,0], dtype=np.uint8)
upper_yellow = np.array([30,255,255], dtype=np.uint8)

myHeight = 9.7 #6.5
myWidth = 9.9 #4.5

while(1):
    centerYellow = np.array([-1,-1]);
    # Take each frame
    _, frame = cap.read()
    
    ##### Calibrazione
    h0,  w0 = frame.shape[:2]
    ##### Method 2: Remapping
    # undistort
    mapx,mapy = cv2.initUndistortRectifyMap(mtx,dist,None,newcameramtx,(w0,h0),5)
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

    #cv2.rectangle(frame, (int(w0/2-20), int(h0/2-20)),(int(w0/2+20), int(h0/2+20)), (255,0,0), 1)
    cv2.rectangle(frame, (int(w0/2-w/2), int(h0/2-h/2)),(int(w0/2+w/2), int(h0/2+h/2)), (255,0,0), 1)

    #Show the original camera feed with a bounding box overlayed 
    cv2.imshow('frame',frame)

    #Use this command to prevent freezes in the feed
    k = cv2.waitKey(5) & 0xFF
    '''
    #If escape is pressed close all windows
    if k == 27:
        break
    '''
    s.sleep(0.2) # Time in seconds
    
    if(abs(convIndex1 - convIndex2) < 0.2):
        break
cv2.destroyAllWindows()

print("Indice di conversione:" + str(convIndex1))
s.save_obj(convIndex1, "convIndex")