import pygame
from sys import exit

screen = pygame.display.set_mode((400,400))
pygame.display.set_caption("bullet based")
clock = pygame.time.Clock()
class player():
    def __init__(self):
        super().__init__()
        
        self.player_rect = pygame.Rect(200,200,10,10)
        self.x_speed = 0
        self.y_speed = 0
    def input(self):
        keys = pygame.key.get_pressed()        
        if keys[pygame.K_a]:
            self.x_speed -=0.6
            print("aa")
        if keys[pygame.K_d]:
            self.x_speed +=0.6
        if keys[pygame.K_w]:
            self.y_speed -=0.6
        if keys[pygame.K_s]:
            self.y_speed +=0.6
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

    def draw(self):
        pygame.draw.rect(screen,("blue"),self.player_rect)
    def update(self):
        self.input()
        self.movement()
        self.side_colisions()
        self.draw()
        print(self.player_rect)
player_class = player()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
    screen.fill(("#70a5d7"))
    
    player_class.update()

    pygame.display.update()
    clock.tick(30)