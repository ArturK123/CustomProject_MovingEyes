"""
Demonstration of the GazeTracking library.
Check the README.md for complete documentation.
"""

import cv2
from gaze_tracking import GazeTracking
import pygame
from colors import changeBrightness
import numpy as np
from PIL import Image
from drawPupil import showPupil
import random
from toPostion import getMovingValues
import time
import datetime

##########################################################################################################################################
X = 2400
Y = 1080

#Eye Cordinates
Center_Down = 270, 370
Center_Up = 270, -45
Center = 270, 170
Left = -30,160
Left_Up = 100, 15
Left_Down = 100, 355
Right_Down = 500, 345
Right = 570, 160
Right_Up = 520,20

#Activate the pygame library
pygame.init()

 
# create the display surface object
# of specific dimension..e(X, Y).
scrn = pygame.display.set_mode((X, Y))
 
# set the pygame window name
pygame.display.set_caption('image')
 
# create a surface object, image is drawn on it.
back = pygame.image.load("sclera.png").convert()
back2 = pygame.image.load("sclera.png").convert()

iris = pygame.image.load("iris.png").convert()
iris2 = pygame.image.load("iris.png").convert()
iris = pygame.transform.flip(iris, True, False)

eyelid1 = pygame.image.load("modified_image.png").convert_alpha()
eyelid1 = pygame.transform.flip(eyelid1, True, False)
eyelid2 = pygame.image.load("modified_image2.png").convert_alpha()
eyelid2 = pygame.transform.flip(eyelid2, True, False)

eyelid1_t = pygame.image.load("modified_image.png").convert_alpha()
eyelid2_t = pygame.image.load("modified_image2.png").convert_alpha()

#Draw Pupil
pupilDiameter = 350
pupil = showPupil(pupilDiameter, 70)
pupil_image = pygame.image.fromstring(pupil.tobytes(), pupil.size, pupil.mode)

pupilDiameter = 350
pupil = showPupil(pupilDiameter, 70)
pupil_image2 = pygame.image.fromstring(pupil.tobytes(), pupil.size, pupil.mode)

rect_2 = pupil_image.get_rect()
rect_2.topleft = (250,190)

rect_3 = pupil_image2.get_rect()
rect_3.topleft = (250+1200,190)


status = True
timer = 0
current_number = 0
values = [Center[0], Center[1]]
values_animated = []
movements = [0.0, 0.0]
my_number = 0
step = 0
current_state = 15
frameCollection = [[0.0,0.0], [0.0,0.0]]


def doUpdate_Animate(current_number, timer, my_number):
    while True:
        scrn.fill(0)
        scrn.blit(back, (60,0))
        scrn.blit(back2, (1260,0))

        pygame.draw.circle(scrn, (0,0,0), (rect_2.x+pupilDiameter, rect_2.y+pupilDiameter), pupilDiameter/2)
        pygame.draw.circle(scrn, (0,0,0), (rect_2.x+pupilDiameter+1200, rect_2.y+pupilDiameter), pupilDiameter/2)

        scrn.blit(pupil_image, rect_2)

        scrn.blit(eyelid1, (60, current_number*-1))
        scrn.blit(eyelid2, (60, current_number))

        scrn.blit(pupil_image2, rect_3)

        pygame.draw.rect(scrn, (0,0,0), pygame.Rect(1200-60,0,120,1080))

        scrn.blit(eyelid1_t, (1260, current_number*-1))
        scrn.blit(eyelid2_t, (1260, current_number))

        pygame.draw.rect(scrn, (0,0,0), pygame.Rect(0,0,1200,current_number))
        pygame.draw.rect(scrn, (0,0,0), pygame.Rect(0,1080-current_number, 2400, 1080))
        pygame.draw.rect(scrn, (0,0,0), pygame.Rect(0,0,60,1200))
        pygame.draw.rect(scrn, (0,0,0), pygame.Rect(1200,0,2400,current_number))
        pygame.draw.rect(scrn, (0,0,0), pygame.Rect(2340,0,1200,2400))

        rect_2.x = values[0]
        rect_2.y = values[1]
        rect_3.x = rect_2.x + 1200
        rect_3.y = rect_2.y 

        #print("X:" + str(rect_2.x) + " Y: " + str(rect_2.y))


        timer += 1
        speed = gaze.horizontal_ratio()
        #print(speed)

        pygame.display.flip()
        if current_number < my_number:
            current_number = current_number + 8
        elif current_number >= my_number:
            break

