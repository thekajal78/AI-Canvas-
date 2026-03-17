import cv2
import pyautogui
from cvzone.HandTrackingModule import HandDetector

# Webcam
cap = cv2.VideoCapture(0)
cap.set(3,1280)
cap.set(4,720)

detector = HandDetector(detectionCon=0.8,maxHands=1)

screen_w,screen_h = pyautogui.size()

mode="mouse"
equation=""

# Calculator buttons
buttons = [
["7","8","9","/"],
["4","5","6","*"],
["1","2","3","-"],
["0",".","=","+"]
]

button_pos=[]

for i in range(4):
    for j in range(4):
        button_pos.append((900+j*80,200+i*80,buttons[i][j]))

while True:

    success,img=cap.read()
    img=cv2.flip(img,1)

    hands,img=detector.findHands(img)

    if hands:

        hand=hands[0]
        lmList=hand["lmList"]
        fingers=detector.fingersUp(hand)

        x,y=lmList[8][0:2]

        # Mode switching
        if fingers[1]==1 and sum(fingers)==1:
            mode="mouse"

        if sum(fingers)==5:
            mode="calculator"

        # ---------- MOUSE MODE ----------
        if mode=="mouse":

            cv2.putText(img,"Mouse Mode",(50,80),
                        cv2.FONT_HERSHEY_SIMPLEX,1,(0,255,0),3)

            screen_x=int(x*screen_w/1280)
            screen_y=int(y*screen_h/720)

            pyautogui.moveTo(screen_x,screen_y)

            length,_,img=detector.findDistance(
                lmList[8][0:2],lmList[12][0:2],img)

            if length<30:
                pyautogui.click()

        # ---------- CALCULATOR MODE ----------
        if mode=="calculator":

            cv2.putText(img,"Calculator Mode",(50,80),
                        cv2.FONT_HERSHEY_SIMPLEX,1,(255,0,0),3)

            # draw buttons
            for (bx,by,val) in button_pos:

                cv2.rectangle(img,(bx,by),(bx+70,by+70),
                              (200,200,200),cv2.FILLED)

                cv2.rectangle(img,(bx,by),(bx+70,by+70),
                              (50,50,50),2)

                cv2.putText(img,val,(bx+20,by+45),
                            cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,0),2)

                if bx<x<bx+70 and by<y<by+70:

                    cv2.rectangle(img,(bx,by),(bx+70,by+70),
                                  (0,255,0),cv2.FILLED)

                    cv2.putText(img,val,(bx+20,by+45),
                                cv2.FONT_HERSHEY_SIMPLEX,1,(255,255,255),2)

                    length,_,img=detector.findDistance(
                        lmList[8][0:2],lmList[12][0:2],img)

                    if length<30:

                        if val=="=":
                            try:
                                equation=str(eval(equation))
                            except:
                                equation="Error"

                        else:
                            equation+=val

            # display equation
            cv2.rectangle(img,(900,120),(1200,170),(255,255,255),cv2.FILLED)

            cv2.putText(img,equation,(910,160),
                        cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,0),2)

    cv2.imshow("Gesture Control System",img)

    if cv2.waitKey(1)==27:
        break

cap.release()
cv2.destroyAllWindows()