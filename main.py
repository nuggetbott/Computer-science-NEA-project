

import pygame
pygame.init()
screen = pygame.display.set_mode((1000, 800))
clock = pygame.time.Clock()
run = True

player_sprite = pygame.image.load('player.png')
class player:
    def __init__(self,x,y,width,height,img_path,scale_factor):
        self.x = x
        self.y = y
        self.y_velocity =0
        self.x_velocity = 0
        self.width = width
        self.height = height
        self.is_ground = True
        self.jump_velocity = 0
        self.hold_jump = False
        self.gravity = 1
        self.charge = 0
        self.max_charge = 100
        self.angle = 0 
        self.min_angle = -80
        self.max_angle = 80
        self.character = img_path
        self.scale_factor = scale_factor

    def draw(self,screen):
        

while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    screen.fill((255, 255, 255))
    pygame.display.update()
    clock.tick(60)