import pygame
import sys

pygame.init()

WIDTH, HEIGHT = 900, 1200
flags = pygame.RESIZABLE
screen = pygame.display.set_mode((WIDTH, HEIGHT), flags)
pygame.display.set_caption("test")

run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    print(pygame.mouse.get_pos())
