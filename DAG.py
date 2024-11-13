from DAGNode import DAGNode
from collections import deque 
from collections import defaultdict
from Trapezoid import Trapezoid
from LineSegment import LineSegment
from Point import Point
import pandas as pd

class DAG:
    def __init__(self, root):
        assert isinstance(root, DAGNode)
        self.root = root

    def build_adjacency_list(self):
        visited = set()
        queue = deque([self.root])
        a_list = defaultdict(list)
        
        while queue:
            curr_node = queue.popleft()
            if not isinstance(curr_node.graph_object, Trapezoid):
                assert isinstance(curr_node, DAGNode)
                if curr_node not in visited:
                    visited.add(curr_node)
                    if curr_node.left_child:
                        queue.append(curr_node.left_child)
                    if curr_node.right_child:
                        queue.append(curr_node.right_child)
                    matrix_object = curr_node.graph_object
                

                    a_list[matrix_object].append(curr_node.left_child.graph_object)
                    a_list[matrix_object].append(curr_node.right_child.graph_object)
            else:
                a_list[curr_node.graph_object]
        print("-------OUTPUT ADJACENCY LIST-------\n")
        for key, value in a_list.items():
            print(f"{key}:")
            for n in value:
                print(n)
            print()
        return a_list
    
    def build_adjacency_matrix(self, segments):
        # get adjacency list
        a_list = self.build_adjacency_list()
        # get all keys within list
        nodes = a_list.keys()
        # rename nodes to make matrix more readable
        node_names = {}
        ls_count, t_count = 1,1
        for seg in segments:
            assert isinstance(seg, LineSegment)
            node_names[seg] = "S"+str(ls_count)
            
            if seg.left not in node_names:
                node_names[seg.left] = "P"+str(ls_count)
                
            if seg.right not in node_names:
                node_names[seg.right] = "Q"+str(ls_count)
            ls_count += 1
        for node in nodes:
            if isinstance(node, Trapezoid):
                node_names[node] = "T"+str(t_count)
                t_count += 1
        node_indices = {node: i for i, node in enumerate(nodes)}  # Map each node to an index

        # Initialize an n x n matrix with zeros
        n = len(nodes)
        adj_matrix = [[0] * (n+2) for _ in range(n+2)]


        k = 1
        for node in nodes:
            adj_matrix[0][k] = node_names[node]
            adj_matrix[k][0] = node_names[node]
            k += 1
        # Output
        for node, neighbors in a_list.items():
            k = node_indices[node]
            for neighbor in neighbors:
                i, j = node_indices[node], node_indices[neighbor]
                adj_matrix[j+1][i+1] = 1  # Set to 1 for an edge from node to neighbor
        adj_matrix = adj_matrix[1:-1]


        top_row = ['']
        for i in range(len(adj_matrix)):
            top_row.append(adj_matrix[i][0])
        top_row.append('sum')
        adj_matrix.insert(0, top_row)
        # Calculate sums
        row_total = ['sum']
        for i in range(1, len(adj_matrix)):
            row_sum = 0
            col_sum = 0
            for j in range(1, len(adj_matrix)):
                row_sum += adj_matrix[i][j]
                col_sum += adj_matrix[j][i]
            print("colsum", col_sum)
            adj_matrix[i][-1] = row_sum
            row_total.append(col_sum)
        row_total.append('')
        adj_matrix.append(row_total)
        
        # adj_matrix.pop(0)
        
        
        print("-------OUTPUT ADJACENCY MATRIX-------\n")
        df = pd.DataFrame(adj_matrix)
        print(df)
        # for row in adj_matrix:
        #     print(row)
        # return adj_matrix