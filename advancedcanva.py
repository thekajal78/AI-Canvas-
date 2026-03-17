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

    # toolbar
    cv2.rectangle(img,(0,0),(1280,100),(40,40,40),-1)

    cv2.putText(img,"BLUE",(150,60),cv2.FONT_HERSHEY_SIMPLEX,1,(255,0,0),3)
    cv2.putText(img,"GREEN",(350,60),cv2.FONT_HERSHEY_SIMPLEX,1,(0,255,0),3)
    cv2.putText(img,"RED",(550,60),cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,255),3)
    cv2.putText(img,"ERASE",(750,60),cv2.FONT_HERSHEY_SIMPLEX,1,(255,255,255),3)
    cv2.putText(img,"SAVE",(950,60),cv2.FONT_HERSHEY_SIMPLEX,1,(255,255,0),3)
    cv2.putText(img,"CLEAR",(1100,60),cv2.FONT_HERSHEY_SIMPLEX,1,(255,255,255),3)

    hands,img = detector.findHands(img)

    if hands:

        hand = hands[0]
        lmList = hand["lmList"]
        fingers = detector.fingersUp(hand)

        x1,y1 = lmList[8][0:2]

        # selection mode
        if fingers[1] and fingers[2]:

            xp,yp = 0,0

            if y1 < 100:

                if 150 < x1 < 300:
                    color = (255,0,0)

                elif 350 < x1 < 500:
                    color = (0,255,0)

                elif 550 < x1 < 700:
                    color = (0,0,255)

                elif 750 < x1 < 900:
                    color = (0,0,0)

                elif 950 < x1 < 1050:
                    cv2.imwrite("drawing.png",canvas)

                elif 1100 < x1 < 1250:
                    canvas = np.zeros((720,1280,3),np.uint8)

        # drawing mode
        if fingers[1] and fingers[2]==False:

            cv2.circle(img,(x1,y1),10,color,cv2.FILLED)

            if xp==0 and yp==0:
                xp,yp = x1,y1

            if color==(0,0,0):
                cv2.line(canvas,(xp,yp),(x1,y1),color,eraserThickness)

            else:
                cv2.line(canvas,(xp,yp),(x1,y1),color,brushThickness)

            xp,yp = x1,y1

        # clear gesture (open hand)
        if fingers == [1,1,1,1,1]:
            canvas = np.zeros((720,1280,3),np.uint8)

    imgGray = cv2.cvtColor(canvas,cv2.COLOR_BGR2GRAY)
    _,imgInv = cv2.threshold(imgGray,50,255,cv2.THRESH_BINARY_INV)

    imgInv = cv2.cvtColor(imgInv,cv2.COLOR_GRAY2BGR)

    img = cv2.bitwise_and(img,imgInv)
    img = cv2.bitwise_or(img,canvas)

    cv2.imshow("AI Air Canvas",img)

    if cv2.waitKey(1)==27:
        break

cap.release()
cv2.destroyAllWindows()