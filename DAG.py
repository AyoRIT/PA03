from DAGNode import DAGNode
from collections import deque 
from collections import defaultdict
from Trapezoid import Trapezoid

class DAG:
    def __init__(self, root):
        assert isinstance(root, DAGNode)
        self.root = root

    def build_adjacency_matrix(self):
        visited = set()
        queue = deque(self.root)
        matrix = defaultdict(list)
        
        while queue:
            curr_node = queue.popleft()
            if not isinstance(curr_node, Trapezoid):
                assert isinstance(curr_node, DAGNode)
                if curr_node not in visited:
                    visited.add(curr_node)
                    queue.append(curr_node.left_child)
                    queue.append(curr_node.right_child)
                    matrix_object = curr_node.graph_object
                    

                    matrix[matrix_object].append(curr_node.left_child.graph_object)
                    matrix[matrix_object].append(curr_node.right_child.graph_object)

        return matrix