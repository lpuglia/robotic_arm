import cv2
import numpy as np
import support as s
import socket

'''
def save_obj (obj, name):
    with open(name + '.pkl', 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)

def load_obj (name):
    with open(name + '.pkl', 'rb') as f:
        return pickle.load(f)
    
def pxTOcm (toConv, ratioIndex):
    return (1/ratioIndex)*toConv
'''

# TEST COLORE - BGR -> HSV
cap = cv2.VideoCapture(0)



'''
mtx = load_obj("mtx")
dist = load_obj("dist")
newcameramtx = load_obj("newcameramtx")
roi = load_obj("roi")
convIndex = load_obj("convIndex")
'''

mtx, dist, newcameramtx, roi = s.calibParam()
convIndex = s.getConvIndex()
# TO Delete
#convIndex = 5.6

print("Posiziona la base del robot sopra al puntino rosso")

## Ciclo per posizionare il robot sempre nella stessa posizione
## Sistemare la base del robot del punto dell'origine del robot

while(1):
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
    #h,w = frame.shape[:2]
    cv2.circle(frame,(int(w/2),int(h*1/2)),5,(0,0,255),-1)
    
    cv2.imshow('Posizionamento robot',frame)
        
    k = cv2.waitKey(5) & 0xFF
    #If escape is pressed close all windows
    if k == 27:
        cv2.destroyAllWindows()
        break

origin= np.array([int(w/2),int(h*1/2)])
#print(origin[0], origin[1])
# VERDE [cartoncino]

lower_green = np.array([30,128,0], dtype=np.uint8)
upper_green = np.array([90,255,255], dtype=np.uint8)
    
# ARANCIONE [cartoncino]
    
lower_orange = np.array([5,192,0], dtype=np.uint8)
upper_orange = np.array([30,255,255], dtype=np.uint8)

# ROSSO [marker]
    
lower_red = np.array([105,128,63], dtype=np.uint8)
upper_red = np.array([125,255,255], dtype=np.uint8)


coordinates = [0, 0, 0, 0, 0]
index_coord = 0

