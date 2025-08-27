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

def in_order(self, current_node):
    if current_node:
        self.in_order(current_node.left_node)
        print(current_node.value)
        self.in_order(current_node.right_node)

def pre_order(self, current_node):
    if current_node:
        print(current_node.value)
        self.in_order(current_node.left_node)
        self.in_order(current_node.right_node)

def pre_order(self, current_node):
    if current_node:
        self.in_order(current_node.left_node)
        self.in_order(current_node.right_node)
        print(current_node.value)


# depth first search - recursive implementation, complexity O(V + E) : V -> number of verteces, E -> number of edges

def dfs(visited_vertices, graph, current_vertex):
    if current_vertex not in visited_vertices:
        print(current_vertex)
        visited_vertices.add(current_vertex)
        for adjacent_vertex in graph[current_vertex]:
            dfs(visited_vertices, graph, adjacent_vertex)

graph = {
  '0' : ['1','2'],
  '1' : ['0', '2', '3'],
  '2' : ['0', '1', '4'],
  '3' : ['1', '4'],
  '4' : ['2', '3']
}

root = BinarySearchTree()
root.insert("Little women")
root.insert("Heidi")
root.insert("Olivier twist")
root.insert("Dracula")
root.insert("Jane Eyre")
root.insert("Moby Dick")
root.insert("Vanity Fair")

visited_vertices = []
current_vertex = 0

# Set() permet de créer un ensemble (un set) vide ou de convertir un objet itérable en un ensemble
dfs(set(), graph, '0')