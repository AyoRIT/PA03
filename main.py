from DAG import DAG
from DAGNode import DAGNode
from Point import Point
from LineSegment import LineSegment
from Trapezoid import Trapezoid
from RandomIncrementalAlgorithm import RandomizedIncrementalConstruction

def read_input(file_path):
    """
    Reads the input file and parses the bounding box and line segments.
    Assigns labels to points and segments according to the specified naming convention.
    """
    with open(file_path, 'r') as f:
        num_segments = int(f.readline())  # Number of segments
        bbox_coords = list(map(float, f.readline().split()))  # Bounding box coordinates
        segments = []
        point_labels = {}  # Dictionary to assign consistent labels to points
        segment_counter = 1  # Counter for segment labels

        for _ in range(num_segments):
            x1, y1, x2, y2 = map(float, f.readline().split())
            # Create or get labels for the starting point
            if (x1, y1) not in point_labels:
                point_labels[(x1, y1)] = f'P{len(point_labels) + 1}'
            p1_label = point_labels[(x1, y1)]
            # Create or get labels for the ending point
            if (x2, y2) not in point_labels:
                point_labels[(x2, y2)] = f'Q{len(point_labels) + 1}'
            p2_label = point_labels[(x2, y2)]
            # Create Point instances with labels
            p1 = Point(x1, y1, label=p1_label)
            p2 = Point(x2, y2, label=p2_label)
            # Create LineSegment instance with label
            segment_label = f'S{segment_counter}'
            segment_counter += 1
            segment = LineSegment(p1, p2, label=segment_label)
            segments.append(segment)
    return bbox_coords, segments

def initialize_trapezoidal_map(bbox_coords):
    """
    Initializes the trapezoidal map with the bounding box trapezoid.
    """
    x_min, y_min, x_max, y_max = bbox_coords
    # Create points for the bounding box corners with labels
    leftp = Point(x_min, y_min, label='P0')
    rightp = Point(x_max, y_max, label='Q0')
    # Create top and bottom segments of the bounding box with labels
    top_segment = LineSegment(Point(x_min, y_max), Point(x_max, y_max), label='S0')
    bottom_segment = LineSegment(Point(x_min, y_min), Point(x_max, y_min), label='S0')
    # Create the initial trapezoid representing the entire bounding box
    initial_trapezoid = Trapezoid(leftp, rightp, top_segment, bottom_segment)
    initial_trapezoid.label = 'T1'  # Assign label to the initial trapezoid
    # Create the root DAG node with the initial trapezoid
    root = DAGNode(initial_trapezoid)
    dag = DAG(root)
    return dag

def build_trapezoidal_map(dag, segments):
    """
    Builds the trapezoidal map by inserting each segment into the DAG.
    Labels new trapezoids created during the insertion.
    """
    ric = RandomizedIncrementalConstruction(segments)
    ric.DAG = dag
    for segment in segments:
        ric.insert_segment(segment)

def query_point(dag, x, y):
    """
    Queries the DAG with a point and returns the traversal path as a list of labels.
    """
    point = Point(x, y)
    node = dag.root
    path = []  # List to store the traversal path
    while isinstance(node.graph_object, (Point, LineSegment)):
        path.append(node.graph_object.label)
        if isinstance(node.graph_object, Point):
            # Decide to go left or right in the DAG based on x-coordinate
            if x < node.graph_object.x:
                node = node.left_child
            else:
                node = node.right_child
        elif isinstance(node.graph_object, LineSegment):
            # Decide to go left or right based on whether the point is above the segment
            if node.graph_object.aboveLine(point):
                node = node.right_child
            else:
                node = node.left_child
    path.append(node.graph_object.label)  # Add the trapezoid label at the end
    return path

def main():
    # Specify the input file containing the line segments
    input_file = 'hs8154.txt'  # Replace with your actual input file name
    # Read the bounding box and segments from the input file
    bbox_coords, segments = read_input(input_file)
    # Initialize the trapezoidal map with the bounding box
    dag = initialize_trapezoidal_map(bbox_coords)
    # Build the trapezoidal map by inserting segments
    build_trapezoidal_map(dag, segments)
    # Build the adjacency matrix of the DAG
    matrix, node_list = dag.build_adjacency_matrix()
    # Write the adjacency matrix and node labels to a file
    with open('adjacency_matrix.txt', 'w') as f:
        labels = [node.graph_object.label for node in node_list]
        f.write('Nodes:\n')
        for idx, label in enumerate(labels):
            f.write(f'{idx}: {label}\n')
        f.write('\nMatrix:\n')
        for row in matrix:
            f.write(' '.join(map(str, row)) + '\n')
    # Interactive loop to query points
    while True:
        user_input = input("Enter query point (x y), or 'exit' to quit: ")
        if user_input.lower() == 'exit':
            break
        try:
            x_str, y_str = user_input.strip().split()
            x, y = float(x_str), float(y_str)
            # Get the traversal path for the query point
            path = query_point(dag, x, y)
            print('Traversal Path:', ' '.join(path))
        except ValueError:
            print("Invalid input. Please enter two numbers separated by a space.")

if __name__ == '__main__':
    main()
