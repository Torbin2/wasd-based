import pygame
from sys import exit

screen = pygame.display.set_mode((400,400))
pygame.display.set_caption("bullet based")
clock = pygame.time.Clock()

weopon_rect = pygame.Rect(-100,-100,50,50)

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


        if keys[pygame.K_RSHIFT] and self.atacking_frames <=20:
            self.atacking = True
    def side_colisions(self):
        if self.player_rect.right > 400:
            self.player_rect.right = 400
            self.x_speed =0
        if self.player_rect.left < 0:
            self.player_rect.left = 0
            self.x_speed =0
        if self.player_rect.bottom > 400:
            self.player_rect.bottom = 400
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
        if self.atacking and self.atacking_frames <= 20:
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
            weopon_rect.center = -100,-100
            if self.atacking_frames >= 60:
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
class enemy():
    def __init__(self, type):
        self.rect = pygame.Rect(0,0,200,200)
        self.radius = 10
        if type == "basic":
            self.speed = 5
            self.colour = ("#395974")
        if type == "speedy":
            self.speed = 10
            self.colour = ("#743959")

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
    def draw(self):
        pygame.draw.circle(screen,self.colour,self.rect.center,self.radius)   
    def update(self):
        self.movement()
        self.draw()


enemy_1 = enemy("basic")
enemy_2 = enemy("speedy")

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
    screen.fill(("#597439"))
    enemy_1.update()
    enemy_2.update()
    player_class.update()

    pygame.display.update()
    clock.tick(30)