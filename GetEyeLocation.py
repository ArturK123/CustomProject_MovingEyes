import cv2
import mediapipe as mp
from drawPupil import showPupil
import pygame
from toPostion import getMovingValues
import random

X = 2400
Y = 1080

pygame.init()

scrn = pygame.display.set_mode((X, Y))
 
# set the pygame window name
pygame.display.set_caption('image')

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

pupilDiameter = 350
pupil = showPupil(pupilDiameter, 70)
pupil_image = pygame.image.fromstring(pupil.tobytes(), pupil.size, pupil.mode)

pupilDiameter = 350
pupil = showPupil(pupilDiameter, 70)
pupil_image2 = pygame.image.fromstring(pupil.tobytes(), pupil.size, pupil.mode)

rect_2 = pupil_image.get_rect()
rect_2.topleft = (250,190)

rect_3 = eyelid1.get_rect()
rect_3.topleft = (60,0)

values_animated = []
values_animated_eyelid = []

current_int_x = 0
current_int_y = 0

speed = 0
step = 0
step2 = 0

lefteye_pos_x = 0
lefteye_pos_y = 0

eyelid_pos_x = 0
eyelid_pos = 0

cam = cv2.VideoCapture(0)
face_mesh = mp.solutions.face_mesh.FaceMesh(refine_landmarks=True)
while True:
    _, frame = cam.read()
    frame = cv2.flip(frame, 1)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    output = face_mesh.process(rgb_frame)
    landmark_points = output.multi_face_landmarks
    frame_h, frame_w, _ = frame.shape
    if landmark_points:
        landmarks = landmark_points[0].landmark

        valuble_points = [landmarks[468], landmarks[473], landmarks[8]] #Left #Right #Center 

        center_x = int(valuble_points[2].x * frame_w)
        center_y = int(valuble_points[2].y * frame_h)

        lefteye_x = int(valuble_points[0].x * frame_w)
        lefteye_y = int(valuble_points[0].y * frame_h)

        righteye_x = int(valuble_points[1].x * frame_w)
        righteye_y = int(valuble_points[1].y * frame_h)

        left = [landmarks[145], landmarks[159]]
        right = [landmarks[386], landmarks[374]]

        step = 0
        speed = 12

        current_int_x = lefteye_pos_x
        current_int_y = lefteye_pos_y

        current_eyelid_pos = rect_3.y

        lefteye_pos_x = (int(valuble_points[0].x * 1200) - int(left[0].x * 1200))*20 + 260
        lefteye_pos_y = (int(int(valuble_points[0].y * 1200) - left[0].y * 1200)*25) + (1080/2) + 100

        eyelid_pos = abs(int(left[1].y * frame_h)-int(left[0].y * frame_h))*10
        eyelid_pos = 260 - eyelid_pos
        print(eyelid_pos)
        eyelid_pos_x = 0

        values_animated = getMovingValues(rect_2.x, rect_2.y, lefteye_pos_x, lefteye_pos_y)
        values_animated_eyelid = getMovingValues(current_eyelid_pos, 0, eyelid_pos, 0)

        if len(values_animated) > 100:
            speed = 20
        else:
            speed = 12

        if (abs(current_int_x - lefteye_pos_x) > 20 and abs(current_int_y - lefteye_pos_y) > 20) or (abs(current_int_x - lefteye_pos_x) > 40) or (abs(current_int_y - lefteye_pos_y) > 40) or abs(eyelid_pos - rect_3.y) > 100:
            for i in range(int(len(values_animated)/speed)):
                # eyelid_pos_x = abs(int(left[1].y * frame_h - left[0].y * frame_h))*10

                scrn.fill(0)

                scrn.blit(back, (60,0))
                scrn.blit(back, (1260,0))

                rect_2.x = values_animated[step][0]
                rect_2.y = values_animated[step][1]

                scrn.blit(pupil_image, rect_2)
                scrn.blit(pupil_image, (rect_2.x+1200, rect_2.y))

                scrn.blit(eyelid1, (60, rect_3.y*-1))
                scrn.blit(eyelid2, (60, rect_3.y))

                scrn.blit(eyelid1_t, (1260, rect_3.y*-1))
                scrn.blit(eyelid2_t, (1260, rect_3.y))

                pygame.draw.rect(scrn, (0,0,0), pygame.Rect(0,0,2400,rect_3.y))
                pygame.draw.rect(scrn, (0,0,0), pygame.Rect(0,1080-rect_3.y, 2400, 1080))

                pygame.draw.rect(scrn, (0,0,0), pygame.Rect(1200-60,0,120,1080))
                pygame.draw.rect(scrn, (0,0,0), pygame.Rect(2340,0,1200,2400))
                pygame.draw.rect(scrn, (0,0,0), pygame.Rect(0,0,60,1200))

                pygame.display.flip()
                step = step + speed
            for i in range(int(len(values_animated_eyelid)/10)):
                scrn.fill(0)

                scrn.blit(back, (60,0))
                scrn.blit(back, (1260,0))

                scrn.blit(pupil_image, rect_2)
                scrn.blit(pupil_image, (rect_2.x+1200, rect_2.y))

                scrn.blit(eyelid1, (60, rect_3.y*-1))
                scrn.blit(eyelid2, (60, rect_3.y))

                scrn.blit(eyelid1_t, (1260, rect_3.y*-1))
                scrn.blit(eyelid2_t, (1260, rect_3.y))

                pygame.draw.rect(scrn, (0,0,0), pygame.Rect(0,0,2400,rect_3.y))
                pygame.draw.rect(scrn, (0,0,0), pygame.Rect(0,1080-rect_3.y, 2400, 1080))

                rect_3.y = values_animated_eyelid[eyelid_pos_x][0]

                pygame.draw.rect(scrn, (0,0,0), pygame.Rect(1200-60,0,120,1080))
                pygame.draw.rect(scrn, (0,0,0), pygame.Rect(2340,0,1200,2400))
                pygame.draw.rect(scrn, (0,0,0), pygame.Rect(0,0,60,1200))

                pygame.display.flip()
                eyelid_pos_x = eyelid_pos_x + 10
    cv2.waitKey(1)