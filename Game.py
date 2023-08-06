import pygame
import os
import random
pygame.font.init()
pygame.init()
main_font=pygame.font.SysFont("Trebuchet",50)
gameover_font=pygame.font.SysFont("Times New Roman",100)

width,height=1280,720
screen = pygame.display.set_mode((width,height))
pygame.display.set_caption("Starship Trooper")

BORDER = pygame.Rect(width - 5, 0, 10, height)
VEL=10
Bullet_vel=14
gameover=False

space=pygame.image.load(os.path.join('Assets','space.jpg'))

endBG_image=pygame.image.load(os.path.join('Assets','BG.png'))
endBG=pygame.transform.scale(endBG_image,(1280,720))

Spaceship_1_image=pygame.image.load(os.path.join('Assets','PLAYER_SPACESHIP.png'))
ship=pygame.transform.scale(Spaceship_1_image,(95,95))

laser_image=pygame.image.load(os.path.join('Assets','laser.png'))
laser=pygame.transform.scale(laser_image,(10,30))

Asteroid_1_image=pygame.image.load(os.path.join('Assets','ASTEROID_1.png'))
Asteroid_1=pygame.transform.scale(Asteroid_1_image,(80,80))

Asteroid_2_image=pygame.image.load(os.path.join('Assets','ASTEROID_2.png'))
Asteroid_2=pygame.transform.scale(Asteroid_2_image,(80,80))

Asteroid_3_image=pygame.image.load(os.path.join('Assets','ASTEROID_3.png'))
Asteroid_3=pygame.transform.scale(Asteroid_3_image,(80,80))

        
class Asteroid(object):
    def __init__(self,rank):
        self.rank=rank
        
        if self.rank==1:
            self.image=Asteroid_1
        elif self.rank==2:
            self.image=Asteroid_2
        else:
            self.image=Asteroid_3
        
        self.ranspawn=(random.randrange(50, 1170), random.randrange(0, 20)) 
        
        #(Random X and Y co-ordinate for spawning asteroids)
        self.w=80
        self.h=80
        
        self.x,self.y=self.ranspawn
        
        self.ydir=1
        self.xdir=random.choice([-1,0,1])
        
        self.yv=self.ydir * random.randrange(1,3)
        self.xv=self.xdir * 0.5
        self.mask=pygame.mask.from_surface(self.image)
        
    def draw(self,screen):
        screen.blit(self.image,(self.x, self.y))
        
def draw_window(SHIP,asteroids,bullets,lives,score):
    screen.blit(space,(0,0))
    screen.blit(ship,(SHIP.x,SHIP.y))  
    for a in asteroids:
        a.draw(screen)
    for b in bullets:
        screen.blit(laser,(b.x , b.y))
    lives_label=main_font.render(f"Lives left: {lives}",1,(204,0,102))
    screen.blit(lives_label,(10,10))
    score_label=main_font.render(f"Score: {score}",1,(255,255,255))
    screen.blit(score_label,(1100,10))
    pygame.display.update()

def draw_gameover(text):
    draw_text = gameover_font.render(text, 1, (255,0,0))
    wait_text = main_font.render('Wait for 5 seconds to restart', 1, (255,255,255))
    screen.blit(endBG,(0,0))
    screen.blit(draw_text,(330,270))
    screen.blit(wait_text,(420,390))
    pygame.display.update()
    pygame.time.delay(5000)
        
def main():
    SHIP=pygame.Rect(560,600,85,85)
    ship_mask=pygame.mask.from_surface(ship)
    clock=pygame.time.Clock()
    run=True
    
    gameover=False
    asteroids=[]
    bullets=[]
    count=0
    lives=3
    FPS=60
    score=0
    Ammo=3
    
    while run:
        clock.tick(FPS)
        count+=1
        if not gameover:
            if count % 80==0:
                    ran=random.choice([1,1,2,2,3])
                    asteroids.append(Asteroid(ran))    
            
            for a in asteroids:
                a.y+=a.yv
                offset=(a.x-SHIP.x, a.y-SHIP.y)
                crash=ship_mask.overlap(a.mask,offset)
                if crash:
                        lives -= 1
                        asteroids.pop(asteroids.index(a))
                        
                if a.y>height:
                    asteroids.pop(asteroids.index(a))
                    lives-=1
                    score-=1
                for b in bullets:
                    if (b.x >= a.x and b.x <= a.x + a.w) or b.x + b.w >= a.x and b.x + b.w <= a.x + a.w:
                        if (b.y >= a.y and b.y <= a.y + a.h) or b.y + b.h >= a.y and b.y + b.h <= a.y + a.h:
                            asteroids.pop(asteroids.index(a))
                            bullets.pop(bullets.index(b))
                            score+=1
                    if b.y < 0:
                        bullets.remove(b)
            
            for b in bullets:
                    b.y-=Bullet_vel        
            keys_pressed = pygame.key.get_pressed()
            if keys_pressed[pygame.K_a] and SHIP.x - VEL > 0:  # LEFT
                SHIP.x -= VEL
            if keys_pressed[pygame.K_d] and SHIP.x + VEL + SHIP.width < BORDER.x - 5:  # RIGHT
                SHIP.x += VEL
            if keys_pressed[pygame.K_w] and SHIP.y - VEL > height//2:  # UP
                SHIP.y -= VEL
            if keys_pressed[pygame.K_s] and SHIP.y + VEL + SHIP.height < height- 15:  # DOWN
                SHIP.y += VEL        
            
            
            for event in pygame.event.get():
                if event.type==pygame.QUIT:
                    run=False
                    pygame.quit()
                if event.type==pygame.KEYDOWN:
                    if event.key==pygame.K_SPACE and len(bullets)<Ammo:
                        bullet=pygame.Rect(SHIP.x + SHIP.width//2,SHIP.y,10,30)
                        bullets.append(bullet)
            gameover_text = ""
            if lives < 0:
                gameover_text = "GAME OVER !!"         
            if gameover_text!="":
                draw_gameover(gameover_text)
                lives=3
                score=0
        draw_window(SHIP,asteroids,bullets,lives,score)
if __name__=="__main__":
    main()