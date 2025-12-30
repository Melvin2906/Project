import pygame
import sys
from chess import Knight, King, Queen, Pawn, Bishop, Tower,    \
    create_plato, add_pieces, print_pieces_and_plato, draw_pieces_with_circle, draw_plato, \
    WIDTH, WHITE, BLACK, BLUE, HEIGHT, SHAPE, PIECES_SHAPE, RED, GREY, screen, lis
pygame.init()



pygame.display.set_caption("my_first_chess_game")

run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    screen.fill(GREY)
    draw_plato()
    print_pieces_and_plato(lis, screen, PIECES_SHAPE, border=3, mouse_position=list(pygame.mouse.get_pos()))
    
    pygame.display.flip()

