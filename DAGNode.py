import copy

from GraphObject import GraphObject
from Point import Point
from LineSegment import LineSegment
from Trapezoid import Trapezoid  # Import Trapezoid class directly

class DAGNode:
    _id_counter = 0  # Class-level counter for unique IDs

    def __init__(self, graph_object, left_child=None, right_child=None):
        # We use graph_object to ensure each node is either a point, a segment, or a trapezoid
        assert isinstance(graph_object, GraphObject)
        self.graph_object = graph_object
        self.left_child = left_child
        self.right_child = right_child
        self.id = DAGNode._id_counter  # Unique identifier for hashing
        DAGNode._id_counter += 1

    def get_offset_point(self, query_point, line_seg) -> Point:
        """
        Handles the special case where the query point coincides with an X-node in the DAG.
        Moves the point slightly along the line segment to avoid ambiguity.
        """
        assert isinstance(query_point, Point)
        assert isinstance(line_seg, LineSegment)

        segment_length = line_seg.length
        if segment_length == 0:
            raise ValueError('Line segment length is zero.')

        new_query_point = copy.copy(query_point)
        if query_point == line_seg.left:
            # The query point is the left point of the line segment
            x_diff = line_seg.right.x - query_point.x
            y_diff = line_seg.right.y - query_point.y
        elif query_point == line_seg.right:
            # The query point is the right point of the line segment
            x_diff = line_seg.left.x - query_point.x
            y_diff = line_seg.left.y - query_point.y
        else:
            raise ValueError('Invalid query point!')

        # Move the query point slightly along the segment
        new_query_point.x = query_point.x + x_diff * (0.1 / segment_length)
        new_query_point.y = query_point.y + y_diff * (0.1 / segment_length)

        return new_query_point

    def getQueryResult(self, query_point, line_seg, query_point_existed=False):
        """
        Determines which trapezoid contains the query point.
        """
        assert isinstance(query_point, Point)
        assert isinstance(line_seg, LineSegment)

        # If we are an X-Node (point)
        if isinstance(self.graph_object, Point):
            epsilon = 1e-9  # Tolerance for floating-point comparison
            if query_point.x < self.graph_object.x - epsilon:
                if self.left_child:
                    return self.left_child.getQueryResult(query_point, line_seg, query_point_existed)
                else:
                    raise ValueError('Left child is None.')
            elif query_point.x > self.graph_object.x + epsilon:
                if self.right_child:
                    return self.right_child.getQueryResult(query_point, line_seg, query_point_existed)
                else:
                    raise ValueError('Right child is None.')
            else:
                # Query point x-coordinate is equal to the X-Node's x-coordinate
                new_query_point = self.get_offset_point(query_point, line_seg)
                return self.getQueryResult(new_query_point, line_seg, query_point == self.graph_object)

        # If we are a Y-Node (line segment)
        elif isinstance(self.graph_object, LineSegment):
            if self.left_child is None or self.right_child is None:
                raise ValueError('Child nodes are not properly assigned.')

            if self.graph_object.aboveLine(query_point):
                return self.right_child.getQueryResult(query_point, line_seg, query_point_existed)
            else:
                return self.left_child.getQueryResult(query_point, line_seg, query_point_existed)

        # If we are a leaf node (trapezoid)
        elif isinstance(self.graph_object, Trapezoid):
            return self, query_point_existed

        else:
            raise ValueError('Invalid DAG node!')

    def modify(self, new_node):
        """
        Replaces the contents of the current node with those of new_node.
        """
        assert isinstance(new_node, DAGNode)
        self.graph_object = new_node.graph_object
        self.left_child = new_node.left_child
        self.right_child = new_node.right_child

    def __hash__(self):
        """Override the default hash behavior."""
        return hash(self.id)

    def __eq__(self, other):
        """Override the default Equals behavior."""
        return isinstance(other, DAGNode) and self.id == other.id

    def __repr__(self):
        return '<Node id: %d, left_child: %s, right_child: %s, graph_object: %s>' % (
            self.id,
            self.left_child.graph_object.label if self.left_child else 'NO',
            self.right_child.graph_object.label if self.right_child else 'NO',
            self.graph_object.label if hasattr(self.graph_object, 'label') else str(self.graph_object)
        )
