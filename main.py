import pygame
from sys import exit
from random import randint

pygame.init()

screen = pygame.display.set_mode((1200,600))
pygame.display.set_caption("bullet based")
clock = pygame.time.Clock()
font = pygame.font.Font(None, 36)
scuffed_timer = 0

energie = 300
points = 0

energie_bar =pygame.Rect(0,-0,energie,30)
weopon_rect = pygame.Rect(-100,-100,50,50)

death = False

bullets = []
enemies = []


class player():
    def __init__(self):
        self.player_rect = pygame.Rect(200,200,10,10)
        self.x_speed = 0
        self.y_speed = 0
        self.atacking = False
        self.atacking_frames =0
        self.colour = ("#9ac963")
        self.direction = 1
    def input(self):
        keys = pygame.key.get_pressed()        
     
        if keys[pygame.K_d]:
            self.x_speed +=0.6
            self.direction=3
        if keys[pygame.K_a]:
            self.x_speed -=0.6
            self.direction = 7
        if keys[pygame.K_s]:
            self.y_speed +=0.6
            if self.direction == 3:self.direction = 4
            elif self.direction == 7:self.direction = 6
            else:self.direction=5
        if keys[pygame.K_w]:
            self.y_speed -=0.6
            if self.direction == 3:self.direction = 2
            elif self.direction == 7:self.direction = 8
            else:self.direction=1

        if keys[pygame.K_RSHIFT] and not self.atacking:
            self.atacking = True

        #adding bullets is in the event menu
        
    
    def side_colisions(self):
        if self.player_rect.right > 1200:
            self.player_rect.right = 1200
            self.x_speed =0
        if self.player_rect.left < 0:
            self.player_rect.left = 0
            self.x_speed =0
        if self.player_rect.bottom > 600:
            self.player_rect.bottom = 600
            self.y_speed = 0
        if self.player_rect.top < 0:
            self.player_rect.top = 0 
            self.y_speed = 0
    
    def movement(self):
        self.player_rect.x += self.x_speed
        self.player_rect.y += self.y_speed
        if self.x_speed >0: self.x_speed -=0.2
        if self.y_speed >0: self.y_speed -=0.2
        if self.x_speed <0: self.x_speed +=0.2
        if self.y_speed <0: self.y_speed +=0.2
    def weopon_logic(self):
        global weopon_rect
        if self.atacking:
            self.atacking_frames +=1    
        if self.atacking and self.atacking_frames <= 40:
            if self.direction == 1:
                weopon_rect.midbottom = self.player_rect.midtop
            elif self.direction == 2:
                weopon_rect.bottomleft = self.player_rect.topright
            elif self.direction == 3:
                weopon_rect.midleft = self.player_rect.midright
            elif self.direction == 4:
                weopon_rect.topleft = self.player_rect.bottomright
            elif self.direction == 5:
                weopon_rect.midtop == self.player_rect.midbottom
            elif self.direction == 6:
                weopon_rect.topright == self.player_rect.bottomleft
            elif self.direction == 7:
                weopon_rect.midright = self.player_rect.midleft
            elif self.direction == 8:
                weopon_rect.bottomright = self.player_rect.topleft
            
            self.colour =("#cde4b1")
        else: 
            weopon_rect.center = -200,-200
            if self.atacking_frames >= 45:
                self.atacking_frames = 0
                self.colour = ("#9ac963")
                self.atacking = False           
    def draw(self):
        pygame.draw.rect(screen,self.colour,self.player_rect)
        if self.atacking:
            pygame.draw.rect(screen,("orange"),weopon_rect)
    def update(self):
        self.input()
        self.movement()
        self.side_colisions()
        self.weopon_logic()
        self.draw()

player_class = player()

class Enemy():
    def __init__(self, type, pos):
        #base
        self.type = type
        if type == 1:
            self.speed = 5
            self.colour = ("#395974")
            self.radius = 10
        #fast
        if type == 2:
            self.speed = 10
            self.colour = ("#743959")
            self.radius = 12
        #big
        if type == 3:
            self.speed = 3
            self.colour = ("#395974")
            self.radius = 20

        self.rect = pygame.Rect(0, 0, self.radius*2, self.radius*2)
        self.rect.center = pos

    def movement(self):
        self.pos_to_player()
        if self.y_delta >0: self.rect.y += self.y_speed
        else: self.rect.y -= self.y_speed
        if self.x_delta >0: self.rect.x += self.x_speed
        else: self.rect.x -= self.x_speed
    
    def pos_to_player(self):
        self.y_delta = player_class.player_rect.centery - self.rect.centery
        self.x_delta = player_class.player_rect.centerx - self.rect.centerx
        
        abs_x = abs(self.x_delta)
        abs_y = abs(self.y_delta)
        if abs_x == 0: abs_x = 0.1
        if abs_y == 0: abs_y = 0.1
        
        if abs_x >= abs_y:
            factor = abs_y/abs_x
            self.y_speed = self.speed *factor
            self.x_speed = self.speed - self.y_speed
        if abs_y > abs_x:
            factor = abs_x/abs_y
            self.x_speed = self.speed *factor
            self.y_speed = self.speed - self.x_speed

    def colision(self):
        global death
        if self.rect.colliderect(player_class.player_rect):
            death = True
        
        if self.rect.colliderect(weopon_rect):
            points_distrubution(self.type)
            return True
        else: return False
                   
    def draw(self):
        pygame.draw.circle(screen,self.colour,self.rect.center,self.radius)   
    def update(self):
        self.movement()
        #self.colision()
        self.draw()

