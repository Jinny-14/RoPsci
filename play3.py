import pygame
import tempfile
import cv2
import time
import os
import handtrackingModule as htm
import random

pygame.font.init()

font = pygame.font.SysFont(None, 20)
font1 = pygame.font.SysFont("Times new Roman", 55)
font2 = pygame.font.SysFont("Times new Roman", 27)
font3 = pygame.font.SysFont("Times new Roman", 20)

color = (255, 255, 255)
color_light = ( 170, 170, 170)
color_dark = (100, 100, 100)
n_round=-1

#Render the text in new surface
text1 = font1.render("Welcome to RoPSci!", True, (100, 10, 10))
text2 = font2.render("Select the number of rounds:", True, (20,2,2))
text3 = font2.render("Instructions to play the game:", True, (30, 2, 2))
text4 = font2.render('PLAY', True, color)

text_r = font2.render("Rock", True, (20, 2, 2))
text_p = font2.render("Paper", True, (20, 2, 2))
text_s = font2.render("Scissor", True, (20, 2, 2))

text_i1 =font3.render("1) Select the number of rounds and click on \'Play\'.", True, (20, 2, 2))
text_i2a =font3.render("2) While the screen shows \'Rock\'... \'Paper\'... \'Scissor\', keep your", True, (20, 2, 2))
text_i2b =font3.render("     hand ready with the response you want to give.", True, (20, 2, 2))
text_i3a =font3.render("3) Make sure to keep your hand stable, upright and around 40 cm ", True, (20, 2, 2))
text_i3b =font3.render("     to 50 cm away from the web cam.", True, (20, 2, 2))

image_r = pygame.image.load(r'C:\Users\Rashi Patil\projects\Python\RoPSci Project\Rock.jpg')
image_p = pygame.image.load(r'C:\Users\Rashi Patil\projects\Python\RoPSci Project\Paper.jpg')
image_s = pygame.image.load(r'C:\Users\Rashi Patil\projects\Python\RoPSci Project\Sc.jpg')

DEFAULT_IMAGE_SIZE = (75, 100)

image_r = pygame.transform.scale(image_r, DEFAULT_IMAGE_SIZE)
image_p = pygame.transform.scale(image_p, DEFAULT_IMAGE_SIZE)
image_s = pygame.transform.scale(image_s, DEFAULT_IMAGE_SIZE)

image_r2 = image_r
image_p2 = image_p
image_s2 = image_s

D_IMAGE_SIZE = (150, 200)

image_r2 = pygame.transform.scale(image_r2, D_IMAGE_SIZE)
image_p2 = pygame.transform.scale(image_p2, D_IMAGE_SIZE)
image_s2 = pygame.transform.scale(image_s2, D_IMAGE_SIZE)

class Checkbox:
    def __init__(self, surface, x, y, idnum, color=(230, 230, 230),
        caption="", outline_color=(0, 0, 0), check_color=(0, 0, 0),
        font_size=40, font_color=(0, 0, 0), 
    text_offset=(28, 1), font='Ariel Black'):
        self.surface = surface
        self.x = x
        self.y = y
        self.color = color
        self.caption = caption
        self.oc = outline_color
        self.cc = check_color
        self.fs = font_size
        self.fc = font_color
        self.to = text_offset
        self.ft = font

        #identification for removal and reorginazation
        self.idnum = idnum

        # checkbox object
        self.checkbox_obj = pygame.Rect(self.x, self.y, 20, 20)
        self.checkbox_outline = self.checkbox_obj.copy()

        # variables to test the different states of the checkbox
        self.checked = False

    def _draw_button_text(self):
        self.font = pygame.font.SysFont(self.ft, self.fs)
        self.font_surf = self.font.render(self.caption, True, self.fc)
        w, h = self.font.size(self.caption)
        self.font_pos = (self.x + self.to[0], self.y + 20 / 2 - h / 2 + 
        self.to[1])
        self.surface.blit(self.font_surf, self.font_pos)

    def render_checkbox(self):
        if self.checked:
            pygame.draw.rect(self.surface, self.color, self.checkbox_obj)
            pygame.draw.rect(self.surface, self.oc, self.checkbox_outline, 1)
            pygame.draw.circle(self.surface, self.cc, (self.x + 10, self.y + 10), 5)

        elif not self.checked:
            pygame.draw.rect(self.surface, self.color, self.checkbox_obj)
            pygame.draw.rect(self.surface, self.oc, self.checkbox_outline, 1)
        self._draw_button_text()

    def _update(self, event_object):
        x, y = pygame.mouse.get_pos()
        px, py, w, h = self.checkbox_obj
        if px < x < px + w and py < y < py + w:
            if self.checked:
                self.checked = False
            else:
                self.checked = True

    def update_checkbox(self, event_object):
        if event_object.type == pygame.MOUSEBUTTONDOWN:
            self.click = True
            self._update(event_object)
            
