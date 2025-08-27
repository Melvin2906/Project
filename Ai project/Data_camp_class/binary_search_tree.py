class TreeNode:
    def __init__(self, data, left=None, right=None):
        self.value = data
        self.left_node = left
        self.right_node = right

class BinarySearchTree:
    def __init__(self):
        self.root = None
    
    def search(self, search_value):
        current_node = self.root

        while current_node:
            if search_value == current_node.value:
                return True
            elif search_value < current_node.value:
                current_node = current_node.left_node
            else:
                current_node = current_node.right_node
        return False
    
    def insert(self, data):
        new_node = TreeNode(data)

        if self.root == None:
            self.root = new_node
        else:
            current_node = self.root
            while True:
                if data < current_node.value:
                    if current_node.left_node == None:
                        current_node.left_node = new_node
                        return
                    else:
                        current_node = current_node.left_node
                elif data > current_node.value:
                    if current_node.right_node == None:
                        current_node.right_node = new_node
                        return
                    else:
                        current_node = current_node.right_node
    
    def find_min(self):
        current_node = self.root
        while current_node.left_node:
           current_node = current_node.left_node
        return current_node.value
  
root = BinarySearchTree()
root.insert("Little women")
root.insert("Heidi")
root.insert("Olivier twist")
root.insert("Dracula")
root.insert("Jane Eyre")
root.insert("Moby Dick")
root.insert("Vanity Fair")

boal = root.search("Heidi")
print(boal)
print(root.find_min())