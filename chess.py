import pygame
import time
import random


WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREY = pygame.Color("grey")
RED = pygame.Color("red")
BLUE = pygame.Color("blue")
WIDTH, HEIGHT, SHAPE, PIECES_SHAPE = 900, 800, 50, 53
flags = pygame.RESIZABLE
screen = pygame.display.set_mode((WIDTH, HEIGHT))
SHAPE_TWO = 50
class King:
    """ 
    King classes stand for the king's piece in chess
       
        :x attribute: x position of the piece
        :y attribute: y position of the piece
        :color attribute: color of the piece
        :id attribute: id of the piece
    
        :move method: for the piece deplacements
        :__eq__ (==) method: to see if a piece have been eat or not

    """
    def __init__(self, x=0, y=0, color="white", id=0):
        self.pos = [x, y]
        self.id = id
        self.color = color

    def move(self, x1, y1):
        if x1 != self.pos[0]:
            print("You can't move the pion horizontally")
        else:
            if y1 > 8 or y1 < 1:
                print("Position out of range, please choose an another 'y' coordinate")
            else:
                self.pos[1] = y1
    
    def __eq__(self, other):
        if isinstance(other, Pawn):
            # return self.pos[0] == other.pos[0] and self.pos[1], other.pos[1]
            if self.color == "white":
                return ((((self.pos[0] + 1) == other.pos[0]) and ((self.pos[1] + 1) == other.pos[1]))
                or (((self.pos[0] - 1) == other.pos[0]) and ((self.pos[1] + 1) == other.pos[1])))
            else:
                return ((((self.pos[0] + 1) == other.pos[0]) and ((self.pos[1] - 1) == other.pos[1]))
                or (((self.pos[0] - 1) == other.pos[0]) and ((self.pos[1] - 1) == other.pos[1])))
        return False


    def __repr__(self):
        string = f"""Pion:
    Position = [pos_x={self.pos[0]}, pos_y={self.pos[1]}]
    Color = {self.color}
    ID = {self.id}"""
        return string

class Queen:
    """ 
    Queen classes stand for the queen's piece in chess
       
        :x attribute: x position of the piece
        :y attribute: y position of the piece
        :color attribute: color of the piece
        :id attribute: id of the piece
    
        :move method: for the piece deplacements
        :__eq__ (==) method: to see if a piece have been eat or not

    """
    def __init__(self, x=0, y=0, id=0, color="white"):
        self.pos = [x, y]
        self.id = id
        self.color=color
    
    def move(self, x1, y1):
        if ((1 <= x1 <= 8) and (1 <= y1 <= 8)):
            self.pos[0] = x1
            self.pos[1] = y1
        else:
            print("\nPosition value out of range, please try an another one\n")

    def __repr__(self):
        string = f"""Queen:
    Position = [pos_x={self.pos[0]}, pos_y={self.pos[1]}]
    ID = {self.id}"""
        return string

class Knight:
    """ 
    Knight classes stand for the knight's piece in chess
       
        :x attribute: x position of the piece
        :y attribute: y position of the piece
        :color attribute: color of the piece
        :id attribute: id of the piece
    
        :move method: for the piece deplacements
        :__eq__ (==) method: to see if a piece have been eat or not

    """
    def __init__(self, x=0, y=0, id=0, color="white"):
        self.pos = [x, y]
        self.id = id
        self.color=color
    
    def move(self, x1=0, y1=0):
        if (((x1 in (self.pos[0]-2, self.pos[0]+2)) and (y1 not in (self.pos[1]-1, self.pos[1]+1)))
            or ((y1 in (self.pos[1]-2, self.pos[1]+2)) and (x1 not in (self.pos[0]-1, self.pos[0]+1)))):
            print("You can't move your knight like that")
        else:
            self.pos = [x1, y1]
    
    def __repr__(self):
        string = f"""Knight:
    Position = [pos_x={self.pos[0]}, pos_y={self.pos[1]}]
    ID = {self.id}"""
        return string

