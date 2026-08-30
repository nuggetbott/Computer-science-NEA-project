import pygame
pygame.init()
screen = pygame.display.set_mode((1000, 800))
clock = pygame.time.Clock()
run = True 
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    screen.fill((255, 255, 255))
    pygame.display.update()
    clock.tick(60)