while(1):
    centerGreen = np.array([-1,-1]);
    centerOrange = np.array([-1,-1]);
    centerRed = np.array([-1,-1]);
    # Take each frame
    _, frame = cap.read()
    
    ##### Calibrazione
    h,  w = frame.shape[:2]
    cv2.imshow('Pre-calib',frame)
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

    # Threshold the HSV image to get only green and Orange colors
    greenMask = cv2.inRange(hsv, lower_green, upper_green)
    orangeMask = cv2.inRange(hsv, lower_orange, upper_orange)
    redMask = cv2.inRange(hsv, lower_red, upper_red)
    # Bitwise-AND mask and original image
    res = cv2.bitwise_and(frame,frame, mask= greenMask)
    res2 = cv2.bitwise_and(frame,frame, mask= orangeMask)
    res3 = cv2.bitwise_and(frame,frame, mask= redMask)
    #Get rid of background noise using erosion and fill in the holes using dilation and erode the final image on last time
    element = cv2.getStructuringElement(cv2.MORPH_RECT,(3,3)) # ex:(3,3)
    greenMask = cv2.erode(greenMask,element, iterations=2) # ex:2
    greenMask = cv2.dilate(greenMask,element,iterations=2) # ex:2
    greenMask = cv2.erode(greenMask,element)
    
    #idem per Arancione
    orangeMask = cv2.erode(orangeMask,element, iterations=2) # ex:2
    orangeMask = cv2.dilate(orangeMask,element,iterations=2) # ex:2
    orangeMask = cv2.erode(orangeMask,element)
    
    #idem per Rosso
    redMask = cv2.erode(redMask,element, iterations=2) # ex:2
    redMask = cv2.dilate(redMask,element,iterations=2) # ex:2
    redMask = cv2.erode(redMask,element)

    #Create Contours for all GREEN objects
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
        cv2.rectangle(frame, (x,y),(x+w,y+h), (0,255,0), 1)
        centerGreen = np.array([int(x+w/2),int(y+h/2)]);
        cv2.circle(frame,(int(centerGreen[0]),int(centerGreen[1])), 5, (255,0,0), -1)
    #Show the original camera feed with a bounding box overlayed 
    #cv2.imshow('frame',frame)
    #Show the contours in a seperate window
    #cv2.imshow('mask',greenMask)
    
    #Create Contours for all orange objects
    _, contours, hierarchy = cv2.findContours(orangeMask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    maximumArea = 0
    bestContour = None
    for contour in contours:
        currentArea = cv2.contourArea(contour)
        if currentArea > maximumArea:
            bestContour = contour
            maximumArea = currentArea
    #Create a bounding box around the biggest orange object
    if bestContour is not None:
        x,y,w,h = cv2.boundingRect(bestContour)
        cv2.rectangle(frame, (x,y),(x+w,y+h), (0,100,255), 1)
        centerOrange = np.array([int(x+w/2),int(y+h/2)]);
        cv2.circle(frame,(int(centerOrange[0]),int(centerOrange[1])), 5, (255,0,0), -1)
        #print(centerOrange[:])
        if centerGreen[0] > 0 and centerOrange[1] > 0:
            cv2.line(frame,(centerGreen[0],centerGreen[1]),(centerOrange[0],centerOrange[1]),(255,0,0),2)
    
    #Create Contours for all red objects
    _, contours, hierarchy = cv2.findContours(redMask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    maximumArea = 0
    bestContour = None
    for contour in contours:
        currentArea = cv2.contourArea(contour)
        if currentArea > maximumArea:
            bestContour = contour
            maximumArea = currentArea
    #Create a bounding box around the biggest red object
    if bestContour is not None:
        x,y,w,h = cv2.boundingRect(bestContour)
        #cv2.rectangle(frame, (x,y),(x+w,y+h), (0,100,255), 1)
        centerRed = np.array([int(x+w/2),int(y+h/2)]);
        #cv2.circle(frame,(int(centerRed[0]),int(centerRed[1])), 10, (255,255,255), -1)
        #print(centerRed[:])
        '''
        if centerRed[1] > 0:
            cv2.circle(frame,(int(centerRed[0]),int(centerRed[1])), 15, (0,255,255), 3)
            cv2.circle(frame,(int(centerRed[0]),int(centerRed[1])), 3, (255,255,255), -1)
        '''   


    # Posizione del gancio del ragno
    g_x = (centerGreen[0] + centerOrange[0])/2
    g_y = (centerGreen[1] + centerOrange[1])/2
    goal = np.array([g_x, g_y])

    #cv2.rectangle(frame, (int(origin[0]),int(origin[1])),(int(g_x), int(g_y)), (255,255,0), 1)

    if centerGreen[0] > 0 and centerOrange[1] > 0:
        cv2.arrowedLine(frame, (int(origin[0]),int(origin[1])),(int(g_x), int(g_y)), (0,0,255), 3, 4, 0, 0.1)
    ### INVIARE COORDINATE:
    ### X: g_x - origin[0]
    ### Y: origin[1] - g_y
    X = g_x - origin[0]
    Y = origin[1] - g_y

    # OK
    X = s.pxTOcm(X, convIndex)
    Y = s.pxTOcm(Y, convIndex)
    
    # Ultime 5 coordinate 
    cc = [X*10, Y*10]
    coordinates[index_coord % 5] = cc
    index_coord+=1
    #print(coordinates)
    
    # coordinate su ascisse e ordinata rispetto al punto di origine del braccio robotico
    # from cm to mm
    print("x = "+str(X)+"mm", "y = "+str(Y)+"mm")

    #angle = math.atan2(centerGreen[1]-centerOrange[1], centerGreen[0]-centerOrange[0])
    #print(angle)
    #gradi = angle *180/pi
    #print(-gradi)
    
    cv2.circle(frame,(int(origin[0]),int(origin[1])),5,(255,255,255),-1)
    #Show the original camera feed with a bounding box overlayed 
    cv2.imshow('frame',frame)

    #Use this command to prevent freezes in the feed
    k = cv2.waitKey(5) & 0xFF
    #If escape is pressed close all windows
    if k == 27:
        break
    
    s.sleep(0.5)

cv2.destroyAllWindows()

print("Invio coordinate")
#print(coordinates)
toSend = np.median(coordinates, axis= 0)
x = toSend[1]
y = -toSend[0]
print(np.median(coordinates, axis= 0))
print(x, y)

##### Send data with UDP

#IP = "172.16.69.174"

soc = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

#print('flag2')
soc.connect(("172.16.69.174", 8089))

#print('flag3')
#clients_input = input("What you want to proceed my dear client?\n")
clients_input = str(x) + "," + str(y) + "\n"
nbyte = soc.send(clients_input.encode("utf8")) # we must encode the string to bytes

#print(nbyte)

soc.shutdown(socket.SHUT_RDWR)
soc.close()