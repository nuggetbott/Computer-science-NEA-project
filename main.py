# import face_recongition
import pygame
import pytmx
from pytmx.util_pygame import load_pygame

pygame.init()
tile_size = 80
Columns = 17
Rows = 9
scaled_tiles = {}
screen = pygame.display.set_mode((Columns * tile_size, Rows * tile_size))
clock = pygame.time.Clock()
run = True
tmx_data = load_pygame("maps/testmap.tmx")
player_sprite = pygame.image.load("pixel_art/player.png")
ti = tmx_data.get_tile_image_by_gid

keys = pygame.key.get_pressed()


def get_world_offset(player, screen_width, screen_height):
    map_width = tmx_data.width * tile_size
    map_height = tmx_data.height * tile_size

    world_offset_x = player.x + player.width / 2 - screen_width / 2
    world_offset_y = player.y + player.height / 2 - screen_height / 2 - 160

    if map_width > screen_width:
        world_offset_x = max(0, min(world_offset_x, map_width - screen_width))
    if map_height > screen_height:
        world_offset_y = max(0, min(world_offset_y, map_height - screen_height))

    return world_offset_x, world_offset_y


def draw_map(screen, tmx_data, world_offset):
    for layer in tmx_data.visible_layers:
        if isinstance(layer, pytmx.TiledTileLayer):
            for x, y, gid in layer:
                if gid not in scaled_tiles:
                    tile = tmx_data.get_tile_image_by_gid(gid)
                    if tile:
                        scaled_tiles[gid] = pygame.transform.scale(
                            tile, (tile_size, tile_size)
                        )
                tile = scaled_tiles.get(gid)
                if tile:
                    screen.blit(
                        tile,
                        (
                            round(x * tile_size - world_offset[0]),
                            round(y * tile_size - world_offset[1]),
                        ),
                    )


class Player:
    def __init__(self, x, y, width, height, player_sprite, scale_factor, screen):
        self.image = player_sprite
        self.x = x
        self.y = y
        self.y_velocity = 0
        self.x_velocity = 0
        self.width = width
        self.height = height
        self.rect = pygame.Rect(x, y, width, height)
        self.is_ground = False
        self.jump_velocity = 0
        self.hold_jump = False
        self.gravity = 1
        self.charge = 0
        self.max_charge = 100
        self.angle = 0
        self.min_angle = -80
        self.max_angle = 80
        self.scale_factor = scale_factor
        self.image = pygame.transform.scale(
            self.image,
            (int(self.width * self.scale_factor), int(self.height * self.scale_factor)),
        )
        self.screen = screen

    def draw(self):
        self.screen.blit(
            self.image, (self.x - world_offset[0], self.y - world_offset[1])
        )
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


    def update(self):
        self.apply_gravity()
        self.rect.x = self.x
        self.rect.y = self.y
        self.check_boudaries()
        self.rect.x = self.x
        self.rect.y = self.y
        self.charge_jump()
        self.release_jump()
        self.draw()
        return

    def check_boudaries(self):
        self.is_ground = False
        next_x = int(self.x + self.x_velocity)
        x_predict = pygame.Rect(next_x, self.rect.y, self.width, self.height)
        for tile in floor_rects:
            if x_predict.colliderect(tile):
                if self.x_velocity > 0:
                    self.x = float(tile.left - self.width)
                elif self.x_velocity < 0:
                    self.x = float(tile.right)
                self.x_velocity = 0
                break
        else:
            self.x = float(next_x)

        next_y = int(self.y + self.y_velocity)
        y_predict = pygame.Rect(self.x, next_y, self.width, self.height)
        for tile in floor_rects:
            if y_predict.colliderect(tile):
                if self.y_velocity > 0:
                    self.y = float(tile.top - self.height)
                elif self.y_velocity < 0:
                    self.y = float(tile.bottom)
                self.y_velocity = 0
                break
        else:
            self.y = float(next_y)

        feet_check = pygame.Rect(
            int(self.x), int(self.y + self.height), self.width, 1
        )
        if feet_check.collidelist(floor_rects) != -1:
            self.is_ground = True
player = Player(800, 400, 50, 50, player_sprite, 1, screen)
world_offset = get_world_offset(player, screen.get_width(), screen.get_height())

floor_layer = tmx_data.get_layer_by_name("floor")
if not isinstance(floor_layer, pytmx.TiledTileLayer):
    raise TypeError("The 'floor' layer must be a tile layer")
floor_rects = [
    pygame.Rect(x * tile_size, y * tile_size, tile_size, tile_size)
    for x, y, gid in floor_layer
    if gid != 0
]

move_speed = 5
jump_power = 5
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    keys = pygame.key.get_pressed()
    if keys[pygame.K_RIGHT]:
        player.x_velocity =  move_speed
    elif keys[pygame.K_LEFT]:
        player.x_velocity = -move_speed
    if not keys[pygame.K_RIGHT] and not keys[pygame.K_LEFT]:
            player.x_velocity = 0

    if keys[pygame.K_UP]:
        player.y_velocity = -jump_power
    if keys[pygame.K_DOWN]:
        player.y_velocity = jump_power

    world_offset = get_world_offset(player, screen.get_width(), screen.get_height())
    screen.fill((0, 0, 0))
    draw_map(screen, tmx_data, world_offset)
    player.update()
    pygame.display.update()
    clock.tick(60)
