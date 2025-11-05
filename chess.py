import pygame
import time
import random

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
    def __init__(self, x=0, y=0, id=0):
        self.pos = [x, y]
        self.id = id

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
    def __init__(self, x=0, y=0, id=0):
        self.pos = [x, y]
        self.id = id
    
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
    def __init__(self, x=0, y=0, id=0):
        self.pos = [x, y]
        self.id = id
    
    def __repr__(self):
        string = f"""Knight:
    Position = [pos_x={self.pos[0]}, pos_y={self.pos[1]}]
    ID = {self.id}"""
        return string

class Tower:
    def __init__(self, x=0, y=0, id=0):
        self.pos = [x, y]
        self.id = id
    
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
    def __init__(self, x=0, y=0, id=0):
        self.pos = [x, y]
        self.id = id
    
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
    def __init__(self, x=0, y=0, color="white", id=0, x1=0, x2=0):
        dic = {"a":1, "b":2, "c":3, "d":4, "e":5, "f":6, "g":7, "h":8}
        self.pos = [x, y]
        self.color = color.lower()
        self.id = id
        self.pos1 = [x1, x2]

    def change_type(self, name):
        dic = {"queen": Queen, "knight":Knight, "tower":Tower, "bishop":Bishop}
        if self.pos1[1] == 8 or self.pos1[1] == 1:
            return dic[name.lower()](self.pos1[0], self.pos1[1], random.randint(10, 50))
    
    def move(self):
        if self.pos1[0] != self.pos[0]:
            print("\nYou can't move the pion horizontally\n")
        else:
            if self.pos1[1] > 8 or self.pos1[1] < 1:
                print("\nPosition out of range, please choose an another 'y' coordinate\n")
            else:
                if (self.color == "white" and self.pos1[1] < self.pos[1]) or (self.color == "black" and self.pos1[1] > self.pos[1]):
                    print("\nYou can't move your pawn like this\n")
                else:
                    self.pos[1] = self.pos1[1]
    
    def __eq__(self, other):
        if isinstance(other, Pawn):
            # return self.pos[0] == other.pos[0] and self.pos[1], other.pos[1]
            if self.color == "white":
                return (((self.pos1[1] == other.pos[0]) and (self.pos1[1] == other.pos[1]))
                or ((self.pos1[1] == other.pos[0]) and (self.pos1[1] == other.pos[1])))
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

pion1 = Pawn(2, 5, "white", 0)
print(pion1)
pion1.move(2, 6)
print(pion1)
pion1.move(2, 7)
print(pion1)

print("\n(-----------------^_^-------------------)\n")
queen_n = pion1.change_type(2, 8, "tower")
print(f"Transformation complete ! Congatulation, your pawn just evolve in a {type(queen_n)}, here is his stat: \n{queen_n}")

print("\n(-----------------^_^-------------------)\n")

pion2 = Pawn(2, 7, "Black", 1)
print(pion2)
pion2.move(2, 8)
print(f"Because of your behavior, the current stat of your pawn is still: \n{pion2}")

pion3 = Pawn(2, 5, "White", 2)
pion3.move(2, 4)
print(f"Because of your behavior, the current stat of your pawn is still: \n{pion3}")

print("\n(================^_^================)\n")
queen_n.move(3, 2)
print(queen_n)

white_pawn = [Pawn(pawn+1, 2, "white", pawn) for pawn in range(8)]
print("\n===================================================\nList des pions blancs\n")
for i in white_pawn:
    print(i)

black_pawn = [Pawn(pawn+1, 2, "black", int((pow(pawn, 2) + 2)/0.5)) for pawn in range(8)]
print("\n===================================================\nList des pions noirs\n")
for i in black_pawn:
    print(i)