# binary tree implementation
class TreeNode:
    def __init__(self, data, left=None, right=None):
        self.data = data
        self.left_child = left
        self.right_child = right

node1 = TreeNode("B")
node2 = TreeNode("C")
main_node = TreeNode("A", node1, node2)

class Graph:
    def __init__(self):
        self.vertices = {}
    def add_vertex(self, vertex):
        self.vertices[vertex] = []
    def add_edge(self, source, target):
        self.vertices[source].append(target)

my_graph = Graph()
my_graph.add_vertex('David')
my_graph.add_vertex('Miriam')
my_graph.add_vertex('Martin')

my_graph.add_edge('David', 'Miriam')
my_graph.add_edge('David', 'Martin')
my_graph.add_edge('Miriam', 'Martin')

class WeightedGraph:
  def __init__(self):
    self.vertices = {}
  
  def add_vertex(self, vertex):
    self.vertices[vertex] = []
    
  def add_edge(self, source, target, weight):
    self.vertices[source].append([target, weight])

print(my_graph.vertices)