def create_enemy():
    random = randint(1,4)
    pos =[0,0]
    
    if randint(1,2) == 1:
        pos[0] = randint(0,1200)
        if randint(1,2) == 1:
            pos[1] = 0
        else: pos[1] =600
    else:
        pos[1] = randint(0,600)
        if randint(1,2) == 1:
            pos[0] = 0
        else: pos[0] = 1200

    enemy = 1
    if random == 1: enemy = 2
    elif random == 2: enemy =3
    enemies.append(Enemy(enemy,tuple(pos)))

class Bullet():
    def __init__(self, direction):
        self.diagonal = False
        if direction == 1 or direction ==5: angle = 90
        elif direction == 2 or direction ==6:
            angle = 45
            self.diagonal = True
        elif direction == 3 or direction ==7: angle = 0
        elif direction == 4 or direction ==8:
            angle = 135
            self.diagonal = True
        
        if self.diagonal:
            self.hitbox_1 = pygame.Rect(0,0,55,40)
            self.hitbox_2 = pygame.Rect(0,0,55,40)


        img = pygame.image.load("graphics/laser.png").convert_alpha()
        self.img = pygame.transform.rotozoom(img,angle,0.5)

        self.rect = self.img.get_rect()
        self.direction = direction
        self.rect.center = player_class.player_rect.center
    def movement(self):
        if self.direction == 1:self.rect.y-=20
        if self.direction == 2:
            self.rect.x+=10
            self.rect.y-=10
            self.hitbox_1.topright = self.rect.topright
            self.hitbox_2.bottomleft = self.rect.bottomleft
        if self.direction == 3:self.rect.x+=20
        if self.direction == 4:
            self.rect.x+=10
            self.rect.y+=10
            self.hitbox_1.topleft = self.rect.topleft
            self.hitbox_2.bottomright = self.rect.bottomright
        if self.direction == 5:self.rect.y+=20
        if self.direction == 6:
            self.rect.x-=10
            self.rect.y+=10
            self.hitbox_1.topright = self.rect.topright
            self.hitbox_2.bottomleft = self.rect.bottomleft
        if self.direction == 7:self.rect.x-=20
        if self.direction == 8:
            self.rect.x-=10
            self.rect.y-=10
            self.hitbox_1.topleft = self.rect.topleft
            self.hitbox_2.bottomright = self.rect.bottomright
    def update(self):
        self.movement()

        screen.blit(self.img,self.rect)
    
    def colison(self,enemy):
        
        if self.rect.colliderect(enemy.rect):
            return True
        else: return False
    def offscreen(self) -> bool:
        if self.rect.left > 1250:return True
        elif self.rect.right < -50: return True
        elif self.rect.top < -50: return True
        elif self.rect.bottom > 650: return True
        else: return False
     
def energie_logic():
    global energie
    if energie <300:
        energie +=1
    energie_bar.width = energie
    energie_bar.bottomright = (1180,580)
    pygame.draw.rect(screen,("#824464"),energie_bar,7,8)

def points_distrubution(sort):
    global points
    if sort== 1:
        points+=1
    elif sort== 2:
        points+=3
    elif sort==3:
        points +=2

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
    
        if event.type == pygame.KEYDOWN:
            if not death:
                if event.key == pygame.K_RETURN and energie >= 25:
                    bullets.append(Bullet(player_class.direction))
                    energie -= 50
            if death:
                if event.key == pygame.K_SPACE:
                    death = False
                    points = 0
    if not death: 
        screen.fill(("#597439"))
        scuffed_timer +=1
        
        if scuffed_timer == 30:
            create_enemy()
            scuffed_timer = 0
        
        player_class.update()
        
        for e in enemies:
            e.update()
            #sword colision
            if e.colision()== True:
                enemies.remove(e)
                energie+=15
        
        for b in bullets:
            b.update()
            if b.offscreen():
                bullets.remove(b)
            else:
                for e in enemies:
                    if b.colison(e):
                        points_distrubution(e.type)
                        enemies.remove(e)
        
        energie_logic()
    
    
    if death:
        screen.fill("#0d8779")
        
        enemies = []
        bullets = []

        text = font.render("press space",True, ("black"))
        BLuk = text.get_rect(midtop= (600,450))
        screen.blit(text,BLuk)
    
    #outside of death
    text = font.render(str(points),True, ("black"))
    BLuk = text.get_rect(midtop= (600,50))
    screen.blit(text, BLuk)

    pygame.display.update()
    clock.tick(30)