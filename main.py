import pygame, sys, os, random
from button import Button

pygame.init()
main_font=pygame.font.SysFont("Trebuchet",50)
SCREEN = pygame.display.set_mode((1280, 720))
gameover_font=pygame.font.SysFont("Times New Roman",100)
pygame.display.set_caption("STARSHIP TROOPER")

WIDTH, HEIGHT = 1280, 720
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
BORDER = pygame.Rect(WIDTH - 5, 0, 10, HEIGHT)
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
BG = pygame.image.load("assets/background.jpg")

def get_font(size): # Returns Press-Start-2P in the desired size
    return pygame.font.Font("assets/font.ttf", size)

def play():
    while True:
        VEL=10
        Bullet_vel=14
        level=0
        space=pygame.image.load(os.path.join('Assets','space.jpg'))
        
        half_image=pygame.image.load(os.path.join('Assets','0.5.png'))
        half=pygame.transform.scale(half_image,(40,40))
        
        full_image=pygame.image.load(os.path.join('Assets','1.png'))
        full=pygame.transform.scale(full_image,(40,40))
        
        mt_image=pygame.image.load(os.path.join('Assets','0.png'))
        mt=pygame.transform.scale(mt_image,(40,40))
        
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
        
                self.ranspawn=(random.randrange(50, 1170), random.randrange(-500,-200)) 
                
                #(Random X and Y co-ordinate for spawning asteroids)
                self.w=80
                self.h=80
                
                self.x,self.y=self.ranspawn
                
                self.ydir=1
                self.xdir=random.choice([-1,0,1])
                
                self.yv=self.ydir * random.randrange(2,3)
                self.xv=self.xdir * 0.5
                self.mask=pygame.mask.from_surface(self.image)
                
            def draw(self,WIN):
                WIN.blit(self.image,(self.x, self.y))
        
        def draw_window(SHIP,asteroids,bullets,lives,score,level):
            WIN.blit(space,(0,0))
            WIN.blit(ship,(SHIP.x,SHIP.y))  
            for a in asteroids:
                a.draw(WIN)
            for b in bullets:
                WIN.blit(laser,(b.x , b.y))
            
            #lives_label=main_font.render(f"Lives left: {lives}",1,(204,0,102))
            level_label=main_font.render(f"Level: {level}",1,(204,0,102))
            #WIN.blit(lives_label,(10,10))
            WIN.blit(level_label,(10,50))
            score_label=main_font.render(f"Score: {score}",1,(0,255,255))
            WIN.blit(score_label,(1100,10))
            #WIN.blit(half,(50,10))
            if lives==3:
                WIN.blit(full,(10,10))
                WIN.blit(full,(50,10))
                WIN.blit(full,(90,10))
            elif lives==2.5:
                WIN.blit(full,(10,10))
                WIN.blit(full,(50,10))
                WIN.blit(half,(90,10))
            elif lives==2:
                WIN.blit(full,(10,10))
                WIN.blit(full,(50,10))
                WIN.blit(mt,(90,10))
            elif lives==1.5:
                WIN.blit(full,(10,10))
                WIN.blit(half,(50,10))
                WIN.blit(mt,(90,10))
            elif lives==1:
                WIN.blit(full,(10,10))
                WIN.blit(mt,(50,10))
                WIN.blit(mt,(90,10))
            elif lives==0.5:
                WIN.blit(half,(10,10))
                WIN.blit(mt,(50,10))
                WIN.blit(mt,(90,10))
            elif lives==0:
                WIN.blit(mt,(10,10))
                WIN.blit(mt,(50,10))
                WIN.blit(mt,(90,10))
                
            pygame.display.update()

        def draw_gameover(text):
            draw_text = gameover_font.render(text, 1, (255,0,0))
            wait_text = main_font.render('Wait for 5 seconds to restart', 1, (255,255,255))
            WIN.blit(endBG,(0,0))
            WIN.blit(draw_text,(330,270))
            WIN.blit(wait_text,(420,390))
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
            level=0
            lives=3
            FPS=60
            score=0
            Ammo=3
            wave=0
            speed=0
            
            while run:
                clock.tick(FPS)
                count+=1
                if not gameover:
                    if len(asteroids)==0:
                        level+=1
                        wave+=1
                        speed+=0.2
                        for i in range(wave):
                            ran=random.choice([1,1,2,2,3])
                            asteroids.append(Asteroid(ran))
                            
                    
                    for a in asteroids:
                        v=a.yv+speed
                        a.y+=v
                        #a.x+=a.xv
                        offset=(a.x-SHIP.x, a.y-SHIP.y)
                        crash=ship_mask.overlap(a.mask,offset)
                        if crash:
                                lives -= 0.5
                                asteroids.pop(asteroids.index(a))
                                
                        if a.y>HEIGHT:
                            a.x=random.randrange(50, 1170)
                            a.y=random.randrange(-500,-200)
                            lives-=0.5
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
                    if keys_pressed[pygame.K_w] and SHIP.y - VEL > HEIGHT//2:  # UP
                        SHIP.y -= VEL
                    if keys_pressed[pygame.K_s] and SHIP.y + VEL + SHIP.height < HEIGHT- 15:  # DOWN
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
                    if lives < 0.5:
                        gameover_text = "GAME OVER !!"         
                    if gameover_text!="":
                        draw_gameover(gameover_text)                   
                        lives=3
                        score=0
                draw_window(SHIP,asteroids,bullets,lives,score,level)
        if __name__=="__main__":
            main()

        pygame.display.update()

def main_menu():
    while True:
        SCREEN.blit(BG, (0, 0))

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        MENU_TEXT = get_font(70).render("STARSHIP TROPPER", True, "#b68f40")
        MENU_RECT = MENU_TEXT.get_rect(center=(640, 100))

        PLAY_BUTTON = Button(image=pygame.image.load("assets/Play Rect.png"), pos=(440, 450), 
                            text_input="PLAY", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        
        QUIT_BUTTON = Button(image=pygame.image.load("assets/Quit Rect.png"), pos=(840, 450), 
                            text_input="QUIT", font=get_font(75), base_color="#d7fcd4", hovering_color="White")

        SCREEN.blit(MENU_TEXT, MENU_RECT)

        for button in [PLAY_BUTTON,  QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(SCREEN)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    play()
                
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()

main_menu()