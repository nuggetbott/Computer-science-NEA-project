
import face_recognition
import pygame
import pytmx
from pytmx.util_pygame import load_pygame
pygame.init()
screen = pygame.display.set_mode((1000, 800))
clock = pygame.time.Clock()
run = True
tmx_data = load_pygame("map.tmx")
ti = tmx_data.get_tile_image_by_gid

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

world_offset = get_world_offset(player,screen.get_width(),screen.get_height())

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
        return

while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    screen.fill((255, 255, 255))
    pygame.display.update()
    clock.tick(60)