import math
from Point import Point
from GraphObject import GraphObject


class LineSegment(GraphObject):
    def __init__(self, left, right, label=None):
        super().__init__()
        assert isinstance(left, Point) and isinstance(right, Point)
        # Ensure left is the leftmost point
        if left.x < right.x:
            self.left = left
            self.right = right
        elif left.x > right.x:
            self.left = right
            self.right = left
        else:
            # If x coordinates are equal, compare y
            if left.y < right.y:
                self.left = left
                self.right = right
            else:
                self.left = right
                self.right = left
        self.isVertical = (self.left.x == self.right.x)
        self.label = label  # Label assigned externally

    @property
    def length(self):
        return math.hypot(self.right.x - self.left.x, self.right.y - self.left.y)

    @property
    def slope(self):
        if self.isVertical:
            return None
        else:
            return (self.right.y - self.left.y) / (self.right.x - self.left.x)

    @property
    def intercept(self):
        if self.isVertical:
            return None
        else:
            return self.left.y - self.slope * self.left.x

    def get_Y(self, x):
        if self.isVertical:
            raise ValueError("Cannot compute Y for a vertical line")
        else:
            return self.slope * x + self.intercept

    @staticmethod
    def on_segment(p, q, r):
        return (min(p.x, r.x) <= q.x <= max(p.x, r.x) and
                min(p.y, r.y) <= q.y <= max(p.y, r.y))

    @staticmethod
    def ccw(p, q, r) -> int:
        val = (q.y - p.y) * (r.x - q.x) - (q.x - p.x) * (r.y - q.y)
        if val == 0:
            return 0  # Colinear
        elif val > 0:
            return 1  # Counter-clockwise
        else:
            return -1  # Clockwise

    def aboveLine(self, point) -> bool:
        if self.isVertical:
            raise ValueError("Above line is not defined for vertical segments")
        v1x = self.right.x - self.left.x
        v1y = self.right.y - self.left.y
        v2x = point.x - self.left.x
        v2y = point.y - self.left.y
        xp = v1x * v2y - v1y * v2x
        return xp > 0  # True if point is above the line

    def intersects(self, other) -> bool:
        assert isinstance(other, LineSegment)

        # Check if they share an endpoint
        if self.left == other.left or self.right == other.right or \
           self.left == other.right or self.right == other.left:
            return False

        o1 = self.ccw(self.left, self.right, other.left)
        o2 = self.ccw(self.left, self.right, other.right)
        o3 = self.ccw(other.left, other.right, self.left)
        o4 = self.ccw(other.left, other.right, self.right)

        # General case
        if o1 != o2 and o3 != o4:
            return True

        # Special cases
        if o1 == 0 and self.on_segment(self.left, other.left, self.right): return True
        if o2 == 0 and self.on_segment(self.left, other.right, self.right): return True
        if o3 == 0 and self.on_segment(other.left, self.left, other.right): return True
        if o4 == 0 and self.on_segment(other.left, self.right, other.right): return True

        return False

    def belowOther(self, other) -> bool:
        return other.aboveLine(self.left) and other.aboveLine(self.right)

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.left == other.left and self.right == other.right
        return NotImplemented

    def __hash__(self):
        return hash((self.left, self.right))

    def __repr__(self):
        return f'<Segment left:{self.left} right:{self.right}>'
