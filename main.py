import sys
from Point import Point
from LineSegment import LineSegment
from RandomIncrementalAlgorithm import RandomizedIncrementalConstruction
import time


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
            if line:
                # Split line into x and y coordinates
                point1_x, point1_y, point2_x, point2_y = line.split()
                segments.append(LineSegment(
                    Point((float(point1_x)), float(point1_y)), 
                    Point(float(point2_x), float(point2_y))
                ))
    return segments, boundBottomLeft, boundTopRight
        


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Please add a file path for the line segments. Usage: python main.py <file_path>")
        
    else:
        file_path = sys.argv[1]
        segments, boundBottomLeft, boundTopRight = load_input(file_path)
        # Initialize algorithm 
        for i in range(0, 1):
            R = RandomizedIncrementalConstruction(segments, boundBottomLeft, boundTopRight)
            matrix = R.DAG.build_adjancency_matrix()
            # print("-------OUTPUT MATRIX-------")
            # for key, value in matrix.items():
            #     print(f"{key}:")
            #     for n in value:
            #         print(n)
            #     print()
