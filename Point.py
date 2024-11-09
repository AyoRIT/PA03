from GraphObject import GraphObject

class Point(GraphObject):
    def __init__(self, x, y, label=None):
        """
        Initializes a Point with coordinates x and y, and an optional label.
        """
        super().__init__()
        self.x = float(x)  # Convert x to float
        self.y = float(y)  # Convert y to float
        self.label = label  # Assign label if provided

    def __eq__(self, other):
        """
        Overrides the default equality method.
        Points are equal if their x and y coordinates are equal.
        """
        if isinstance(other, self.__class__):
            return self.x == other.x and self.y == other.y
        return NotImplemented

    def __hash__(self):
        """
        Overrides the default hash method.
        Allows Points to be used in sets and as dictionary keys.
        """
        return hash((self.x, self.y))

    def __repr__(self):
        """
        Defines the string representation of the Point.
        """
        return f'({self.x:.2f}, {self.y:.2f})'
