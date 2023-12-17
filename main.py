import math

import pygame
from sys import exit
from random import randint

pygame.init()

screen = pygame.display.set_mode((1200, 600))
pygame.display.set_caption("wasd based")
clock = pygame.time.Clock()
font = pygame.font.Font(None, 36)
scuffed_timer = 0

energy = 300
points = 0

energy_bar = pygame.Rect(0, -0, energy, 30)
weapon_rect = pygame.Rect(-100, -100, 50, 50)

death = False

bullets = []
enemies = []


class Player:
    
    def __init__(self):

        self.player_rect = pygame.Rect(200, 200, 10, 10)
        self.x_speed = 0
        self.y_speed = 0
        self.attacking = False
        self.attacking_frames = 0
        self.colour = "#9ac963"
        self.direction = 1

        self.bombing = False
        self.bomb_time = 0
        self.bomb_rect = pygame.Rect(0, 0, 0, 0)

    def input(self):

        global energy
        keys = pygame.key.get_pressed()

        if keys[pygame.K_d]:
            self.x_speed += 0.6
            self.direction = 3

        if keys[pygame.K_a]:
            self.x_speed -= 0.6
            self.direction = 7

        if keys[pygame.K_s]:
            self.y_speed += 0.6
            if self.direction == 3:
                self.direction = 4
            elif self.direction == 7:
                self.direction = 6
            else:
                self.direction = 5

        if keys[pygame.K_w]:
            self.y_speed -= 0.6
            if self.direction == 3:
                self.direction = 2
            elif self.direction == 7:
                self.direction = 8
            else:
                self.direction = 1

        if keys[pygame.K_RSHIFT] and not self.attacking:
            self.attacking = True

        if keys[pygame.K_SLASH] and energy >= 400 and not self.bombing:
            self.bombing = True
            energy -= 400

        # adding bullets is in the event menu

    def side_colisions(self):

        if self.player_rect.right > 1200:
            self.player_rect.right = 1200
            self.x_speed = 0
        if self.player_rect.left < 0:
            self.player_rect.left = 0
            self.x_speed = 0
        if self.player_rect.bottom > 600:
            self.player_rect.bottom = 600
            self.y_speed = 0
        if self.player_rect.top < 0:
            self.player_rect.top = 0
            self.y_speed = 0

    def movement(self):

        self.player_rect.x += self.x_speed
        self.player_rect.y += self.y_speed

        if self.x_speed > 0: self.x_speed -= 0.2
        if self.y_speed > 0: self.y_speed -= 0.2
        if self.x_speed < 0: self.x_speed += 0.2
        if self.y_speed < 0: self.y_speed += 0.2

    def weapon_logic(self):

        global weapon_rect

        if self.attacking:
            self.attacking_frames += 1

        if self.attacking and self.attacking_frames <= 40:
            if self.direction == 1:
                weapon_rect.midbottom = self.player_rect.midtop
            elif self.direction == 2:
                weapon_rect.bottomleft = self.player_rect.topright
            elif self.direction == 3:
                weapon_rect.midleft = self.player_rect.midright
            elif self.direction == 4:
                weapon_rect.topleft = self.player_rect.bottomright
            elif self.direction == 5:
                weapon_rect.midtop = self.player_rect.midbottom
            elif self.direction == 6:
                weapon_rect.topright = self.player_rect.bottomleft
            elif self.direction == 7:
                weapon_rect.midright = self.player_rect.midleft
            elif self.direction == 8:
                weapon_rect.bottomright = self.player_rect.topleft

            self.colour = "#cde4b1"

        else:

            weapon_rect.center = -200, -200

            if self.attacking_frames >= 45:
                self.attacking_frames = 0
                self.colour = "#9ac963"
                self.attacking = False

        if self.bombing:

            if self.bomb_time == 0:
                self.bomb_pos = self.player_rect.center

            self.bomb_time += 1
            self.bomb_rect.size = (self.bomb_time, self.bomb_time)
            self.bomb_rect.center = self.bomb_pos

            if self.bomb_time >= 275:
                self.bombing = False
                self.bomb_time = 0

            for e in enemies:
                if collidebomb(e.rect, self.bomb_rect, self.bomb_time):
                    enemies.remove(e)
                    points_distribution(e.type)

            pygame.draw.circle(screen, "blue", self.bomb_rect.center, self.bomb_time, 2)

    def draw(self):
        pygame.draw.rect(screen, self.colour, self.player_rect)
        if self.attacking:
            pygame.draw.rect(screen, "orange", weapon_rect)

    def update(self):
        self.input()
        self.movement()
        self.side_colisions()
        self.weapon_logic()
        self.draw()


