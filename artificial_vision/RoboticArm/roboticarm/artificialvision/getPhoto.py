import cv2
import numpy as np

cap = cv2.VideoCapture(0)

_, frame = cap.read()


cv2.imshow('frame',frame)
cv2.waitKey(50)
cv2.imwrite("orange_1"  + ".png", frame)