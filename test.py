from pathlib import Path

import pygame
import pytmx
from pytmx.util_pygame import load_pygame

pygame.init()

# Show 20 tiles across and 7 tiles down.
TILE_SIZE =80
COLUMNS = 17
ROWS = 9

screen = pygame.display.set_mode(
    (COLUMNS * TILE_SIZE, ROWS * TILE_SIZE)
)
pygame.display.set_caption("Tile map test — arrow keys to move")
clock = pygame.time.Clock()

# Keep this script beside testmap.tmx.
map_path = Path(__file__).resolve().parent / "testmap.tmx"
tmx_data = load_pygame(str(map_path))

# Scale each tile once.
scaled_tiles = {}

for layer in tmx_data.visible_layers:
    if isinstance(layer, pytmx.TiledTileLayer):
        for x, y, gid in layer:
            if gid not in scaled_tiles:
                tile = tmx_data.get_tile_image_by_gid(gid)

                if tile:
                    scaled_tiles[gid] = pygame.transform.scale(
                        tile, (TILE_SIZE, TILE_SIZE)
                    )

camera_x = 0
camera_y = 0
running = True

while running:
    dt = clock.tick(60) / 1000

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

    keys = pygame.key.get_pressed()

    camera_x += (
        keys[pygame.K_RIGHT] - keys[pygame.K_LEFT]
    ) * 400 * dt
    camera_y += (
        keys[pygame.K_DOWN] - keys[pygame.K_UP]
    ) * 400 * dt

    max_x = max(0, tmx_data.width * TILE_SIZE - screen.get_width())
    max_y = max(0, tmx_data.height * TILE_SIZE - screen.get_height())

    camera_x = max(0, min(camera_x, max_x))
    camera_y = max(0, min(camera_y, max_y))

    screen.fill((30, 30, 40))

    for layer in tmx_data.visible_layers:
        if isinstance(layer, pytmx.TiledTileLayer):
            for x, y, gid in layer:
                tile = scaled_tiles.get(gid)

                if tile:
                    screen.blit(
                        tile,
                        (
                            round(x * TILE_SIZE - camera_x),
                            round(y * TILE_SIZE - camera_y),
                        ),
                    )

    pygame.display.flip()

pygame.quit()