player = Player()


class Enemy:

    def __init__(self, type_: int, pos):
        # base
        self.type = type_

        if self.type == 1:

            self.speed = 5
            self.radius = 20

            img_1 = pygame.transform.scale(pygame.image.load("graphics/slimes/slime_1.png").convert_alpha(), (50, 50))
            img_2 = pygame.transform.scale(pygame.image.load("graphics/slimes/slime_2.png").convert_alpha(), (50, 50))
            self.normal_frames = [img_1, img_2]
            self.flipped_frames = [pygame.transform.flip(img_1, True, False), pygame.transform.flip(img_2, True, False)]
            self.frames = self.normal_frames
            self.img = self.frames[0]

        # fast
        if self.type == 2:

            self.speed = 7

            img_1 = pygame.transform.scale(pygame.image.load("graphics/fast slime/1.png").convert_alpha(), (60, 60))
            img_2 = pygame.transform.scale(pygame.image.load("graphics/fast slime/2.png").convert_alpha(), (60, 60))

            self.normal_frames = [img_1, img_2]
            self.flipped_frames = [pygame.transform.flip(img_1, True, False), pygame.transform.flip(img_2, True, False)]
            self.frames = self.normal_frames
            self.img = self.frames[0]
            self.radius = 12

        # big
        if self.type == 3:

            self.speed = 3
            self.radius = 40
            # big_slime created by Hugo on GitHub
            img_1 = pygame.transform.scale(pygame.image.load("graphics/big_slime.png").convert_alpha(), (80, 80))

            self.normal_frames = [img_1]
            self.flipped_frames = [pygame.transform.flip(img_1, True, False)]

            self.frames = self.normal_frames
            self.img = self.frames[0]

        self.frame = 0
        self.rect = self.img.get_rect()
        self.rect.center = pos

    def movement(self):
        self.pos_to_player()
        if self.y_delta > 0:
            self.rect.y += self.y_speed
            self.frames = self.normal_frames
        else:
            self.rect.y -= self.y_speed
            self.frames = self.flipped_frames
        if self.x_delta > 0:
            self.rect.x += self.x_speed
            self.frames = self.normal_frames
        else:
            self.rect.x -= self.x_speed
            self.frames = self.flipped_frames

    def pos_to_player(self):

        self.y_delta = player.player_rect.centery - self.rect.centery
        self.x_delta = player.player_rect.centerx - self.rect.centerx

        abs_x = abs(self.x_delta)
        abs_y = abs(self.y_delta)

        if abs_x == 0: abs_x = 0.1
        if abs_y == 0: abs_y = 0.1

        if abs_x >= abs_y:
            factor = abs_y / abs_x
            self.y_speed = self.speed * factor
            self.x_speed = self.speed - self.y_speed

        if abs_y > abs_x:
            factor = abs_x / abs_y
            self.x_speed = self.speed * factor
            self.y_speed = self.speed - self.x_speed

    def collision(self):
        global death

        if self.rect.colliderect(player.player_rect):
            death = True

        if self.rect.colliderect(weapon_rect):
            points_distribution(self.type)
            return True
        else:
            return False

    def draw(self):
        screen.blit(self.img, self.rect)

    def animation(self):
        self.frame += 0.1
        if self.frame >= len(self.frames):
            self.frame = 0
        self.img = self.frames[int(self.frame)]

    def update(self):

        self.movement()
        # self.colision()
        self.draw()
        self.animation()


def create_enemy():
    random = randint(1, 6)
    pos = [0, 0]

    if randint(1, 2) == 1:
        pos[0] = randint(0, 1200)
        if randint(1, 2) == 1:
            pos[1] = 0
        else:
            pos[1] = 600
    else:
        pos[1] = randint(0, 600)
        if randint(1, 2) == 1:
            pos[0] = 0
        else:
            pos[0] = 1200

    enemy = 1
    if random == 1:
        enemy = 2
    elif random == 2:
        enemy = 3
    enemies.append(Enemy(enemy, tuple(pos)))