def doUpdate(current_number, timer, my_number, val, values_animated):
    if val == 1:
        doUpdate_AnimteMovement(current_number, timer, my_number)
    else:
        basicMovement(current_number, timer, my_number)

def basicMovement(current_number, timer, my_number):
    while True:
        scrn.fill(0)
        scrn.blit(back, (60,0))
        scrn.blit(back2, (1260,0))

        pygame.draw.circle(scrn, (0,0,0), (rect_2.x+pupilDiameter, rect_2.y+pupilDiameter), pupilDiameter/2)
        pygame.draw.circle(scrn, (0,0,0), (rect_2.x+pupilDiameter+1200, rect_2.y+pupilDiameter), pupilDiameter/2)

        scrn.blit(pupil_image, rect_2)

        scrn.blit(eyelid1, (60, current_number*-1))
        scrn.blit(eyelid2, (60, current_number))

        scrn.blit(pupil_image2, rect_3)

        pygame.draw.rect(scrn, (0,0,0), pygame.Rect(1200-60,0,120,1080))

        scrn.blit(eyelid1_t, (1260, current_number*-1))
        scrn.blit(eyelid2_t, (1260, current_number))

        pygame.draw.rect(scrn, (0,0,0), pygame.Rect(0,0,1200,current_number))
        pygame.draw.rect(scrn, (0,0,0), pygame.Rect(0,1080-current_number, 2400, 1080))
        pygame.draw.rect(scrn, (0,0,0), pygame.Rect(0,0,60,1200))
        pygame.draw.rect(scrn, (0,0,0), pygame.Rect(1200,0,2400,current_number))
        pygame.draw.rect(scrn, (0,0,0), pygame.Rect(2340,0,1200,2400))
        rect_2.x = values[0]
        rect_2.y = values[1]
        rect_3.x = rect_2.x + 1200
        rect_3.y = rect_2.y 
        #print("X:" + str(rect_2.x) + " Y: " + str(rect_2.y))


        timer += 1
        speed = gaze.horizontal_ratio()
        #print(speed)

        pygame.display.flip()
        if current_number <= 10:
            break
        elif current_number >= my_number:
            current_number = current_number - 8
        time.sleep(1)

def doUpdate_AnimteMovement(current_number, timer, my_number):
    step = 0
    while True:
        scrn.fill(0)
        scrn.blit(back, (60,0))
        scrn.blit(back2, (1260,0))

        pygame.draw.circle(scrn, (0,0,0), (rect_2.x+pupilDiameter, rect_2.y+pupilDiameter), pupilDiameter/2)
        pygame.draw.circle(scrn, (0,0,0), (rect_2.x+pupilDiameter+1200, rect_2.y+pupilDiameter), pupilDiameter/2)

        scrn.blit(pupil_image, rect_2)

        scrn.blit(eyelid1, (60, current_number*-1))
        scrn.blit(eyelid2, (60, current_number))

        scrn.blit(pupil_image2, rect_3)

        pygame.draw.rect(scrn, (0,0,0), pygame.Rect(1200-60,0,120,1080))

        scrn.blit(eyelid1_t, (1260, current_number*-1))
        scrn.blit(eyelid2_t, (1260, current_number))

        pygame.draw.rect(scrn, (0,0,0), pygame.Rect(0,0,1200,current_number))
        pygame.draw.rect(scrn, (0,0,0), pygame.Rect(0,1080-current_number, 2400, 1080))
        pygame.draw.rect(scrn, (0,0,0), pygame.Rect(0,0,60,1200))
        pygame.draw.rect(scrn, (0,0,0), pygame.Rect(1200,0,2400,current_number))
        pygame.draw.rect(scrn, (0,0,0), pygame.Rect(2340,0,1200,2400))
        try:
            rect_2.x = values_animated[step][0]
            rect_2.y = values_animated[step][1]
            rect_3.x = rect_2.x + 1200
            rect_3.y = rect_2.y 
        except:
            break

        timer += 1
        step += 14
        speed = gaze.horizontal_ratio()
        pygame.display.flip()
        if current_number <= 10:
            pass
        elif current_number >= my_number:
            current_number = current_number - 8

