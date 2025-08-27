# Pour les queues le premier élément entré est le premier élément enlevé
class Node:
    def __init__(self, data):
        self.data = data
        self.next = None

class queues:
    def __init__(self):
        self.top = None
        self.end = None
    
    def enqueue(self, data):
        new_node = Node(data)
        if self.top == None:
            self.top = new_node
            self.end = new_node
        else:
            self.end.next = new_node
            self.end = new_node
    
    def dequeue(self):
        if self.top:
            remove = self.top
            self.top = remove.next
            remove.next = None
        
        if self.top == None:
            self.end = None

    def has_element(self):
        return self.top != None

    def print_list(self):
        current_node = self.top
        while current_node:
            print(current_node.data, end=" -> ")
            current_node = current_node.next
        print()
        

if __name__ == "__main__":
    sushi_preparation = queues()
    sushi_preparation.enqueue(10)
    sushi_preparation.enqueue(11)
    sushi_preparation.enqueue(12)
    sushi_preparation.enqueue(13)
    sushi_preparation.enqueue(14)
    sushi_preparation.print_list()
    sushi_preparation.dequeue()
    data1 = sushi_preparation.has_element()
    print(data1)
    sushi_preparation.print_list()

import queue

my_queue = queue.SimpleQueue()

my_queue.put("Sushi")
my_queue.put("Lasagna")
my_queue.put("Paella")

print("The sise is: ", my_queue.qsize())

print(my_queue.get())
print(my_queue.get())
print(my_queue.get())

print("Empty queue: ", my_queue.empty())