class Bullet:

    def __init__(self, direction):

        self.diagonal = False

        angle = None

        if direction == 1 or direction == 5:
            angle = 90
        elif direction == 2 or direction == 6:
            angle = 45
            self.diagonal = True
        elif direction == 3 or direction == 7:
            angle = 0
        elif direction == 4 or direction == 8:
            angle = 135
            self.diagonal = True

        if self.diagonal:
            self.hitbox_1 = pygame.Rect(0, 0, 40, 40)
            self.hitbox_2 = pygame.Rect(0, 0, 40, 40)

        img = pygame.image.load("graphics/laser.png").convert_alpha()
        self.img = pygame.transform.rotozoom(img, angle, 0.5)

        self.rect = self.img.get_rect()
        self.direction = direction
        self.rect.center = player.player_rect.center

    def movement(self):
        if self.direction == 1: self.rect.y -= 20
        if self.direction == 2:
            self.rect.x += 10
            self.rect.y -= 10
            self.hitbox_1.topright = self.rect.topright
            self.hitbox_2.bottomleft = self.rect.bottomleft
        if self.direction == 3: self.rect.x += 20
        if self.direction == 4:
            self.rect.x += 10
            self.rect.y += 10
            self.hitbox_1.topleft = self.rect.topleft
            self.hitbox_2.bottomright = self.rect.bottomright
        if self.direction == 5: self.rect.y += 20
        if self.direction == 6:
            self.rect.x -= 10
            self.rect.y += 10
            self.hitbox_1.topright = self.rect.topright
            self.hitbox_2.bottomleft = self.rect.bottomleft
        if self.direction == 7: self.rect.x -= 20
        if self.direction == 8:
            self.rect.x -= 10
            self.rect.y -= 10
            self.hitbox_1.topleft = self.rect.topleft
            self.hitbox_2.bottomright = self.rect.bottomright

    def update(self):
        self.movement()

        screen.blit(self.img, self.rect)

    def collision(self, enemy):

        if self.rect.colliderect(enemy.rect):
            return True
        else:
            return False

    def offscreen(self) -> bool:
        if self.rect.left > 1250:
            return True
        elif self.rect.right < -50:
            return True
        elif self.rect.top < -50:
            return True
        elif self.rect.bottom > 650:
            return True
        else:
            return False


def energy_logic():
    global energy
    colour = "#824464"
    if energy < 300:
        energy += 1
    if energy >= 400:
        colour = "#447d82"
    energy_bar.width = energy
    energy_bar.bottomright = (1180, 580)
    pygame.draw.rect(screen, colour, energy_bar, 7, 8)


def points_distribution(sort: int):

    global points

    if sort == 1:
        points += 1
    elif sort == 2:
        points += 3
    elif sort == 3:
        points += 2

def collidebomb(rect: pygame.Rect, circle: pygame.Rect, radius):

    dist = math.sqrt((rect.centerx - circle.centerx) ** 2 + (rect.centery - circle.centery) ** 2)
    return dist < rect.width / 2 + radius

while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if event.type == pygame.KEYDOWN:
            if not death:
                if event.key == pygame.K_RETURN and energy >= 25:
                    bullets.append(Bullet(player.direction))
                    energy -= 50
            if death:
                if event.key == pygame.K_SPACE:
                    death = False
                    points = 0
    if not death:
        screen.fill("#597439")
        scuffed_timer += 1

        if scuffed_timer == 20:
            create_enemy()
            scuffed_timer = 0

        player.update()

        for e in enemies:
            e.update()
            # sword colision
            if e.collision():
                enemies.remove(e)
                energy += 15

        for b in bullets:
            b.update()
            if b.offscreen():
                bullets.remove(b)
            else:
                for e in enemies:
                    if b.collision(e):
                        points_distribution(e.type)
                        enemies.remove(e)

        energy_logic()

    if death:
        screen.fill("#0d8779")

        enemies = []
        bullets = []

        player.attacking = False
        player.attacking_frames = 0

        text = font.render("press space", True, "black")
        BLuk = text.get_rect(midtop=(600, 450))
        screen.blit(text, BLuk)

    # outside of death
    text = font.render(str(points), True, "black")
    BLuk = text.get_rect(midtop=(600, 50))
    screen.blit(text, BLuk)

    pygame.display.update()
    clock.tick(30)
