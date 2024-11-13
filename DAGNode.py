import copy

from GraphObject import GraphObject
from Point import Point
from LineSegment import LineSegment
import Trapezoid


class DAGNode:


    def __init__(self, graph_object, left_child=None, right_child=None):
        # we use graph object to enure each node is either a point, a segment, or a trapezoid
        assert isinstance(graph_object, GraphObject)
        self.graph_object = graph_object
        self.left_child = left_child
        self.right_child = right_child
    
    # special case where we insert a segment with an end point already in the DAG graph, we simply get a new point by moving along the line segment by a small fraction and use that point for querying instead
    def get_offset_point(self, query_point, line_seg) -> Point:
        assert isinstance(query_point, Point)
        assert isinstance(line_seg, LineSegment)

        new_query_point = copy.copy(query_point)
        if query_point == line_seg.left:
            # the query point is the left point of the line segment
            x_diff = (line_seg.right.x - query_point.x)
            y_diff = (line_seg.right.y - query_point.y)
        elif query_point == line_seg.right:
            # the query point is the right point of the line segment
            x_diff = (line_seg.left.x - query_point.x)
            y_diff = (line_seg.left.y - query_point.y)
        else:
            raise ValueError('Invalid query point!')

        # (p2.x - p1.x) * t --> xDiff * t
        new_query_point.x = query_point.x + x_diff * (0.1 / line_seg.len)

        # (p2.y - p1.y) * t --> yDiff * t
        new_query_point.y = query_point.y + y_diff * (0.1 / line_seg.len)

        return new_query_point

    def getQueryResult(self, query_point, line_seg, query_point_existed=False):
        # function to determine what trapezoid we are in, when we receive a line segment end points
        assert isinstance(query_point, Point)
        assert isinstance(line_seg, LineSegment)

        # if we are an X-Node (point), then we want to check if query point is to our right or our left
        if isinstance(self.graph_object, Point):
            # if the query point is to our left, we traverse the graph by going into our left child
            if query_point.x < self.graph_object.x:
                return self.left_child.getQueryResult(query_point, line_seg, query_point_existed)
            # if the query point is to our right, we traverse the graph by going into our right child
            elif query_point.x > self.graph_object.x:
                return self.right_child.getQueryResult(query_point, line_seg, query_point_existed)
            # if the query point is equal to us, we develop new query point as mentioned above in get_offset_point and use the new point to figure out what trapezoid we are in  
            else:
                new_query_point = self.get_offset_point(query_point, line_seg)
                return self.getQueryResult(new_query_point, line_seg, query_point == self.graph_object)

        # if we are a Y-Node, 
        elif isinstance(self.graph_object, LineSegment):
            # traverse tree by checking above and going right if point is found, or 
            if self.graph_object.aboveLine(query_point):
                return self.left_child.getQueryResult(query_point, line_seg, query_point_existed)
            # going left if point isn't above. 
            else:
                return self.right_child.getQueryResult(query_point, line_seg, query_point_existed)

        # we are a leaf node
        elif isinstance(self.graph_object, Trapezoid.Trapezoid):
            return self, query_point_existed

        # We are neither a point, line or trapezoid
        else:
            raise ValueError('invalid DAG node!')

    def modify(self, new_node):
        assert isinstance(new_node, DAGNode)
        self.graph_object = new_node.graph_object
        self.left_child = new_node.left_child
        self.right_child = new_node.right_child

    def __hash__(self):
        """Override the default hash behavior (that returns the id or the object)"""
        return hash(str(self))

    def __eq__(self, other):
        """Override the default Equals behavior"""
        if isinstance(other, self.__class__):
            return self.graph_object == other.graph_object \
                   and self.left_child is other.left_child \
                   and self.right_child is other.right_child
        return NotImplemented

    def __ne__(self, other):
        """Define a non-equality test"""
        if isinstance(other, self.__class__):
            return not self == other
        return NotImplemented

    def __repr__(self):
        return 'Node GRAPH_OBJECT: %s \nleft_child: %s \nright_child: %s \n' % (
            self.graph_object,
            self.left_child.graph_object if self.left_child else 'None',
            self.right_child.graph_object if self.right_child else 'None')