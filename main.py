import cv2
from cvzone.HandTrackingModule import HandDetector

cap = cv2.VideoCapture(0)
cap.set(3,1280)
cap.set(4,720)

detector = HandDetector(detectionCon=0.8,maxHands=1)

class Button:
    def __init__(self,pos,width,height,value):
        self.pos = pos
        self.width = width
        self.height = height
        self.value = value

    def draw(self,img):
        x,y = self.pos
        cv2.rectangle(img,(x,y),(x+self.width,y+self.height),(50,50,50),cv2.FILLED)
        cv2.rectangle(img,(x,y),(x+self.width,y+self.height),(255,255,255),2)
        cv2.putText(img,self.value,(x+30,y+70),
                    cv2.FONT_HERSHEY_PLAIN,2,(255,255,255),2)

buttonValues = [['7','8','9','/'],
                ['4','5','6','*'],
                ['1','2','3','-'],
                ['0','.','=','+']]

buttonList=[]

for x in range(4):
    for y in range(4):
        xpos=x*100+450
        ypos=y*100+200
        buttonList.append(Button((xpos,ypos),100,100,buttonValues[y][x]))

equation=""
delay=0

while True:

    success,img=cap.read()
    img=cv2.flip(img,1)

    hands,img=detector.findHands(img)

    # Transparent panel
    overlay=img.copy()
    cv2.rectangle(overlay,(430,150),(870,600),(0,0,0),-1)
    img=cv2.addWeighted(overlay,0.3,img,0.7,0)

    # display box
    cv2.rectangle(img,(450,120),(850,180),(255,255,255),cv2.FILLED)

    for button in buttonList:
        button.draw(img)

    if hands:

        lmList=hands[0]['lmList']

        length,_,img=detector.findDistance(lmList[8][0:2],lmList[12][0:2],img)

        x,y=lmList[8][0:2]

        for i,button in enumerate(buttonList):

            bx,by=button.pos

            if bx<x<bx+button.width and by<y<by+button.height:

                cv2.rectangle(img,button.pos,
                              (bx+button.width,by+button.height),
                              (0,255,0),cv2.FILLED)

                cv2.putText(img,button.value,
                            (bx+25,by+80),
                            cv2.FONT_HERSHEY_PLAIN,4,(255,255,255),4)

                if length<40 and delay==0:

                    value=buttonValues[int(i%4)][int(i/4)]

                    if value=="=":
                        try:
                            equation=str(eval(equation))
                        except:
                            equation="Error"
                    else:
                        equation+=value

                    delay=1

    if delay!=0:
        delay+=1
        if delay>10:
            delay=0

    cv2.putText(img,equation,(460,170),
                cv2.FONT_HERSHEY_PLAIN,3,(0,0,0),3)

    cv2.imshow("AI Virtual Calculator",img)

    key=cv2.waitKey(1)

    if key==ord('c'):
        equation=""

    if key==27:
        break

cap.release()
cv2.destroyAllWindows()