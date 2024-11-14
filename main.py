import sys
from GraphObject import GraphObject
from Point import Point
from LineSegment import LineSegment
from DAGNode import DAGNode, Trapezoid
from RandomIncrementalAlgorithm import RandomizedIncrementalConstruction
import time
from collections import deque

def load_input(file_path):
    with open(file_path, 'r') as file:
        segments = []
        # Discard number of segments
        file.readline()
        # process bounding points
        line = file.readline()
        bottomLeftX, bottomLeftY, topRightX, topRightY = line.split()
        boundBottomLeft = Point(float(bottomLeftX), float(bottomLeftY))
        boundTopRight = Point(float(topRightX), float(topRightY))

        # Process each subsequent line
        for line in file:
            if len(line.split()) != 0:
                # Split line into x and y coordinates
                point1_x, point1_y, point2_x, point2_y = line.split()
                segments.append(LineSegment(
                    Point((float(point1_x)), float(point1_y)), 
                    Point(float(point2_x), float(point2_y))
                ))
            else:
                break
    return segments, boundBottomLeft, boundTopRight
        


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Please add a file path for the line segments. Usage: python main.py <file_path>")
        
    else:
        file_path = sys.argv[1]
        segments, boundBottomLeft, boundTopRight = load_input(file_path)
        # Initialize algorithm 
        
        R = RandomizedIncrementalConstruction(segments, boundBottomLeft, boundTopRight)
        matrix, node_names = R.DAG.build_adjacency_matrix(segments)
        matrix.to_csv('output.txt', sep='\t', index=False)
        
        def getQueryResult(root, query_point, path = []):
            # function to determine what trapezoid we are in, when we receive a line segment end points
            assert isinstance(query_point, Point)
            assert isinstance(root, DAGNode)
            # assert isinstance(line_seg, LineSegment)
            path.append(node_names[root.graph_object])
            # if we are an X-Node (point), then we want to check if query point is to our right or our left
            if isinstance(root.graph_object, Point):
                # if the query point is to our left, we traverse the graph by going into our left child
                if query_point.x < root.graph_object.x:
                    return getQueryResult(root.left_child, query_point, path)
                # if the query point is to our right, we traverse the graph by going into our right child
                elif query_point.x > root.graph_object.x:
                    return getQueryResult(root.right_child, query_point, path)
                # if the query point is equal to us, we develop new query point as mentioned above in get_offset_point and use the new point to figure out what trapezoid we are in  
                else:
                    return query_point, path

            # if we are a Y-Node, 
            elif isinstance(root.graph_object, LineSegment):
                # traverse tree by checking above and going right if point is found, or 
                if root.graph_object.aboveLine(query_point):
                    return getQueryResult(root.left_child, query_point, path)
                # going left if point isn't above. 
                else:
                    return getQueryResult(root.right_child, query_point, path)

            # we are a leaf node
            elif isinstance(root.graph_object, Trapezoid.Trapezoid):
                return root, path

            # We are neither a point, line or trapezoid
            else:
                raise ValueError('invalid DAG node!')

        def process_input(user_input):
            # Define the function that processes the input and returns the result
            x, y = user_input.split()
            query_point = Point(float(x), float(y))
            output = getQueryResult(R.DAG.root, query_point)
            return output


        while True:
            print()
            user_input = input("Enter points (or press 1 to end): ")
            
            if user_input == "1":
                print("Ending program...")
                break  # Exit the loop if the user enters '1'
            
            # Run the function on the user input and output the result
            trapezoid, path = process_input(user_input)
            print(f"Point found in Trapezoid {trapezoid} through path {path}")


        # def bfs_traversal(root):
        #     if root is None:
        #         return

        #     # Initialize a queue and add the root node
        #     queue = deque([root])

        #     while queue:
        #         # Get the current node from the front of the queue
        #         current_node = queue.popleft()
                
        #         # Process the current node (print its value or do other operations)
        #         print("NODE")
        #         print(current_node.graph_object)

        #         # Add the left and right children of the current node to the queue
        #         if current_node.left_child:
        #             queue.append(current_node.left_child)
        #             print("LEFT: ", current_node.left_child.graph_object)
        #         if current_node.right_child:
        #             queue.append(current_node.right_child)
        #             print("RIGHT: ", current_node.right_child.graph_object)
        #         print()
        # # bfs_traversal(R.DAG.root)