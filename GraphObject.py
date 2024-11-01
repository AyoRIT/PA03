class GraphObject:
    def __init__(self):
        pass

    def __hash__(self):
        return hash(str(self))