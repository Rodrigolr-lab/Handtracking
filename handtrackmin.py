import cv2
import mediapipe as mp
import time
import math

class Finger:
    def __init__(self, id=None, cx=None, cy=None):
        self.id = id
        self.cx = cx
        self.cy = cy

class handDetector():
    def __init__ (self, mode=False, maxHands=2, detectionCon=1, trackCon=0.5):
        self.mode=mode
        self.maxHands=maxHands
        self.detectionCon=detectionCon
        self.trackCon=trackCon

        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(self.mode, self.maxHands, self.detectionCon, self.trackCon)
        self.mpDraw = mp.solutions.drawing_utils

    def findHands(self, img, draw=True):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(imgRGB)
        if self.results.multi_hand_landmarks:
            for handLms in self.results.multi_hand_landmarks:
                self.mpDraw.draw_landmarks(img, handLms, self.mpHands.HAND_CONNECTIONS)
        return img

    def findPosition(self, img, handNo=0, draw=True ):
        lmList = []
        fingerList = []
        if self.results.multi_hand_landmarks:
            myHand =  self.results.multi_hand_landmarks[handNo]
            for id, lm in enumerate(myHand.landmark):
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                # print(id, cx, cy)
                index = Finger()
                if id == 8:
                    index.cx = cx
                    index.cy = cy
                thumb = Finger()
                if id == 4:
                    thumb.cx = cx
                    thumb.cy = cy
                fingerList.append(thumb)
                fingerList.append(index)

                lmList.append([id, cx, cy])
                if not draw:
                    cv2.circle(img, (cx,cy), 10, (128,128,0), cv2.FILLED)
        return lmList, fingerList

def main():
    pTime = 0
    cTime = 0
    
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
            print("dist: " , dist , " \n")
            if( dist < 30):
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