class Tower:
    """ 
    Tower classes stand for the tower's piece in chess
       
        :x attribute: x position of the piece
        :y attribute: y position of the piece
        :color attribute: color of the piece
        :id attribute: id of the piece
    
        :move method: for the piece deplacements
        :__eq__ (==) method: to see if a piece have been eat or not

    """
    def __init__(self, x=0, y=0, id=0, color="white"):
        self.pos = [x, y]
        self.id = id
        self.color=color
    
    def move(self, x1, y1):
        if (x1 != self.pos[0] and y1 != self.pos[1]):
            print("\nYou can't use an diagonal way for your tower, please try again\n")
        else:
            if ((1 <= x1 <= 8) and (1 <= y1 <= 8)):
                self.pos[0] = x1
                self.pos[1] = y1 
            else:
                print("\nPosition out of range please try an another one\n")       

    def __repr__(self):
        string = f"""Tower:
    Position = [pos_x={self.pos[0]}, pos_y={self.pos[1]}]
    ID = {self.id}"""
        return string

class Bishop:
    """ 
    Bishop classes stand for the bishop's piece in chess
       
        :x attribute: x position of the piece
        :y attribute: y position of the piece
        :color attribute: color of the piece
        :id attribute: id of the piece
    
        :move method: for the piece deplacements
        :__eq__ (==) method: to see if a piece have been eat or not

    """
    def __init__(self, x=0, y=0, id=0, color="white"):
        self.pos = [x, y]
        self.id = id
        self.color=color
    
    def move(self, x1, y1):
        if (x1 == self.pos[0] or y1 == self.pos[1]):
            print("\nYou can't move your bishop like that, you need a disgonal way\n")
        else:
            if ((1 <= x1 <= 8) and (1 <= y1 <= 8)):
                self.pos[0] = x1
                self.pos[1] = y1
            else:
                print("\nPosition value out of range, select an another one\n")

    def __repr__(self):
        string = f"""Bishop:
    Position = [pos_x={self.pos[0]}, pos_y={self.pos[1]}]
    ID = {self.id}"""
        return string

class Pawn:
    """ 
    Pawn classes stand for the pawn piece in chess
       
        :x attribute: x position of the piece
        :y attribute: y position of the piece
        :color attribute: color of the piece
        :id attribute: id of the piece
    
        :move method: for the piece deplacements
        :__eq__ (==) method: to see if a piece have been eat or not

    """
    def __init__(self, x=0, y=0, color="white", id=0, img=""):
        dic = {"a":1, "b":2, "c":3, "d":4, "e":5, "f":6, "g":7, "h":8}
        self.pos = [x, y]
        self.color = color.lower()
        self.id = id
        self.img = img

    def change_type(self, x1, y1, name):
        dic = {"queen": Queen, "knight":Knight, "tower":Tower, "bishop":Bishop}
        if y1 == 8 or y1 == 1:
            return dic[name.lower()](x1, y1, random.randint(10, 50))
    
    def move(self, x1, y1):
        if x1 != self.pos[0]:
            print("\nYou can't move the pion horizontally\n")
        else:
            if y1 > 8 or y1 < 1:
                print("\nPosition out of range, please choose an another 'y' coordinate\n")
            else:
                if (self.color == "white" and y1 < self.pos[1]) or (self.color == "black" and y1 > self.pos[1]):
                    print("\nYou can't move your pawn like this\n")
                else:
                    self.pos[1] = y1
    
    def __eq__(self, other):
        if isinstance(other, Pawn):
            # return self.pos[0] == other.pos[0] and self.pos[1], other.pos[1]
            if self.color == "white":
                return ((((self.pos[0] + 1) == other.pos[0]) and ((self.pos[1] + 1) == other.pos[1]))
                or (((self.pos[0] - 1) == other.pos[0]) and ((self.pos[1] + 1) == other.pos[1])))
            else:
                return ((((self.pos[0] + 1) == other.pos[0]) and ((self.pos[1] - 1) == other.pos[1]))
                or (((self.pos[0] - 1) == other.pos[0]) and ((self.pos[1] - 1) == other.pos[1])))
        return False


    def __repr__(self):
        string = f"""Pion:
    Position = [pos_x={self.pos[0]}, pos_y={self.pos[1]}]
    Color = {self.color}
    ID = {self.id}"""
        return string

