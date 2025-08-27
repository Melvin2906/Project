# Pour les stacks le dernier élément entré est le premier éléments enlevé
class Node:
    def __init__(self, data):
        self.data = data
        self.next = None

class Stack:
    def __init__(self):
        self.top = None
        self.size = 0
     
    def push(self, data):
        new_node = Node(data)
        if self.top:
            new_node.next = self.top
        self.top = new_node
        self.size += 1
    
    def pop(self):
        if self.top is None:
            return None
        else:
            popped_node = self.top
            self.size -= 1
            self.top = self.top.next
            popped_node.next = None
            return popped_node.data 
    
    def peek(self):
        if self.top:
            return self.top.data
        else:
            return None

    def print_list(self):
        current_node = self.top
        while current_node:
            print(current_node.data, end=" -> ")
            current_node = current_node.next
        print()
        
if __name__ == "__main__":
    sushi_preparation = Stack()
    sushi_preparation.push(10)
    sushi_preparation.push(11)
    sushi_preparation.push(12)
    sushi_preparation.push(13)
    sushi_preparation.push(14)
    sushi_preparation.print_list()
    data1 = sushi_preparation.pop()
    print(data1)
    sushi_preparation.print_list()
    data = sushi_preparation.peek()
    print(data)

import queue

my_book_stack = queue.LifoQueue(maxsize=0)
my_book_stack.put("The misunderstanding")
my_book_stack.put("Persepolis")
my_book_stack.put("1984")

print("The size is: ", my_book_stack.qsize())
print(my_book_stack.get())
print(my_book_stack.get())
print(my_book_stack.get())
print("Empty stack: ", my_book_stack.empty())