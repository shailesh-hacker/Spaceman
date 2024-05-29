import pygame
import random
from pygame import mixer

pygame.init()
mixer.init()
mixer.music.load("space.mp3")
mixer.music.set_volume(0.7)  

clock=pygame.time.Clock()
fps=60
score=0
check=True

width=600
height=727
white=(255,255,255)
high_score=open("high_score.txt","r")
highscore=high_score.read()
high_score.close()
a=int(highscore)

screen=pygame.display.set_mode((width,height))
pygame.display.set_caption("spaceman")
bg_img=pygame.image.load('back.jpg').convert_alpha()
bg_img=pygame.transform.scale(bg_img,(width,height))
spaceman_move=pygame.image.load('player.png').convert_alpha()
comet_img1=pygame.image.load('comet.png').convert_alpha()
comet_img2=pygame.image.load('comet.png').convert_alpha()
comet_img3=pygame.image.load('comet.png').convert_alpha()

font= pygame.font.SysFont('Arial', 30)
font1= pygame.font.SysFont('comic sans', 32)

def draw_font(text,font,text_col,x,y):
    img=font.render(text,True,text_col)
    screen.blit(img, (x,y))

mixer.music.play(-1) 

while check:
    
    screen.fill((0,0,0))
    draw_font("SPACEMAN",font1,white,210,200)
    draw_font("Press space to start", font, white,200,380)
    draw_font("use arrow keys to avoid getting hit by the asteroid",font,white,38,600)
    draw_font("Press x to turn off nusic and press z to turn on music",font,white,15,530)
    
    key=pygame.key.get_pressed()
    pygame.display.update()
    
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            run=False
            check=False
            pygame.quit()
            break
    
    if key[pygame.K_x]:
        mixer.music.pause()
    
    elif key[pygame.K_z]: 
        mixer.music.unpause()   

    if key[pygame.K_SPACE]:
        run=True
        break

class player():
    
    def __init__(self,x,y):
        self.img=pygame.transform.scale(spaceman_move,(45,55))
        self.width=46
        self.height=55
        self.rect=pygame.Rect(0,0,self.width,self.height)
        self.rect.center=(x,y)
        self.flip=False
    
    def draw(self):
        screen.blit(pygame.transform.flip(self.img,self.flip,False), (self.rect.x,self.rect.y))

    def move(self):
        dx=0
        dy=0
        key=pygame.key.get_pressed()
        
        if key[pygame.K_LEFT]:
            dx-=6
            self.flip=True
        
        elif key[pygame.K_RIGHT]:
            dx+=6
            self.flip=False
        
        elif key[pygame.K_UP]:
            dy-=7
        
        elif key[pygame.K_DOWN]:
            dy+=5
        
        if self.rect.left+dx<0:
            dx=-self.rect.left
        
        if self.rect.right+dx>width:
            dx=width-self.rect.right
        
        if self.rect.top+dy<0:
            dy=-self.rect.top
        
        if self.rect.bottom+dy>height:
            dy=height-self.rect.bottom
        
        self.rect.x+=dx   
        self.rect.y+=dy

spaceman=player(width//2,600)

class obstacle():
    
    def __init__(self):
        self.img1=pygame.transform.scale(comet_img1,(120,175))
        self.img2=pygame.transform.scale(comet_img2,(120,175))
        self.img3=pygame.transform.scale(comet_img3,(120,175))
        self.width=45
        self.height=70
        self.score=0
        self.close=0
        self.rect1=pygame.Rect(0,0,self.width,self.height)
        self.rect2=pygame.Rect(0,0,self.width,self.height)
        self.rect3=pygame.Rect(0,0,self.width,self.height)
        
    def position_comet1(self):
        self.rect1.x = random.randint(5, 180)
        self.rect1.y = 0
    
    def position_comet2(self):
        self.rect2.x = random.randint(201, 380)
        self.rect2.y = 0
    
    def position_comet3(self):
        self.rect3.x = random.randint(401, 570)
        self.rect3.y = 0
    
    def draw(self):
        screen.blit(self.img1,(self.rect1.x-35,self.rect1.y-70))
        self.rect1=pygame.Rect(self.rect1.x,self.rect1.y,self.width,self.height)
        
        screen.blit(self.img2,(self.rect2.x-35,self.rect2.y-70))
        self.rect2=pygame.Rect(self.rect2.x,self.rect2.y,self.width,self.height)
        
        screen.blit(self.img3,(self.rect3.x-35,self.rect3.y-70))
        self.rect3=pygame.Rect(self.rect3.x,self.rect3.y,self.width,self.height)

    def move_comet(self):

        if comet.rect1.y > height + 40:
            self.position_comet1()
            if self.close==0:
                self.score+=1
        else:
            self.rect1.y += 10
            pygame.time.wait(5)

        if comet.rect2.y > height + 40:
            self.position_comet2()
        else:
            self.rect2.y += 10
            pygame.time.wait(5)

        if comet.rect3.y > height + 40:
            self.position_comet3()
        else:
            self.rect3.y += 10
            pygame.time.wait(5)
        
    def colide(self):
        if spaceman.rect.colliderect(self.rect1):
            self.close=1
        elif spaceman.rect.colliderect(self.rect2):
            self.close=1
        elif spaceman.rect.colliderect(self.rect3):
            self.close=1

comet=obstacle()
comet.position_comet1()
comet.position_comet2()
comet.position_comet3()

pygame.time.wait(400)

while run:
    clock.tick(fps)    
    spaceman.move()
    screen.blit(bg_img,(0,0))
    spaceman.draw()
    comet.draw()
    comet.move_comet()
    comet.colide()
    
    if (comet.close == 1):
        final_score=comet.score
        if a<final_score:
            highscore=str(final_score)
            w_high_score=open("high_score.txt","w")
            w_high_score.write(highscore)
            w_high_score.close()

        while True:
            screen.fill((0,0,0))
            draw_font("Your Score= {}".format(final_score),font,white,225,190)
            draw_font("High Score= {}".format(highscore),font,white,225,240)
            draw_font("Press space to quit the game!",font,white,150,370)
            break
    
    if(comet.close ==1):
        close_key=pygame.key.get_pressed()
        if close_key[pygame.K_SPACE]:
            pygame.quit()
            break            
    
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            run=False
            break
    
    pygame.display.update()

pygame.quit()