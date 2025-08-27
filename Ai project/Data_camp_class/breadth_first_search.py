import queue

class TreeNode:
    def __init__(self, data, left=None, right=None):
        self.value = data
        self.left_node = left
        self.right_node = right

class BinaryTreeSearch:
    def __init__(self):
        self.root = None

    def insert(self, data):
        new_node = TreeNode()

        if self.root == None:
            self.root = new_node
        else:
            current_node = new_node
            while True:
                if data < current_node.value:
                    if current_node.left_node == None:
                        current_node.left_node = new_node
                        return
                    else:
                        current_node = current_node.left_node
                elif data > current_node:
                    if current_node.right_node == None:
                        current_node.right_node = new_node
                        return
                    else:
                        current_node = current_node.right_node

# Breadth first search - binary trees: complexity of O(n)

def bfs(self):
    if self.root:
        visited_nodes = []
        bfs_queue = queue.SimpleQueue()
        bfs_queue.put(self.root)
        while not bfs_queue.empty():
            current_node = bfs_queue.get()
            visited_nodes.append(current_node.value)
            if current_node.left_node:
                bfs_queue.put(current_node.left_node)
            if current_node.right_node:
                bfs_queue.put(current_node.right_node)
    return visited_nodes

# Breadth first search - graphs: complexity O(V + E) : V -> number of verteces, E -> number of edges
def bfs_2(graph, initial_vertex):
    visited_vertices = []
    bfs_queue = queue.SimpleQueue()
    bfs_queue.put(initial_vertex)
    visited_vertices.append(initial_vertex)
    while not bfs_queue.empty():
        current_vertext = bfs_queue.get()
        for adjacent_vertex in graph[current_vertext]:
            if adjacent_vertex not in visited_vertices:
                visited_vertices.append(adjacent_vertex)
                bfs_queue.put(adjacent_vertex)
    return visited_vertices


# Bfs for search in graph:
import queue

def bfs_3(graph, initial_vertex, search_value):
  visited_vertices = []
  bfs_queue = queue.SimpleQueue()
  visited_vertices.append(initial_vertex)
  bfs_queue.put(initial_vertex)

  while not bfs_queue.empty():
    current_vertex = bfs_queue.get()
    # Check if you found the search value
    if current_vertex == search_value:
      # Return True if you find the search value
      return True   
    for adjacent_vertex in graph[current_vertex]:
      # Check if the adjacent vertex has been visited
      if adjacent_vertex not in visited_vertices:
        visited_vertices.append(adjacent_vertex)
        bfs_queue.put(adjacent_vertex)
  # Return False if you didn't find the search value
  return False

graph = {
  '4' : ['6','7'],
  '6' : ['4', '7', '8'],
  '7' : ['4', '6', '9'],
  '8' : ['6', '9'],
  '9' : ['7', '8']
}

print(bfs_3(graph, '4', '8'))