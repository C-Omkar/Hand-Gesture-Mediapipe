# Imorting All the required Modules Necessary 
# (opencv, mediapipe, numpy)
# You may include math and time for displaying fps with ouput source
#############################################################################################################
import cv2
import mediapipe as mp
import numpy as np 
import time 
import math 
mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands
#############################################################################################################

# The main code is for you to make the class handDetector with all the required functions for getting the 
# info from the detected hand
# For each functions input, output and what has to be done is been included, your task is to write the code
# for getting the required output from the input in the respective functions
#############################################################################################################


class handDetector():
#############################################################################################################
#############################################################################################################
#############################################################################################################
#############################################################################################################
# Firstly the initialize constuctor is already defined if need be you can make any changes to this constructor
    def __init__(self, mode=False, maxHands=2, detectionCon=0.5, trackCon=0.5):
        self.mode = mode
        self.maxHands = maxHands
        self.detectionCon = detectionCon
        self.trackCon = trackCon

        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(self.mode, self.maxHands,
        self.detectionCon, self.trackCon)
        self.mpDraw = mp.solutions.drawing_utils
        self.tipIds = [4, 8, 12, 16, 20]

#############################################################################################################
# findHands function takes the image source from the calling block and if the input draw = True then draw the
# hands with all the landmarks using mediapip Hands solution (Read the doc for details)
# Also add the results to the class variable results which would then be used for further calculations
    def findHands(self, img, draw=True):
        #Firstly remember to convert the given image in RBG to RGB
        img_RGB = cv2.cvtColor(cv2.flip(img, 1),cv2.COLOR_BGR2RGB)
        show = img_RGB.copy() 

        # call hands.process and pass the converted image to it and store in self.results
        with mp_hands.Hands(min_detection_confidence=0.6,min_tracking_confidence=0.4) as hands:
            img_RGB.flags.writeable = False
            self.results = hands.process(img_RGB)
            
        # For Debugging you can print(results.multi_hand_landmarks)
        # Write the code for drawing the landmarks
            show.flags.writeable = True
            show = cv2.cvtColor(show, cv2.COLOR_RGB2BGR)
            if self.results.multi_hand_landmarks:
                for hand_landmarks in self.results.multi_hand_landmarks:
                    mp_drawing.draw_landmarks(show, hand_landmarks, mp_hands.HAND_CONNECTIONS)

        img = show.copy()
        # Finally return the image

        return img

# findPosition function takes the image source, hand we are currently working in the image source
# and if to draw or not from the calling block and if the input draw = True then draw the
# hand positions with all the landmarks using mediapip Hands solution (Read the doc for details)
# also make the x-coordinate, y-coordinate and the the rectangle containing the hand and aslo the landmark list
# Also add the results to the class variable results which would then be used for further calculations
    def findPosition(self, img, handNo=0, draw=True):
        xList = []
        yList = []
        bbox = []
        self.lmList = []
        box = np.array(bbox)
        #Write the code here 
        # Remember: mp gives you landmarks which are normalized to 0.0 and 1.0 which need to be converted into 
        # exact coordinates for use

        self.image_height, self.image_width, _ = img.shape
        if self.results.multi_hand_landmarks:
            for hand in self.results.multi_hand_landmarks:
                for landmark in hand.landmark:
                    xList.append(landmark.x * self.image_width)
                    yList.append(landmark.y * self.image_height)
                    self.lmList.append([landmark.z, 
                    landmark.x * self.image_width, landmark.y * self.image_height])


            self.right = max(xList)
            self.left = min(xList)
            self.top = max(yList)
            self.bottom = min(yList)

            
            bbox.append([min(xList), max(yList)])
            bbox.append([max(xList), max(yList)])
            bbox.append([max(xList), min(yList)])
            bbox.append([min(xList), min(yList)])
            
        # Draw if the draw given is true

        # if draw:
        #     img = cv2.polylines(img, box, True,(0,255,0), 3)

        return self.lmList, box
# fingersUp function return list of 5 fingers and their respective state
# 0- down and 1- Up
# Make sure to go through the mediapipe docs to get to know landmark 
# number of each finger and a method to know if the finger is up or not 
    def fingersUp(self):
        fingers = []
        
        for hand in self.results.multi_hand_landmarks:
            for fingerid in self.tipIds:
                if hand.landmark[fingerid].y > hand.landmark[fingerid-3].y:
                    fingers.append(1)
                else:
                    fingers.append(0)


        return fingers

# findDistance function returns the image after drawing distance between 2 points 
# and drawing thar distance and highlighting the points with r radius circle and 
# t thickness line and also return length there
# this function would help us make our click to execute

    def findDistance(self, p1, p2, img, draw=True, r=15, t=3):
        x1, y1 = self.lmList[p1][1:]
        x2, y2 = self.lmList[p2][1:]
        cx, cy = (x1 + x2) // 2, (y1 + y2) // 2

        # write your code here
        length = math.dist([x1,y1],[x2,y2])

        if draw:
            img = cv2.line(img, (x1,y1), (x2,y2), (255,255,255), t)
            img = cv2.circle(img, (x1,y1), r, (255,255,255),-1)
            img = cv2.circle(img, (x2,y2), r, (255,255,255),-1)
            img = cv2.circle(img, (cx,cy), r, (255,255,255),-1)

        return length, img, [x1, y1, x2, y2, cx, cy]
#############################################################################################################
#############################################################################################################
#############################################################################################################
#############################################################################################################





# Now for the main function is to check and debug the class
# You may change it any way you want
# I have added the FPS counter and take the video feed from the PC
# If you donot have a webcam in yout PC you can use DROID CAM Software
# To debug you can also use image of a hand , the code for this I have commented out
# you can decomment it out and comment the video feed code to debug if you feel 
# some functipn is not working as required


#############################################################################################################

def main():
    pTime = 0
    cTime = 0
    # Add the video source here
    # 0-For your first webcam in the PC
    cap = cv2.VideoCapture(0)
    detector = handDetector()
    while True:
        ret, img = cap.read()
        img = detector.findHands(img)
        lmList, boundary = detector.findPosition(img)
        # if len(lmList) != 0:
        #     print(lmList[3])

        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime

        cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3,
                    (0, 0, 0), 3)
        cv2.polylines(img, boundary, True,(0,255,0), 3)

        cv2.imshow("Image", img)
        cv2.waitKey(10)
    
    # img = cv2.imread("./File path for image goes here"")
    # img = detector.findHands(img)
    # lmList = detector.findPosition(img)
    # #if len(lmList) != 0:
    # #    print(lmList[3])



    # cv2.imshow("Image", img)
    # cv2.waitKey(0)
        


if __name__ == "__main__":
    main()