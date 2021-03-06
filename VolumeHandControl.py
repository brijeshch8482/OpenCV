from sre_constants import SUCCESS
import cv2 as cv
import time
import numpy as np
import HandTrackingModule as htm
import math
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

#####################################
wCam , hCam = 640, 480
#####################################

cap = cv.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)
pTime = 0

detector = htm.handDectector(detectionCon=0.7)



devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))
# volume.GetMute()
# volume.GetMasterVolumeLevel()
volRange = volume.GetVolumeRange()

minVol = volRange[0]
maxVol = volRange[1]
vol = 0
volBar = 400
volPer = 0

while True:
    success, img = cap.read()
    img = detector.findHands(img)
    lmLIst = detector.findPosition(img, draw=False)
    if len(lmLIst) != 0:
        # print(lmLIst[4], lmLIst[8])

        x1, y1 = lmLIst[4][1], lmLIst[4][2]
        x2, y2 = lmLIst[8][1], lmLIst[8][2]
        # center of the line
        cx, cy = (x1 + x2)//2, (y1 + y2)//2

        cv.circle(img, (x1,y1), 15, (255,0,255), cv.FILLED)
        cv.circle(img, (x2,y2), 15, (255,0,255), cv.FILLED)
        # Create line between them
        cv.line(img, (x1,y1), (x2,y2), (255,0,255), 3)
        # put the circle in mid of the line
        cv.circle(img, (cx, cy), 15, (255,0,255), cv.FILLED)

        # Length of the line
        length = math.hypot(x2 - x1, y2 - y1)
        # print(length)

        # Hand rang 30 - 180
        # Volume Range -63.5 - 0

        vol = np.interp(length, [30, 180], [minVol, maxVol])
        volBar = np.interp(length, [30,180], [400, 150])
        volPer = np.interp(length, [30,180], [0, 100])
        print(vol)
        volume.SetMasterVolumeLevel(vol, None)

        
        # if length is less than 50 , change the center of the line color
        if length<50:
            cv.circle(img, (cx, cy), 15, (255,0,0), cv.FILLED)

    cv.rectangle(img, (50, 150), (85, 400), (255,0,0), 3)
    cv.rectangle(img, (50, int(volBar)), (85, 400), (255,0,0), cv.FILLED)
    cv.putText(img, f'{int(volPer)} %', (40, 450), cv.FONT_HERSHEY_COMPLEX, 1, (255,0,0), 3)


    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime

    cv.putText(img, f'FPS: {int(fps)}', (40, 50), cv.FONT_HERSHEY_COMPLEX, 1, (255,0,0), 2)

    cv.imshow('img', img)
    cv.waitKey(1)