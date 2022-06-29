import cv2 as cv
import mediapipe as mp
import time
import HandTrackingModule as htm


pTime = 0
cTime = 0
cap = cv.VideoCapture(0)
detector = htm.handDectector()
while True:
    success, img = cap.read()
    img = detector.findHands(img)
    lmLIst = detector.findPosition(img)
    if len(lmLIst) != 0:
            print(lmLIst[4])

    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime

    cv.putText(img, str(int(fps)), (10, 70),
                   cv.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)

    
    cv.imshow('image', img)
    cv.waitKey(1)
