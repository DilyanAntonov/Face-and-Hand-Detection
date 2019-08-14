"""
This program detects Face and Hand. For the face I used HaardCascade. It's simple and works pretty well.
For the hand the HaardCascade method is not very reliable. That's why I used a different method.
When you run the code you will see a square on the right of your window. Your hand is only detected in it.
The way it works is the following: when there are no objects in the square you hit the SPACE key and the code
will take a picture of the square. When something new appears in it (that when wasn't there before when
taking the background picture) it will be processed by several filters to get a clean outline of it.
Those filters can be seen on the additional windows that will open upon running the code. This means that
it will capture objects other than your hand. Also a change in the background will be seen as a new object,
therefore it will be shown as one. If your background changes you can easily remove your hand and hit the
SPACE key again to capture a new background. You exit the program by hitting the ESCAPE key.
"""

# pip install opencv-python

import cv2
import numpy as np
import copy


# Parameters used in the detection later
threshold = 20
bgSubThreshold = 50
blurValue = 11

isBgCaptured = 0
triggerSwitch = False

face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

def removeBG(frame):
    fgmask = bgModel.apply(frame, learningRate=0)
    kernel = np.ones((3, 3), np.uint8)
    mask = cv2.erode(fgmask, kernel, iterations=1)
    res = cv2.bitwise_and(frame, frame, mask=mask)
    return res


# Camera capture
capture = cv2.VideoCapture(0)
capture.set(10, 200)

while capture.isOpened():
    ret, frame = capture.read()
    frame = cv2.bilateralFilter(frame, 5, 50, 100)
    frame = cv2.flip(frame, 1)  # Flips the frame so it is not mirrored
    cv2.rectangle(frame, (int(0.6 * frame.shape[1]), 0), # Drawing the rectangle
                  (frame.shape[1], int(0.6 * frame.shape[0])), (255, 0, 0), 2)

    # Capturing the face
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    for x, y, w, h in faces:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 3)

    cv2.imshow('Hand and Face Detection', frame)

    #  Main operation
    if isBgCaptured == 1:
        img = removeBG(frame)
        img = img[0:int(0.6 * frame.shape[0]),
              int(0.6 * frame.shape[1]):frame.shape[1]]
        cv2.imshow('Mask', img)

        # Some filters making the image easier to process
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray, (blurValue, blurValue), 0)
        cv2.imshow('Blur', blur)
        ret, thresh = cv2.threshold(blur, threshold, 255, cv2.THRESH_BINARY)
        cv2.imshow('Thresh', thresh)

        # Making the contours
        thresh1 = copy.deepcopy(thresh)
        contours, hierarchy = cv2.findContours(thresh1, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        length = len(contours)
        maxArea = -1
        if length > 0:
            for i in range(length): # Gets the biggest contour
                temp = contours[i]
                area = cv2.contourArea(temp)
                if area > maxArea:
                    maxArea = area
                    ci = i

            res = contours[ci]
            hull = cv2.convexHull(res)
            contour = np.zeros(img.shape, np.uint8)
            cv2.drawContours(contour, [res], 0, (0, 255, 0), 2)
            cv2.drawContours(contour, [hull], 0, (0, 0, 255), 3)

        cv2.imshow('Hand Detection', contour)

    # Keyboard OP
    k = cv2.waitKey(10)
    if k == 27:  # press ESC to exit
        break
    elif k == 32:  # press SPACE to capture the background
        bgModel = cv2.createBackgroundSubtractorMOG2(0, bgSubThreshold)
        isBgCaptured = 1