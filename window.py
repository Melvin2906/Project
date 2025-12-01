import pygame
import sys
from chess import Knight, King, Queen, Pawn, Bishop, Tower, create_plato, add_pieces, print_pieces_and_plato, lis
pygame.init()

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREY = pygame.Color("grey")
RED = pygame.Color("red")
BLUE = pygame.Color("blue")
WIDTH, HEIGHT, SHAPE, PIECES_SHAPE = 900, 800, 50, 53
flags = pygame.RESIZABLE
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("test")

def draw_plato(plaq=create_plato()):
    for i in range(8):
        for j in range(8):
            if plaq[i][j] == "0":
                pygame.draw.rect(screen, WHITE, ((i + 4) * SHAPE, (j + 4) * SHAPE, SHAPE, SHAPE))
            else:
                pygame.draw.rect(screen, BLACK, ((i + 4) * SHAPE, (j + 4) * SHAPE, SHAPE, SHAPE))
run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    screen.fill(GREY)
    draw_plato()
    print_pieces_and_plato(lis, screen, PIECES_SHAPE)
    
    pygame.display.flip()

