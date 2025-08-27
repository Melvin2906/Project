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

    def insert_at_end(self, data):
        new_node = Node(data)
        if self.head:
            self.tail.next = new_node
            self.tail = new_node
        else:
            self.head = new_node
            self.tail = new_node

    def search(self, data):
        current_node = self.head
        while current_node:
            if current_node.data == data:
                return True
            else:
                current_node = current_node.next
        return False
    
    def print_list(self):
        current_node = self.head
        while current_node:
            print(current_node.data, end=" -> ")
            current_node = current_node.next
        print()
    
    def remove_at_beginning(self):
        self.head = self.head.next

if __name__ == "__main__":
    sushi_preparation = LinkedList()
    sushi_preparation.insert_at_beginin(10)
    sushi_preparation.insert_at_end(12)
    sushi_preparation.print_list()
    sushi_preparation.remove_at_beginning()
    sushi_preparation.print_list()
    data = sushi_preparation.search(12)
    print(data)
        
