from Point import Point
from LineSegment import LineSegment
from GraphObject import GraphObject
from DAGNode import DAGNode

class Trapezoid(GraphObject):
    def __init__(self, left_p, right_p, top, bottom, label=None):
        super().__init__()
        assert isinstance(left_p, Point) and isinstance(right_p, Point), 'left_p and/or right_p is not a point'
        assert isinstance(top, LineSegment) and isinstance(bottom, LineSegment), 'top and/or bottom is not a line segment'
        self.left_p = left_p
        self.right_p = right_p
        self.top = top
        self.bottom = bottom
        self.left_neighbors = set()
        self.right_neighbors = set()
        self._node = DAGNode(self)
        self.label = label  # Label is assigned externally

    @property
    def node(self):
        return self._node

    @node.setter
    def node(self, node):
        self._node.modify(node)

    def updateLeftNeighbors(self, neighbors, auto=False):
        for n in neighbors:
            assert isinstance(n, Trapezoid)
            # If the neighbor already exists or it's not directly adjacent, skip
            if n in self.left_neighbors or self.left_p.x != n.right_p.x:
                continue
            self.left_neighbors.add(n)
            if not auto:
                n.updateRightNeighbors({self}, auto=True)

    def updateRightNeighbors(self, neighbors, auto=False):
        for n in neighbors:
            assert isinstance(n, Trapezoid)
            # If the neighbor already exists or it's not directly adjacent, skip
            if n in self.right_neighbors or self.right_p.x != n.left_p.x:
                continue
            self.right_neighbors.add(n)
            if not auto:
                n.updateLeftNeighbors({self}, auto=True)

    def __hash__(self):
        return super().__hash__()

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.left_p == other.left_p and self.right_p == other.right_p \
                   and self.top == other.top and self.bottom == other.bottom
        return super().__eq__(other)

    def __ne__(self, other):
        if isinstance(other, self.__class__):
            return not self == other
        return NotImplemented

    def __repr__(self):
        return '<Trapezoid %s left_p:%s right_p:%s top:%s bottom:%s>' % (
            self.label if self.label else '',
            str(self.left_p), str(self.right_p), str(self.top), str(self.bottom))
