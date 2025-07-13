import cv2
import numpy as np
import imutils
import keyboard
from screeninfo import get_monitors
from interception import move_to

cap = cv2.VideoCapture(0);
#values frmo HSV_calibration.py
HSV_MIN = [172,51,0]
HSV_MAX = [179, 255, 255]

CAMERA_WIDTH = 640
CAMERA_HEIGHT = 400
while(True):
    if keyboard.is_pressed('esc'):
        break
    
    monitor = get_monitors()[0]
    screenWidth = monitor.width
    screenHeight =  monitor.height

    ret, frame = cap.read()
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    lowerBound =  HSV_MIN
    upperBound = HSV_MAX
    lower = np.array(lowerBound, dtype = "uint8")
    upper = np.array(upperBound, dtype = "uint8")
    mask = cv2.inRange(hsv,lower,upper)
    output = cv2.bitwise_and(hsv,frame,mask=mask)
    # Optional filtering (experimentalnot reccomended)
    # kernel = np.ones((5,5),np.uint8)
    # output = cv2.morphologyEx(output, cv2.MORPH_OPEN, kernel)
    gray = cv2.cvtColor(output, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    thresh = cv2.threshold(blurred, 60, 255, cv2.THRESH_BINARY)[1]  
    cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
	cv2.CHAIN_APPROX_SIMPLE)
    contours = imutils.grab_contours(cnts)

    biggest_contour = []
    for c in contours:
        biggest_contour_area = 0
        if cv2.contourArea(c) > biggest_contour_area:
            biggest_contour = c
            biggest_contour_area = cv2.contourArea(c)

    if len(biggest_contour) != 0:
        M = cv2.moments(c)
        if M["m00"] == 0:
            continue
        cX = int(M["m10"] / M["m00"])
        cY = int(M["m01"] / M["m00"])
        x = screenWidth - screenWidth * (cX/CAMERA_WIDTH)  
        y = screenHeight * (cY/CAMERA_HEIGHT)
        move_to(x,y)
        cv2.drawContours(output, [biggest_contour], -1, (0, 255, 0), 2)
        cv2.circle(output, (cX, cY), 7, (255, 255, 255), -1)
        cv2.putText(output, "center", (cX - 20, cY - 20),
            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
    cv2.imshow('frame',output)
    if cv2.waitKey(1) == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()
