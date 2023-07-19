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

drawOverlay = []

for i in range(Y):
    currentArray = []
    for j in range(Y):
        currentArray.append((0, 0, 0))

    drawOverlay.append(currentArray)

print(drawOverlay)

upper_colormap = Image.open('upper.png')
lower_colormap = Image.open('lower.png')

#Eye Cordinates
Center_Down = 270, 370
Center_Up = 270, -45
Center = 270, 170
Left = -30,230
Left_Up = 100, 15
Left_Down = 100, 355
Right_Down = 500, 345
Right = 570, 160
Right_Up = 520,20

#Backround Colormaping
upper = np.array(upper_colormap)
upper_i = np.invert(upper_colormap)

lower = np.array(lower_colormap)
lower_i = np.invert(lower_colormap)

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

#Show Back
scrn.blit(back, (60,0))

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


pygame.display.flip()
clock = pygame.time.Clock()
status = True
timer = 0
my_number = 0
current_number = 0
values = []
step = 0
current_state = 15
##########################################################################################################################################

gaze = GazeTracking()
webcam = cv2.VideoCapture(0)

while True:
    # We get a new frame from the webcam
    _, frame = webcam.read()

    # We send this frame to GazeTracking to analyze it
    gaze.refresh(frame)

    frame = gaze.annotated_frame()

    if gaze.is_blinking():
        pass
    elif gaze.is_right():
        if current_state != 1:
            values = getMovingValues(rect_2.x, rect_2.y, Right[0], Right[1])
            step = 0
        current_state = 1
    elif gaze.is_left():
        if current_state != 0:
            values = getMovingValues(rect_2.x, rect_2.y, Left[0], Left[1])
            step = 0
        current_state = 0
    elif gaze.is_center():
        if current_state != 2:
            values = getMovingValues(rect_2.x, rect_2.y, Center[0], Center[1])
            step = 0
        current_state = 2

    #clock.tick(60)
    scrn.fill(0)
    if timer == 100:
        my_number = random.randint(0, 100)
        timer = 0

    for i in pygame.event.get():
        if i.type == pygame.QUIT:
            status = False

    try:
        rect_2.x = values[step][0]
        rect_2.y = values[step][1]
        rect_3.x = rect_2.x + 1200
        rect_3.y = rect_2.y 
    except:
        pass
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
    #pygame.draw.rect(scrn, (0,0,0), pygame.Rect(1200-60,0,1200,1200))

    # pygame.draw.circle(scrn, (0,0,0), (rect_2.x+pupilDiameter+1200, rect_2.y+pupilDiameter+1200), pupilDiameter/2)
    # scrn.blit(pupil_image, (rect_2.x+1200, rect_2.y+1200))
    # scrn.blit(eyelid1, (1260, current_number*-1))
    # scrn.blit(eyelid2, (1260, current_number))
    pygame.draw.rect(scrn, (0,0,0), pygame.Rect(1200,0,2400,current_number))
    #pygame.draw.rect(scrn, (0,0,0), pygame.Rect(1200,1080-current_number, 2400, 1080))
    pygame.draw.rect(scrn, (0,0,0), pygame.Rect(2340,0,1200,2400))


    print("X:" + str(rect_2.x) + " Y: " + str(rect_2.y))
  # iterate over the list of Event objects
  # that was returned by pygame.event.get() method.
    if current_number < my_number:
        current_number = current_number + 3
    if current_number > my_number:
        current_number = current_number - 3
    timer += 1
    step += 3
    pygame.display.flip()
   
webcam.release()
cv2.destroyAllWindows()
