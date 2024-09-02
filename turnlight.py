import cv2
import handtrackmin
import mediapipe as mp
import time
import math
from handtrackmin import *
from cvzone.SerialModule import SerialObject
from time import sleep

try:
    arduino = SerialObject("/dev/cu.usbmodem14201", 9600)
    sleep(2)
    print("Connection !\n")
except Exception as e:
    print("failed {e}")



def main():
    pTime = 0
    cTime = 0
    
    prevSend = 0
    cap = cv2.VideoCapture(0)
    detector = handDetector()
    while True:
        success, img = cap.read()
        img = detector.findHands(img, draw=True)
        lmList, fingerList = detector.findPosition(img)
        if len(lmList)!=0:
            x1, y1 = lmList[4][1], lmList[4][2]
            x2, y2 = lmList[8][1], lmList[8][2]

            # circle the correct finger
            cv2.circle(img, (x1,y1), 10, (255,0,255), cv2.FILLED)
            cv2.circle(img, (x2,y2), 10, (255,128,255), cv2.FILLED)
            
            # line between fingers
            cv2.line(img, (x1,y1), (x2,y2), (0,128,0), 2)

            dist = (abs(x1-x2)+abs(y1-y2))/2
            # print("dist: " , dist , " \n")
            if( dist < 30 ):
                if prevSend == 0:
                    arduino.sendData([1])
                    prevSend = 1
                else:
                    arduino.sendData([0])
                    prevSend = 0

                cv2.circle(img, ((x1+x2)//2, (y1+y2)//2), 15, (0, 255, 0), cv2.FILLED)
                print("ON!!\n")

        # fps counter
        cTime = time.time()
        fps = 1/(cTime-pTime)
        pTime = cTime
    
        cv2.putText(img, str(int(fps)), (10,70), cv2.FONT_HERSHEY_PLAIN, 3, (255,0,255), 2)
        cv2.imshow("Image", img)
        # end   
        if cv2.waitKey(1) & 0xFF == ord('q'):
            print("Ended!")
            break
    
if __name__ == "__main__":
    main()
    # while True:
    #     arduino.sendData([0])
    #     sleep(3)
    #     arduino.sendData([1])
    #     sleep(1)
