import cv2
import numpy as np

# TEST COLORE - BGR -> HSV
cap = cv2.VideoCapture(0)

#START
#centerGreen = np.array([-1,-1]);
#centerYellow = np.array([-1,-1]);

while(1):
    centerGreen = np.array([-1,-1]);
    centerYellow = np.array([-1,-1]);
    # Take each frame
    _, frame = cap.read()

    # Convert BGR to HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # define range of blue color in HSV
    #lower_blue = np.array([110,50,50])
    #upper_blue = np.array([130,255,255])
    

    """
    Come settare i colori in HSV:
    http://colorizer.org/
    Valori consigliati:
        x = x/2 (IMPORTANTE!)
        y = 100
        z = 255
    """
    
    lower_green = np.array([50,100,100], dtype=np.uint8)
    upper_green = np.array([75,255,255], dtype=np.uint8)

    lower_yellow = np.array([25,100,100], dtype=np.uint8)
    upper_yellow = np.array([40,255,255], dtype=np.uint8)
    
    # Threshold the HSV image to get only blue colors
    #mask = cv2.inRange(hsv, lower_blue, upper_blue)
    greenMask = cv2.inRange(hsv, lower_green, upper_green)
    yellowMask = cv2.inRange(hsv, lower_yellow, upper_yellow)
    
    # Bitwise-AND mask and original image
    res = cv2.bitwise_and(frame,frame, mask= greenMask)
    res2 = cv2.bitwise_and(frame,frame, mask= yellowMask)

    #Get rid of background noise using erosion and fill in the holes using dilation and erode the final image on last time
    element = cv2.getStructuringElement(cv2.MORPH_RECT,(3,3)) # ex:(3,3)
    greenMask = cv2.erode(greenMask,element, iterations=2) # ex:2
    greenMask = cv2.dilate(greenMask,element,iterations=2) # ex:2
    greenMask = cv2.erode(greenMask,element)
    
    #idem per Giallo
    yellowMask = cv2.erode(yellowMask,element, iterations=2) # ex:2
    yellowMask = cv2.dilate(yellowMask,element,iterations=2) # ex:2
    yellowMask = cv2.erode(yellowMask,element)
    
    #cv2.imshow('frame',frame)
    #cv2.imshow('mask',greenMask)
    #cv2.imshow('res',res+res2)    
    #cv2.imshow('res',res)
    
    #Create Contours for all blue objects
    _, contours, hierarchy = cv2.findContours(greenMask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    maximumArea = 0
    bestContour = None
    for contour in contours:
        currentArea = cv2.contourArea(contour)
        if currentArea > maximumArea:
            bestContour = contour
            maximumArea = currentArea
    #Create a bounding box around the biggest blue object
    if bestContour is not None:
        x,y,w,h = cv2.boundingRect(bestContour)
        cv2.rectangle(frame, (x,y),(x+w,y+h), (0,0,255), 3)
        centerGreen = np.array([int(x+w/2),int(y+h/2)]);
        cv2.circle(frame,(int(centerGreen[0]),int(centerGreen[1])), 5, (255,0,0), -1)
    #Show the original camera feed with a bounding box overlayed 
    #cv2.imshow('frame',frame)
    #Show the contours in a seperate window
    #cv2.imshow('mask',greenMask)
    
    ###########
    ###########
    
    #Create Contours for all blue objects
    _, contours, hierarchy = cv2.findContours(yellowMask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    maximumArea = 0
    bestContour = None
    for contour in contours:
        currentArea = cv2.contourArea(contour)
        if currentArea > maximumArea:
            bestContour = contour
            maximumArea = currentArea
    #Create a bounding box around the biggest blue object
    if bestContour is not None:
        x,y,w,h = cv2.boundingRect(bestContour)
        cv2.rectangle(frame, (x,y),(x+w,y+h), (255,0,255), 3)
        centerYellow = np.array([int(x+w/2),int(y+h/2)]);
        cv2.circle(frame,(int(centerYellow[0]),int(centerYellow[1])), 5, (255,0,0), -1)
        print(centerGreen[:])
        if centerGreen[0] > 0 and centerYellow[1] > 0:
            cv2.line(frame,(centerGreen[0],centerGreen[1]),(centerYellow[0],centerYellow[1]),(255,0,0),2)

    #Segmento tra i 2 centri


    #Show the original camera feed with a bounding box overlayed 
    cv2.imshow('frame',frame)
    #Show the contours in a seperate window
    cv2.imshow('mask',greenMask)
    cv2.imshow('mask',yellowMask)
    
    #Use this command to prevent freezes in the feed
    k = cv2.waitKey(5) & 0xFF
    #If escape is pressed close all windows
    if k == 27:
        break


cv2.destroyAllWindows()