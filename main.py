import math
import cv2
import numpy as np
import HandTrackingModule as htm
import time
import autopy
import ctypes
import speech_recognition as sr
import pyttsx3
import subprocess
import pyautogui

detector = htm.handDetector(maxHands=1)
wCam, hCam = 640, 480
frameR = 100
smoothening = 7
pTime = 0
plocX, plocY = 0, 0
clocX, clocY = 0, 0
cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)
threshold = 50
handle = ctypes.windll.user32.GetForegroundWindow()
wScr, hScr = autopy.screen.size()
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)
recognizer = sr.Recognizer()

while True:
    success, img = cap.read()
    img = detector.findHands(img)
    lmList, bbox = detector.findPosition(img)
    if len(lmList) != 0:
        x1, y1 = lmList[8][1:]
        x2, y2 = lmList[12][1:]

        fingers = detector.fingersUp()
        cv2.rectangle(img, (frameR, frameR), (wCam - frameR, hCam - frameR), (255, 0, 255), 2)
        if fingers[1] == 1 and fingers[2] == 0:
            x3 = np.interp(x1, (frameR, wCam-frameR), (0, wScr))
            y3 = np.interp(y1, (frameR, hCam-frameR), (0, hScr))
            clocX = plocX + (x3 - plocX) / smoothening
            clocY = plocY + (x3 - plocY) / smoothening
            autopy.mouse.move(wScr-x3, y3)
            cv2.circle(img, (x1, y1), 15, (255, 0, 255), cv2.FILLED)
            plocX, plocY = clocX, clocY
        if fingers[1] == 1 and fingers[2] == 1:
            length, img, line_Info = detector.findDistance(8, 12, img)
            if length < 70:
                cv2.circle(img, (line_Info[4], line_Info[5]), 15, (0, 255, 0), cv2.FILLED)
                autopy.mouse.click()
        #thumb thingy
        x4, y4 = lmList[4][1], lmList[4][2]
        x5, y5 = lmList[8][1], lmList[8][2]
        cx, cy = (x4 + x5) // 2, (y4 + y5) // 2
        cv2.circle(img, (x4, y4), 15, (255, 0, 255), cv2.FILLED)
        cv2.circle(img, (x5, y5), 15, (255, 0, 255), cv2.FILLED)
        cv2.line(img, (x4, y4), (x5, y5), (255, 0, 255), 3)
        cv2.circle(img, (cx, cy), 15, (255, 0, 255), cv2.FILLED)

        length2 = math.hypot(x5 - x4, y5 - y4)
        #print(length2)
        if length2 < 50:
            time.sleep(1)
            pyautogui.hotkey('win', 'down')
    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime
    cv2.putText(img, str(int(fps)), (20,50), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3)
    cv2.imshow("Image", img)
    cv2.waitKey(1)