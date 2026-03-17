import cv2
import random
import time
from cvzone.HandTrackingModule import HandDetector

cap = cv2.VideoCapture(0)
cap.set(3,1280)
cap.set(4,720)

detector = HandDetector(maxHands=1)

playerScore = 0
computerScore = 0

startGame = False
timer = 0
stateResult = False

while True:

    success, img = cap.read()
    img = cv2.flip(img,1)

    hands, img = detector.findHands(img)

    cv2.putText(img,"Press S to start round",(450,650),
                cv2.FONT_HERSHEY_SIMPLEX,1,(0,255,0),3)

    # SCOREBOARD
    cv2.putText(img,f"Player: {playerScore}",(40,80),
                cv2.FONT_HERSHEY_SIMPLEX,1,(0,255,0),3)

    cv2.putText(img,f"Computer: {computerScore}",(40,140),
                cv2.FONT_HERSHEY_SIMPLEX,1,(255,0,0),3)

    if startGame:

        if not stateResult:
            timer = time.time() - initialTime

            cv2.putText(img,str(int(3-timer)),(600,200),
                        cv2.FONT_HERSHEY_SIMPLEX,4,(0,0,255),4)

            if timer > 3:

                stateResult = True

                if hands:

                    hand = hands[0]
                    fingers = detector.fingersUp(hand)

                    if fingers == [0,0,0,0,0]:
                        playerMove = "Rock"

                    elif fingers == [1,1,1,1,1]:
                        playerMove = "Paper"

                    elif fingers == [0,1,1,0,0]:
                        playerMove = "Scissors"

                    else:
                        playerMove = ""

                    computerMove = random.choice(["Rock","Paper","Scissors"])

                    if playerMove == computerMove:
                        result = "Draw"

                    elif (playerMove=="Rock" and computerMove=="Scissors") or \
                         (playerMove=="Paper" and computerMove=="Rock") or \
                         (playerMove=="Scissors" and computerMove=="Paper"):

                        result = "Player Wins"
                        playerScore += 1

                    else:
                        result = "Computer Wins"
                        computerScore += 1

                    cv2.putText(img,f"Player: {playerMove}",(450,400),
                                cv2.FONT_HERSHEY_SIMPLEX,1,(0,255,0),3)

                    cv2.putText(img,f"Computer: {computerMove}",(450,450),
                                cv2.FONT_HERSHEY_SIMPLEX,1,(255,0,0),3)

                    cv2.putText(img,result,(450,520),
                                cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,255),3)

    cv2.imshow("Rock Paper Scissors AI",img)

    key = cv2.waitKey(1)

    if key == ord('s'):
        startGame = True
        initialTime = time.time()
        stateResult = False

    if key == 27:
        break

cap.release()
cv2.destroyAllWindows()

