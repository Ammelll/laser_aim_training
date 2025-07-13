import cv2
import numpy as np
import imutils
import keyboard  # pip install keyboard
import win32api
from interception import move_t
cap = cv2.VideoCapture(0);
x=500
y=500
while(True):
    screenWidth = win32api.GetSystemMetrics(0)
    screenHeight = win32api.GetSystemMetrics(1)
    move_to(x,y)
    if keyboard.is_pressed('esc'):
        break

    ret, frame = cap.read()
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    lowerBound =  [172, 51, 0]
    upperBound = [179, 255, 255]
    lower = np.array(lowerBound, dtype = "uint8")
    upper = np.array(upperBound, dtype = "uint8")
    mask = cv2.inRange(hsv,lower,upper)
    output = cv2.bitwise_and(hsv,frame,mask=mask)
    # kernel = np.ones((5,5),np.uint8)
    # output = cv2.morphologyEx(output, cv2.MORPH_OPEN, kernel)
    gray = cv2.cvtColor(output, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    thresh = cv2.threshold(blurred, 60, 255, cv2.THRESH_BINARY)[1]  
    cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
	cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)

    biggest_contour = []
    for c in cnts:
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
        x = screenWidth * (cX/640)  
        y = screenHeight * (cY/400)
        cv2.drawContours(output, [biggest_contour], -1, (0, 255, 0), 2)
        cv2.circle(output, (cX, cY), 7, (255, 255, 255), -1)
        cv2.putText(output, "center", (cX - 20, cY - 20),
            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
    cv2.imshow('frame',output)
    if cv2.waitKey(1) == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()
