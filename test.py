import pygame
import os
import random
pygame.font.init()
pygame.init()
main_font=pygame.font.SysFont("Trebuchet",50)

ASTEROID_HIT=pygame.USEREVENT+1

width,height=1280,720
screen = pygame.display.set_mode((width,height))
pygame.display.set_caption("Game")

BORDER = pygame.Rect(width - 5, 0, 10, height)
VEL=10
Bullet_vel=14


space=pygame.image.load(os.path.join('Assets','space.jpg'))

Spaceship_1_image=pygame.image.load(os.path.join('Assets','PLAYER_SPACESHIP.png'))
ship=pygame.transform.scale(Spaceship_1_image,(95,95))

laser_image=pygame.image.load(os.path.join('Assets','laser.png'))
laser=pygame.transform.scale(laser_image,(10,5))

Asteroid_1_image=pygame.image.load(os.path.join('Assets','ASTEROID_1.png'))
Asteroid_1=pygame.transform.scale(Asteroid_1_image,(80,80))

Asteroid_2_image=pygame.image.load(os.path.join('Assets','ASTEROID_2.png'))
Asteroid_2=pygame.transform.scale(Asteroid_2_image,(80,80))

Asteroid_3_image=pygame.image.load(os.path.join('Assets','ASTEROID_3.png'))
Asteroid_3=pygame.transform.scale(Asteroid_3_image,(80,80))


'''def blue_movement(keys_pressed,blue):
    if keys_pressed[pygame.K_a] and blue.x >=20:  
            blue.x -= VEL
    if keys_pressed[pygame.K_d] and blue.x <=1170:
            blue.x += VEL
    if keys_pressed[pygame.K_w] and blue.y >=100:  
            blue.y -= VEL
    if keys_pressed[pygame.K_s] and blue.y <=610:  
            blue.y += VEL'''

        
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
    
    def draw(self,screen):
        screen.blit(self.image,(self.x, self.y))
        
def handle_bullets(bullets,SHIP,asteroids):
    for bullet in bullets:
        bullet.y -= Bullet_vel
        for asteroid in asteroids:
            if asteroid.colliderect(bullet):
                pygame.event.post(pygame.event.Event(ASTEROID_HIT))
                bullets.remove(bullet)
                #asteroids.remove(asteroid)
      
        
def draw_window(SHIP,asteroids,bullets,lives):
    screen.blit(space,(0,0))
    screen.blit(ship,(SHIP.x,SHIP.y))
    lives_label=main_font.render(f"Lives: {lives}",1,(255,255,255))
    screen.blit(lives_label,(10,10))  
    for a in asteroids:
        a.draw(screen)
    for bullet in bullets:
        screen.blit(laser,(bullet.x , bullet.y))
    pygame.display.update()


def main():
    SHIP=pygame.Rect(560,600,95,95)
    clock=pygame.time.Clock()
    run=True
    
    gameover=False
    asteroids=[]
    bullets=[]
    count=0
    
    lives=3
    FPS=60
   
    while run:
        clock.tick(FPS)
        count+=1
        if not gameover:
            if count % 80==0:
                    ran=random.choice([1,1,2,2,3])
                    asteroids.append(Asteroid(ran))    
            
            for a in asteroids:
                a.y+=a.yv
                if (a.x >= SHIP.x - SHIP.w//2 and a.x <= SHIP.x + SHIP.w//2) or (a.x + a.w <= SHIP.x + SHIP.w//2 and a.x + a.w >= SHIP.x - SHIP.w//2):
                    if(a.y >= SHIP.y - SHIP.h//2 and a.y <= SHIP.y + SHIP.h//2) or (a.y  +a.h >= SHIP.y - SHIP.h//2 and a.y + a.h <= SHIP.y + SHIP.h//2):
                        lives -= 1
                        asteroids.pop(asteroids.index(a))
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
                    if event.key==pygame.K_SPACE:
                        bullet=pygame.Rect(SHIP.x + SHIP.width//2,SHIP.y,10,5)
                        bullets.append(bullet)
                    
        handle_bullets(bullets,SHIP,asteroids)
        draw_window(SHIP,asteroids,bullets,lives)
    pygame.quit()
if __name__=="__main__":
    main()