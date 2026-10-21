
import face_recognition
import pygame
import pytmx
from pytmx.util_pygame import load_pygame
pygame.init()
screen = pygame.display.set_mode((1000, 800))
clock = pygame.time.Clock()
run = True
tmx_data = load_pygame("map.tmx")
player_sprite = pygame.image.load('player.png')
ti = tmx_data.get_tile_image_by_gid
keys = pygame.key.get_pressed()
def get_world_offset(player,screen_width,screen_height):
    world_offset_x = player.x - (screen_width/2)
    world_offset_y = player.y - (screen_height/2)
    return world_offset_x, world_offset_y
def draw_map(screen,tmx_data,world_offset):
    for layer in tmx_data.visible_layers:
        if isinstance(layer, pytmx.TiledTileLayer):
            for x ,y , gid in layer:
                tile = ti(gid)
                if tile:
                    screen.blit(tile, (x * tmx_data.tilewidth - world_offset[0], y * tmx_data.tileheight - world_offset[1]))



class Player:
    def __init__(self,x,y,width,height,player_sprite,scale_factor,screen):
        self.image = player_sprite
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
        self.scale_factor = scale_factor
        self.image = pygame.transform.scale(self.image, (int(self.width * self.scale_factor), int(self.height * self.scale_factor)))
        self.screen = screen

    def draw(self):
        self.screen.blit(self.image, (self.x - world_offset[0], self.y - world_offset[1]))
        return

    def charge_jump(self):
        if self.is_ground == True:
            if keys[pygame.K_SPACE]:
                self.hold_jump = True
                self.charge += 0.2
                if self.charge > self.max_charge:
                    self.charge = self.max_charge
                if keys[pygame.K_a]:
                    self.angle -= 1
                    if self.angle < self.min_angle:
                        self.angle = self.min_angle
                if keys[pygame.K_d]:
                    self.angle += 1
                    if self.angle > self.max_angle:
                        self.angle = self.max_angle
    def release_jump(self):
        if self.is_ground == True:
            if self.hold_jump == True:
                self.hold_jump = False
                if not keys[pygame.K_SPACE]:
                    self.y_velocity = -self.charge * 0.5
                    self.x_velocity = self.charge * 0.5 * (self.angle / 90)
                    self.is_ground = False
                    self.charge = 0
                    self.angle = 0           

    def apply_gravity(self):
        if not self.is_ground:
            self.y_velocity += self.gravity
            self.y += self.y_velocity
            self.x += self.x_velocity

    def update(self):
        self.apply_gravity()
        self.charge_jump()
        self.release_jump()
        self.draw()
        return
player = Player(100, 100, 50, 50, player_sprite, 1, screen)
world_offset = get_world_offset(player,screen.get_width(),screen.get_height())
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        player.update()
    screen.fill((255, 255, 255))
    pygame.display.update()
    clock.tick(60)