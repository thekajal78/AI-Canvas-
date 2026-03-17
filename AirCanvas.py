import cv2
import numpy as np
from cvzone.HandTrackingModule import HandDetector

cap = cv2.VideoCapture(0)
cap.set(3,1280)
cap.set(4,720)

detector = HandDetector(detectionCon=0.8,maxHands=1)

canvas = np.zeros((720,1280,3),np.uint8)

xp,yp = 0,0
color = (255,0,255)
brushThickness = 8
eraserThickness = 40

while True:

    success,img = cap.read()
    img = cv2.flip(img,1)

    # draw toolbar
    cv2.rectangle(img,(0,0),(1280,100),(50,50,50),-1)

    cv2.putText(img,"BLUE",(200,60),cv2.FONT_HERSHEY_SIMPLEX,1,(255,0,0),3)
    cv2.putText(img,"GREEN",(450,60),cv2.FONT_HERSHEY_SIMPLEX,1,(0,255,0),3)
    cv2.putText(img,"RED",(700,60),cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,255),3)
    cv2.putText(img,"ERASE",(950,60),cv2.FONT_HERSHEY_SIMPLEX,1,(255,255,255),3)

    hands,img = detector.findHands(img)

    if hands:

        hand = hands[0]
        lmList = hand["lmList"]
        fingers = detector.fingersUp(hand)

        x1,y1 = lmList[8][0:2]
        x2,y2 = lmList[12][0:2]

        # Selection mode
        if fingers[1] and fingers[2]:

            xp,yp = 0,0

            if y1 < 100:

                if 200 < x1 < 350:
                    color = (255,0,0)

                elif 450 < x1 < 600:
                    color = (0,255,0)

                elif 700 < x1 < 850:
                    color = (0,0,255)

                elif 950 < x1 < 1100:
                    color = (0,0,0)

        # Drawing mode
        if fingers[1] and fingers[2] == False:

            cv2.circle(img,(x1,y1),10,color,cv2.FILLED)

            if xp==0 and yp==0:
                xp,yp = x1,y1

            if color == (0,0,0):
                cv2.line(img,(xp,yp),(x1,y1),color,eraserThickness)
                cv2.line(canvas,(xp,yp),(x1,y1),color,eraserThickness)

            else:
                cv2.line(img,(xp,yp),(x1,y1),color,brushThickness)
                cv2.line(canvas,(xp,yp),(x1,y1),color,brushThickness)

            xp,yp = x1,y1

    imgGray = cv2.cvtColor(canvas,cv2.COLOR_BGR2GRAY)
    _,imgInv = cv2.threshold(imgGray,50,255,cv2.THRESH_BINARY_INV)

    imgInv = cv2.cvtColor(imgInv,cv2.COLOR_GRAY2BGR)

    img = cv2.bitwise_and(img,imgInv)
    img = cv2.bitwise_or(img,canvas)

    cv2.imshow("Air Canvas",img)

    if cv2.waitKey(1)==27:
        break

cap.release()
cv2.destroyAllWindows()