pygame.display.flip()
##########################################################################################################################################

gaze = GazeTracking()
webcam = cv2.VideoCapture(0)
index = 0
closed = True


if __name__ == "__main__":
    while True:
        # We get a new frame from the webcam
        _, frame = webcam.read()

        # We send this frame to GazeTracking to analyze it
        gaze.refresh(frame)

        horizontal_ratio = gaze.horizontal_ratio()
        vertical_ratio = gaze.vertical_ratio()

        frame = gaze.annotated_frame()

        frameCollection[index] = [horizontal_ratio, vertical_ratio]
        animationYN = 0
        try:
            if abs(frameCollection[0][0] - frameCollection[1][0]) <= 0.03:
                animationYN = 1
            elif abs(frameCollection[0][1] - frameCollection[1][1]) <= 0.03:
                animationYN = 1
            else:
                animationYN = 0
        except:
            pass

        try:
            if gaze.vertical_ratio() <= 0.4:
                values = [values[0], 20]
                values_animated = getMovingValues(rect_2.x, rect_2.y, values[0], 20)
                my_number = 0
                doUpdate(current_number, timer, my_number, animationYN, values_animated)
                current_number = 0
            elif gaze.vertical_ratio() >= 0.60:
                values = [values[0], 360]
                values_animated = getMovingValues(rect_2.x, rect_2.y, values[0], 360)
                my_number = 0
                doUpdate(current_number, timer, my_number, animationYN, values_animated)
                current_number = 0
            else:
                values = [values[0], Center[1]]
                values_animated = getMovingValues(rect_2.x, rect_2.y, values[0], Center[1])
                my_number = 0
                doUpdate(current_number, timer, my_number, animationYN, values_animated)
                current_number = 0
        except:
            pass



        if gaze.is_blinking() and current_number != 150:
            # my_number = 150
            # current_number = 150
            # doUpdate_Animate(0, timer, 150)
            pass


        elif gaze.is_right():
            speed = gaze.horizontal_ratio()
            if speed == 0.0:
                values = [Right[0], values[1]]
                values_animated = getMovingValues(rect_2.x, rect_2.y, Right[0], values[1])
            elif speed >= 0.29 and speed <= 0.51:
                values = [400, values[1]]
                values_animated = getMovingValues(rect_2.x, rect_2.y, 400, values[1])
            else:
                values = [Right[0], values[1]]
                values_animated = getMovingValues(rect_2.x, rect_2.y, Right[0], values[1])
            doUpdate(current_number, timer, my_number, animationYN, values_animated)
            current_number = 0


        elif gaze.is_left():
            speed = gaze.horizontal_ratio()
            if speed == 1.0:
                values = [Left[0], values[1]]
                values_animated = getMovingValues(rect_2.x, rect_2.y, Left[0], values[1])
            elif speed >= 0.5 and speed <= 0.7:
                values = [110, values[1]]
                values_animated = getMovingValues(rect_2.x, rect_2.y, 110, values[1])
            else:
                values = [Left[0], values[1]]
                values_animated = getMovingValues(rect_2.x, rect_2.y, Left[0], values[1])
                my_number = 0
            doUpdate(current_number, timer, my_number, animationYN, values_animated)
            current_number = 0

        elif gaze.is_center():
            values = [Center[0], values[1]]
            values_animated = getMovingValues(rect_2.x, rect_2.y, Center[0], values[1])
            my_number = 0
            doUpdate(current_number, timer, my_number, animationYN, values_animated)
            current_number = 0

        try:
            print("Vertical: "+str(int(gaze.vertical_ratio()*100)) + ", Horizontal: "+str(int(gaze.horizontal_ratio()*100)))
        except:
            print("No Eyes")

        #clock.tick(60)

        #cv2.imshow("CameraWindow", frame)

        for i in pygame.event.get():
            if i.type == pygame.QUIT:
                status = False
        if index == 1:
            index -= 1
        else:
            index += 1
    webcam.release()
    cv2.destroyAllWindows()