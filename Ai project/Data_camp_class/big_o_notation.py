# O(1) or constant:
# c'est l'efficacité d'un algorithm dont où le temps d'exécution reste indépendant de la taille de l'entrée

# example:
def constant(colors):
    print(colors[2])

if __name__ == "__main__":
    color = ['green', 'red', 'blue', 'pink']
    constant(color)

# O(n) or linear complexity:
#If the list has N elements, the complexity is 1 + (N - 1) + 1 = N + 1 = O(N)

# example:
def linear(colors):
    for color in colors:
        print(color)
    
if __name__ == "__main__":
    print("\n")
    color = ['green', 'red', 'blue', 'pink']
    linear(color)

# O(n²) or quadratic:
# Dans ce type, le temps d'exécution de l'algorithme augmente en fonction du carré de la taille de l'entrée.

# example:
def quadratic(colors):
    for first in colors:
        for second in color:
            print(first, second)

if __name__ == "__main__":
    print("\n")
    color = ['green', 'red', 'blue']
    quadratic(color)

# O(n^3) or cubic:
# its run time is proportional to the cube of the number of elements being processed

# example:
def cubic(colors):
    for first in colors:
        for second in colors:
            for third in colors:
                print(first, second, third)

if __name__ == "__main__":
    print("\n")
    color = ['green', 'red', 'blue']
    cubic(color)

# Calculating big O notation:
colors = ['green', 'yellow', 'blue', 'pint', 'black', 'white', 'purple'] # O(1)
other_colors = ['orange', 'brown'] # O(1)

def complew_algorithm(colors):
    color_count = 0 # O(1)

    for color in colors:
        print(color) # O(n)
        color_count += 1 # O(n)
    
    for other_color in other_colors:
        print(other_color) # O(m) parce que c'est une autre boucle, donc on remplace le n par m
        color_count += 1 # O(m)
    
    print(color_count) # O(1)

complew_algorithm(colors) # O(4 + 2n + 2m)

# Simplifying Big O Notation

# 1. Remove constans
#   O(4 + 2n + 2m) -> O(n + m)
# 2. Different variables for different inputs
#   O(n + m)

# exercices

# calculate the complexity

# 1.
class Node:
    def __init__(self, data):
        self.data = data
        self.next = None

class LinkedList:
    def __init__(self):
        self.head = None
        self.tail = None
    
    def insert_at_beginin(self, data):
        new_node = Node(data)
        if self.head:
            new_node.next = self.head
            self.head = new_node
        else:
            self.tail = new_node
            self.head = new_node
    
# 2.
def search(self, data):
    current_node = self.head
    while current_node:
        if current_node.data == data:
            return True
        else:
            current_node = current_node.next
    return False