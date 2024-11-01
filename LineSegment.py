import math
from Point import Point
from GraphObject import GraphObject


class LineSegment(GraphObject):

    def __init__(self, left, right):
        super().__init__()
        assert isinstance(left, Point) and isinstance(right, Point)
        # we want to make sure left is always the leftmost point
        if left.x < right.x:
            self.left = left
            self.right = right
        elif left.x > left.x:
            self.left = right
            self.right = left
        else:
            if left.y < right.y:
                self.left = left
                self.right = right
            else:
                self.left = right
                self.right = left

        if left.x == right.x:
            self.isVertical = True
        else:
            self.isVertical = False

    @property
    def len(self):
        return math.pow(self.right.x - self.left.x, 2) + math.pow(self.right.y - self.left.y, 2)

    @property
    def slope(self):
        return None if self.isVertical else (self.right.y - self.left.y) / (self.right.x - self.left.x)

    @property
    def intercept(self):
        return self.left.y - self.slope * self.left.x

    @property
    def get_Y(self, x):
        return Point(x, self.slope * x + self.intercept)

    @staticmethod
    # Check if point q lies on segment p -> r
    def on_segment(p, q, r):
        assert isinstance(p, Point) and isinstance(q, Point) and isinstance(r, Point)
        return min(p.x, r.x) <= q.x <= max(p.x, r.x) and min(p.y, r.y) <= q.y <= max(p.y, r.y)

    @staticmethod
    # Check if pqr is counter-clockwise
    def ccw(p, q, r) -> int:
        assert isinstance(p, Point) and isinstance(q, Point) and isinstance(r, Point)
        val = (q.y - p.y) * (r.x - q.x) - (q.x - p.x) * (r.y - q.y)

        # this shows that the points are collinear
        if val == 0:
            return 0

        # -1 for clockwise
        #  1 for counter-clockwise
        return -1 if val > 0 else 1

    def aboveLine(self, point) -> bool:
        # Return true if point lies above line segment 'self'.
        assert isinstance(point, Point)
        if self.isVertical:
            raise ValueError("Above line is not defined for Vertical segments")
        v1x = self.right.x - self.left.x  
        v1y = self.right.y - self.left.y  
        v2x = self.right.x - point.x  
        v2y = self.right.y - point.y 
        xp = v1x * v2y - v1y * v2x  # Cross product
        # when its larger than zero, return false
        # so we assume that if it lies on the line that it is "above"
        if xp > 0:
            return False
        else:
            return True

    def intersects(self, other) -> bool:
        assert isinstance(other, LineSegment)

        # check if they share an endpoint
        if self.left == other.left or self.right == other.right or self.left == other.right or self.right == other.left:
            return False

        o1 = self.ccw(self.left, self.right, other.left)
        o2 = self.ccw(self.left, self.right, other.right)
        o3 = self.ccw(other.left, other.right, self.left)
        o4 = self.ccw(other.left, other.right, self.right)

        # General case
        if o1 != o2 and o3 != o4:
            return True

        # Special cases
        # A, B and C are colinear and C lies on segment AB
        if o1 == 0 and self.on_segment(self.left, other.left, self.right): return True

        # A, B and C are colinear and D lies on segment AB
        if o2 == 0 and self.on_segment(self.left, other.right, self.right): return True

        # C, D and A are colinear and A lies on segment CD
        if o3 == 0 and self.on_segment(other.left, self.left, other.right): return True

        # C, D and B are colinear and B lies on segment CD
        if o4 == 0 and self.on_segment(other.left, self.right, other.right): return True

        return False

    def belowOther(self, other) -> bool:
        # if both points of other segment is not above us, then segment is below us
        if self.aboveLine(other.left) and self.aboveLine(other.right):
            return True

        if not other.aboveLine(self.left) and not other.aboveLine(self.right):
            return True

        
        return False

    def __hash__(self):
        return super().__hash__()

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.__dict__ == other.__dict__
        return NotImplemented

    def __ne__(self, other):
        if isinstance(other, self.__class__):
            return not self == other
        return NotImplemented

    def __lt__(self, other):
        # returns if self is below the other line segment
        return self.belowOther(other)

    def __gt__(self, other):
        # returns if self is above the other line segment
        return not self.belowOther(other)

    def __repr__(self):
        return '<Segment left:%s right:%s>' % (str(self.left), str(self.right))