def create_plato():
    plaq = [[] for i in range(8)]
    for i in range(8):
        for j in range(8):
            if i % 2 == 0:
                if j % 2 == 0:
                    plaq[i].append('1')
                else:
                    plaq[i].append('0')
            else:
                if j % 2 != 0:
                    plaq[i].append('1')
                else:
                    plaq[i].append('0')
    return plaq

lis = [[Tower(1, 1), Knight(2, 1), Bishop(3, 1), Queen(4, 1), King(5, 1), Bishop(6, 1), Knight(7, 1), Tower(8, 1)],
       [Pawn(i, 2, "white") for i in range(1,9)],
       [0 for i in range(8)],
       [0 for i in range(8)],
       [0 for i in range(8)],
       [0 for i in range(8)],
       [Pawn(i, 7, "black") for i in range(1,9)],
       [Tower(1, 8, "black"), Knight(2, 8, "black"), Bishop(3, 8, "black"), Queen(4, 8, "black"), King(5, 8, "black"), Bishop(6, 8, "black"), Knight(7, 8, "black"), Tower(8, 8, "black")]]

def add_pieces(plaq):
    for i in range(len(lis)):
        for j in range(len(lis[i])):
            if (lis[i][j] == 0):
                pass
            else:
                plaq[lis[i][j].pos[1] - 1][lis[i][j].pos[0] - 1] = lis[i][j]

def draw_plato(plaq=create_plato()):
    for i in range(8):
        for j in range(8):
            if plaq[i][j] == "0":
                pygame.draw.rect(screen, WHITE, ((i + 4) * SHAPE_TWO, (j + 4) * SHAPE_TWO, SHAPE_TWO, SHAPE_TWO))
            else:
                pygame.draw.rect(screen, BLACK, ((i + 4) * SHAPE_TWO, (j + 4) * SHAPE_TWO, SHAPE_TWO, SHAPE_TWO))

def draw_pieces_with_circle(surface,color, x, y, border, mouse_position):
    new_color = (0, 0, 0)
    if ((x <= mouse_position[0] <= x + 10) and (y <= mouse_position[1] <= y + 10)):
        pygame.draw.circle(surface, color, (x, y), 10)
        pygame.draw.circle(surface, new_color, (x, y), 10, border)
    else:
        pygame.draw.circle(surface, color, (x, y), 10)

def determine_type(element):
    li = [King, Queen, Tower, Bishop, Pawn, Knight]

    for j in li:
        if (type(element) == j):    
            b = 0
            break
        else:
            b = 1
    return b

# for i in lis:
#     for j in i:
#         print(determine_type(j))


def print_pieces_and_plato(lis, surface, shape, border, mouse_position):
    for i in range(len(lis)):
        for j in range(len(lis[i])):
            if (type(lis[i][j]) == Knight):
                draw_pieces_with_circle(surface, pygame.Color("blue"), (j + 4) * shape, (i + 4) * shape, border, mouse_position)
            elif (type(lis[i][j]) == Pawn):
                if lis[i][j].color == "black":
                    draw_pieces_with_circle(surface, pygame.Color("brown"), (j + 4) * shape, (i + 4) * shape, border, mouse_position)
                else :
                    draw_pieces_with_circle(surface, pygame.Color("yellow"), (j + 4) * shape, (i + 4) * shape, border, mouse_position)
            elif (type(lis[i][j]) == Queen):
                draw_pieces_with_circle(surface, pygame.Color("green"), (j + 4) * shape, (i + 4) * shape, border, mouse_position)
            elif (type(lis[i][j]) == King):
                draw_pieces_with_circle(surface, pygame.Color("purple"), (j + 4) * shape, (i + 4) * shape, border, mouse_position)
            elif (type(lis[i][j]) == Bishop):
                draw_pieces_with_circle(surface, pygame.Color("pink"), (j + 4) * shape, (i + 4) * shape, border, mouse_position)
            elif (type(lis[i][j]) == Tower):
                draw_pieces_with_circle(surface, pygame.Color("magenta"), (j + 4) * shape, (i + 4) * shape, border, mouse_position)
            else:
                pass