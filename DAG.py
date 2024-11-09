from DAGNode import DAGNode
from collections import deque
from Trapezoid import Trapezoid

class DAG:
    def __init__(self, root):
        assert isinstance(root, DAGNode)
        self.root = root

    def build_adjacency_matrix(self):
        """
        Builds the adjacency matrix of the DAG.
        Returns the adjacency matrix and the list of nodes.
        """
        # Dictionary to keep track of visited nodes and their indices
        visited = {}
        # Queue for BFS traversal
        queue = deque([self.root])
        node_list = []
        # BFS traversal to visit all nodes
        while queue:
            node = queue.popleft()
            if node not in visited:
                # Assign an index to the node
                visited[node] = len(node_list)
                node_list.append(node)
                # Add children to the queue
                if node.left_child:
                    queue.append(node.left_child)
                if node.right_child:
                    queue.append(node.right_child)
        # Initialize the adjacency matrix
        size = len(node_list)
        matrix = [[0] * size for _ in range(size)]
        # Build the adjacency matrix based on parent-child relationships
        for node in node_list:
            idx_parent = visited[node]
            for child in [node.left_child, node.right_child]:
                if child:
                    idx_child = visited[child]
                    matrix[idx_parent][idx_child] = 1  # Edge from parent to child
        return matrix, node_list