def game():
    running =True
    screen1=pygame.display.set_mode([800, 600])
    screen1.fill((100, 0 ,100))
    
    wCam , hCam = 640, 480
    ges = "m"  #initiallizing user's response variable in terms of rock, paper and scissor
    mes = "m"  #initiallizing computer's response variable in terms of rock, paper and scissor
    res = "None" #initiallizing point goes to "res"
    uss = -1  #initializing user's response variable in terms of 1 2 3
    comp = -1 #initializing computer's response variable in terms of 1 2 3
    score =0  #intializing user's score
    score_o =0  #initializing opponents score

    cap= cv2.VideoCapture(0)  #storing the webcam input in a variable cap
    cap.set(3, wCam)
    cap.set(4, hCam)
    
    detector = htm.handDectector()  # creates an object of called detector from handDetector Class, hand tracking module

    tipids = [4,8,12,16,20] # ids of the tip of the fingers 
    
    for i in range(n_round): # loops runs for the number of rounds selected
        screen1.fill((100, 0 ,100))
    
        text5 = font2.render("Round: " + str(i+1), True, (0, 0, 0))
        screen1.blit(text5, (400 - text5.get_width()// 2, 50 - text5.get_height()//2))
        text11 = font2.render("Your Score: "+ str(score), True, (0, 0, 0))
        screen1.blit(text11, (200 - text11.get_width()// 2, 520 - text11.get_height()//2))
        text13 = font2.render("Opponent Score: "+ str(score_o), True, (0, 0, 0))
        screen1.blit(text13, (500 - text13.get_width()// 2, 520 - text13.get_height()//2))
        

        text6 = font2.render("ROCK!", True, (0,0,0))
        text7 = font2.render("Paper!", True, (0,0,0))
        text8 = font2.render("Scissor!", True, (0,0,0))

        #rendering the text 'rock', updating this on the screen and then pausing the execution of code for 1 sec
        screen1.blit(text6, (300 - text6.get_width()// 2, 300 - text6.get_height()//2))
        pygame.display.update()
        pygame.time.wait(1000)
        
        #covering the previous text 'rock' by a rectangle of color same as background and then rendering the
        # text 'paper', updating and pausing for 1 sec
        pygame.draw.rect(screen1, (100, 0, 100), pygame.Rect(0, 100, 700, 400)) 
        screen1.blit(text7, (400 - text7.get_width()// 2, 300 - text7.get_height()//2))
        pygame.display.update()
        pygame.time.wait(1000)

        #covering the previous text 'paper' by a rectangle of color same as background and then rendering the
        # text 'scissor', updating and pausing for 1 sec
        pygame.draw.rect(screen1, (100, 0, 100), pygame.Rect(0, 100, 700, 400))
        screen1.blit(text8, (500 - text8.get_width()// 2, 300 - text8.get_height()//2))
        pygame.display.update()
        pygame.time.wait(1000)


        success, img = cap.read() 
        frame = img.copy()
        left = img.copy()
        img = detector.findHands(img) #detects hand in img
        lmList = detector.findPosition(img, draw=False) #lmList conatins the positions of all the 21 ids of the hand
        # 0 contains the id number, 1 contains the id's x coordinate, 2 conatins the id's y coordinate
        flag = 0 # keeps the track of right-left hand, flag==0 indicates right hand and flag==1 indicates left hand

        if len(lmList) !=0:
            # coparing the base point of thumb to the base point of last finger so as to conclude left/right hand 
            if ( lmList[1][1]<lmList[17][1] ):
                #incase of a left hand, flip the img and then proceed
                img = cv2.flip(left, 1)
                flag = 1
                img = detector.findHands(frame)
                lmList = detector.findPosition(img, draw=False)

        if len(lmList) != 0: #if hand is detected i.e, ids and there positions are present in lmList
            fingers = [] # list that keep tracks of open/closed finger
            #thumb
                # for right hand
            if flag == 0: 
                #comparing the tip of thumb to the point below tip in horizontal direction
                if lmList[tipids[0]][1]> lmList[tipids[0]-1][1]:
                    fingers.append(1)
                else:
                    fingers.append(0)
                #for left hand
            else:   
                if lmList[tipids[0]][1]< lmList[tipids[0]-1][1]:
                    fingers.append(1)
                else:
                    fingers.append(0)

            #four fingers
            for id in range(1,5):
                #comparing the tip of finger to the point below tip in vertical direction
                if lmList[tipids[id]][2]< lmList[tipids[id]-2][2]:
                    fingers.append(1)
                else:
                    fingers.append(0)

            totalFingers = fingers.count(1)
            #code to determine whether it is a rock,paper or scissor 
            if (totalFingers==0):
                ges = "Rock"
                uss = 1
            elif (totalFingers==5):
                ges = "Paper"
                uss = 2
            elif (totalFingers==2):
                if(fingers[1]==1 and fingers[2]==1):
                    ges = "Scissor"
                    uss = 3
                else:
                    ges="Invalid move"
                    uss = -1
            else:
                ges = "Invalid move"
                uss = -1
        
        #incase a hand is not detected 
        else:
            ges = "Invalid move"
            uss = -1
        
        #generating random response from the computer
        comp = random.randint(1,3)
        if (comp==1):
            mes = "Rock"
        if (comp==2):
            mes = "Paper"
        if (comp==3):
            mes = "Scissor"
        
        #converting the web cam input img which is of the format numpy ndarray to surafce of pygame
        frame = pygame.surfarray.make_surface(frame)
        #rotating the frme by 270 degree and scaling it as required
        frame = pygame.transform.rotate(frame, 270)
        NEW_IMAGE_SIZE = (250, 200)
        frame = pygame.transform.scale(frame, NEW_IMAGE_SIZE)

        pygame.draw.rect(screen1, (100, 0, 100), pygame.Rect(0, 100, 700, 400))
        screen1.blit(frame, (110, 200))
        
        #displying images according to what computer response is generated
        if comp ==1:
            screen1.blit(image_r2, (550, 200))
        if comp==2:
            screen1.blit(image_p2, (550, 200))
        if comp ==3:
            screen1.blit(image_s2, (550, 200))

        text9 = font2.render("Comp response: " + mes, True, (0,0,0))
        text10 = font2.render("Your response: " + ges, True, (0,0,0))

        
        screen1.blit(text9, (600 - text9.get_width()// 2, 150 - text9.get_height()//2))
        screen1.blit(text10, (200 - text10.get_width()// 2, 150 - text10.get_height()//2))
        pygame.display.update()
        pygame.time.wait(2000)

        if(comp==-1) or (uss==-1):
            res = "None, invalid "
        elif (comp==uss):
            res = "None"
        elif (((comp==1) and (uss ==2)) or ((comp==2) and (uss == 3)) or ((comp==3) and (uss ==1))):
            res = "You!"
            score = score +1
        else:
            res = "Opponent!"
            score_o = score_o+1
        
        pygame.draw.rect(screen1, (100, 0, 100), pygame.Rect(0, 100, 800, 500))
        pygame.display.update()
        text11 = font2.render("Your Score: "+ str(score), True, (0, 0, 0))
        screen1.blit(text11, (200 - text11.get_width()// 2, 520 - text11.get_height()//2))
        text13 = font2.render("Opponent Score: "+ str(score_o), True, (0, 0, 0))
        screen1.blit(text13, (500 - text13.get_width()// 2, 520 - text13.get_height()//2))
        text12 = font2.render("Point goes to " + res, True, (0,0,0))
        screen1.blit(text12, (400 - text12.get_width()// 2, 300 - text12.get_height()//2))
        pygame.display.update()
        pygame.time.wait(1000)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
      
        
        pygame.display.update()
    if(score_o>score):
        text14 = font1.render("You Lost!" , True, (10,0,0))
    elif(score_o<score):
        text14 = font1.render("You Won!" , True, (10,0,0))
    else:
        text14 = font1.render("Tie!", True, (10,0,0))
        
    pygame.draw.rect(screen1, (100, 0, 100), pygame.Rect(0, 100, 700, 400))
    screen1.blit(text14, (400 - text14.get_width()// 2, 300 - text14.get_height()//2))
    pygame.display.update()
    pygame.time.wait(2000)

    text15 = font2.render("Press ESC to quit game" , True, (10,0,0))
    text16 = font2.render("Press any other key to return to Home" , True, (10,0,0))
    screen1.blit(text15, (400 - text15.get_width()// 2, 350 - text15.get_height()//2))
    screen1.blit(text16, (400 - text16.get_width()// 2, 380 - text16.get_height()//2))
    pygame.display.update()

    k = True
    while k:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                k = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                else:
                    k = False
            
            

click = False

def main():
    boxes = []
    screen=pygame.display.set_mode([800, 600])
    screen.fill((100, 0 ,240))

    button1 = Checkbox(screen, 370, 440, 0, caption='3')
    button2 = Checkbox(screen, 430, 440, 1, caption='5')
    button3 = Checkbox(screen, 490, 440, 2, caption='7')
    boxes.append(button1)
    boxes.append(button2)
    boxes.append(button3)
    
    screen.blit(image_r, (650, 100))
    screen.blit(image_p, (650, 250))
    screen.blit(image_s, (650, 400))

    screen.blit(text_r, (685 - text_r.get_width()// 2, 220 - text_r.get_height()//2))
    screen.blit(text_p, (689 - text_p.get_width()// 2, 370 - text_p.get_height()//2))
    screen.blit(text_s, (689- text_s.get_width()// 2, 520 - text_s.get_height()//2))
    
    screen.blit(text1, (400 - text1.get_width()// 2, 50 - text1.get_height()//2))
    screen.blit(text2, (200 - text2.get_width()// 2, 450 - text2.get_height()//2))
    screen.blit(text3, (180 - text2.get_width()// 2, 150 - text2.get_height()//2))

    screen.blit(text_i1, (50 , 180))
    screen.blit(text_i2a, (50 , 220))
    screen.blit(text_i2b, (50 , 240))
    screen.blit(text_i3a, (50 , 280))
    screen.blit(text_i3b, (50 , 300))
    
    running = True
    while running:
        global n_round
        
        mouse = pygame.mouse.get_pos() #Input from mouse or touchpad
        p_button = pygame.Rect(350, 500, 100, 35) 
        if p_button.collidepoint((mouse[0],mouse[1])):  #Incase mouse is hovered over the rectangle (p_button)
            if click and n_round != -1: # Incase the mouse button is clicked and number of round selected is not empty, if it is empty nothing will happen
                game()  # directed to the game window
                screen.fill((100, 0 ,240))   # back to original window after complete execution of game window
            
                button1 = Checkbox(screen, 370, 440, 0, caption='3')
                button2 = Checkbox(screen, 430, 440, 1, caption='5')
                button3 = Checkbox(screen, 490, 440, 2, caption='7')
                boxes.append(button1)
                boxes.append(button2)
                boxes.append(button3)
                
                screen.blit(image_r, (650, 100))
                screen.blit(image_p, (650, 250))
                screen.blit(image_s, (650, 400))

                screen.blit(text_r, (685 - text_r.get_width()// 2, 220 - text_r.get_height()//2))
                screen.blit(text_p, (689 - text_p.get_width()// 2, 370 - text_p.get_height()//2))
                screen.blit(text_s, (689- text_s.get_width()// 2, 520 - text_s.get_height()//2))
                
                screen.blit(text1, (400 - text1.get_width()// 2, 50 - text1.get_height()//2))
                screen.blit(text2, (200 - text2.get_width()// 2, 450 - text2.get_height()//2))
                screen.blit(text3, (180 - text2.get_width()// 2, 150 - text2.get_height()//2))

                screen.blit(text_i1, (50 , 180))
                screen.blit(text_i2a, (50 , 220))
                screen.blit(text_i2b, (50 , 240))
                screen.blit(text_i3a, (50 , 280))
                screen.blit(text_i3b, (50 , 300))
        pygame.draw.rect(screen,(255, 0, 0), p_button)

        click = False
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
            
            if event.type == pygame.MOUSEBUTTONDOWN:    
                if event.button == 1:
                    click = True

                   
                for box in boxes:
                    box.update_checkbox(event)
                    if box.checked is True:
                        n_round = int(box.caption) 
                        for b in boxes:
                            if b != box:
                                b.checked = False
        screen.blit(text4 , (367,500))

        for box in boxes:
            box.render_checkbox()

        pygame.display.update()
        pygame.display.flip()
    
    pygame.time.wait(1000)

if __name__=='__main__':
    main()