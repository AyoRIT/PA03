from DAGNode import Point, LineSegment, DAGNode
from DAG import DAG
from Trapezoid import Trapezoid
import random


class RandomizedIncrementalConstruction:
    def __init__(self, segments):
        """
        Initializes the Randomized Incremental Construction algorithm.
        """
        for segment in segments:
            assert isinstance(segment, LineSegment)
        self.segments = segments
        self.DAG = None
        self.new_trapezoids = []
        self.trapezoid_counter = 2  # Start from 2 since T1 is used for the bounding box

    def computeBoundingBox(self, bottomLeftPoint, topRightPoint):
        bottomLeft = bottomLeftPoint
        topRight = topRightPoint

        top_segment = LineSegment(Point(bottomLeft.x, topRight.y), topRight, label='S0')
        bottom_segment = LineSegment(bottomLeft, Point(topRight.x, bottomLeft.y), label='S0')

        B = Trapezoid(bottomLeft, topRight, top_segment, bottom_segment, label='T1')

        self.DAG = DAG(DAGNode(B))
        self.trapezoid_counter = 2

    def computeDecomposition(self, bottomLeftPoint, topRightPoint):
        self.computeBoundingBox(bottomLeftPoint, topRightPoint)

        for segment in self.segments:
            self.insert_segment(segment)

    def getIntersectingTrapezoids(self, line_seg):
        assert isinstance(line_seg, LineSegment)

        # Find the trapezoid containing the left endpoint of the segment
        left_trap_node = self.DAG.root.query(line_seg.left)
        left_trap = left_trap_node.graph_object
        left_point_exists = (line_seg.left == left_trap.left_p or line_seg.left == left_trap.right_p)

        # Find the trapezoid containing the right endpoint of the segment
        right_trap_node = self.DAG.root.query(line_seg.right)
        right_trap = right_trap_node.graph_object
        right_point_exists = (line_seg.right == right_trap.left_p or line_seg.right == right_trap.right_p)

        # Initialize the list of intersecting trapezoids
        intersecting_trapezoids = []
        current_trapezoid = left_trap

        while True:
            intersecting_trapezoids.append(current_trapezoid)
            if current_trapezoid == right_trap:
                break

            # Move to the next trapezoid to the right
            next_trap = None
            for neighbor in current_trapezoid.right_neighbors:
                # Check if the neighbor is to the right of the current trapezoid
                if neighbor.left_p.x >= current_trapezoid.right_p.x:
                    next_trap = neighbor
                    break

            if next_trap is not None:
                current_trapezoid = next_trap
            else:
                # Handle cases where there is no right neighbor
                # You can choose to break or raise an exception
                # For now, we'll break the loop
                break

        return intersecting_trapezoids, (left_trap_node, left_point_exists), (right_trap_node, right_point_exists)

    def insert_segment(self, segment):
        # Assert segment is a LineSegment instance
        assert isinstance(segment, LineSegment)

        # Initialize the list to keep track of new trapezoids created in this insertion
        self.new_trapezoids = []

        # Find all trapezoids intersected by the segment
        intersectingTrapezoids, (leftTrapNode, leftPointExists), (
            rightTrapNode, rightPointExists) = self.getIntersectingTrapezoids(segment)
        leftTrapezoid, rightTrapezoid = leftTrapNode.graph_object, rightTrapNode.graph_object

        # Dictionaries to keep track of new trapezoids for neighbor updates
        trap_dict = {}

        # CASE 1: The segment lies completely within one trapezoid
        if len(intersectingTrapezoids) == 1:
            D = leftTrapezoid  # Only one trapezoid intersected

            # Create new trapezoids
            # Left trapezoid (if needed)
            if not leftPointExists and segment.left.x > D.left_p.x:
                left_trap = Trapezoid(D.left_p, segment.left, D.top, D.bottom)
                left_node = DAGNode(left_trap)
                self.new_trapezoids.append(left_trap)
            else:
                left_trap = None
                left_node = None

            # Right trapezoid (if needed)
            if not rightPointExists and segment.right.x < D.right_p.x:
                right_trap = Trapezoid(segment.right, D.right_p, D.top, D.bottom)
                right_node = DAGNode(right_trap)
                self.new_trapezoids.append(right_trap)
            else:
                right_trap = None
                right_node = None

            # Top middle trapezoid
            top_trap = Trapezoid(segment.left, segment.right, D.top, segment)
            top_node = DAGNode(top_trap)
            self.new_trapezoids.append(top_trap)

            # Bottom middle trapezoid
            bottom_trap = Trapezoid(segment.left, segment.right, segment, D.bottom)
            bottom_node = DAGNode(bottom_trap)
            self.new_trapezoids.append(bottom_trap)

            # Update neighbors
            if left_trap:
                left_trap.right_neighbors = {top_trap, bottom_trap}
                top_trap.left_neighbors = {left_trap}
                bottom_trap.left_neighbors = {left_trap}
                trap_dict[left_trap] = left_node
            else:
                top_trap.left_neighbors = D.left_neighbors
                bottom_trap.left_neighbors = D.left_neighbors

            if right_trap:
                right_trap.left_neighbors = {top_trap, bottom_trap}
                top_trap.right_neighbors = {right_trap}
                bottom_trap.right_neighbors = {right_trap}
                trap_dict[right_trap] = right_node
            else:
                top_trap.right_neighbors = D.right_neighbors
                bottom_trap.right_neighbors = D.right_neighbors

            trap_dict[top_trap] = top_node
            trap_dict[bottom_trap] = bottom_node

            # Build the DAG nodes
            s_node = DAGNode(segment, top_node, bottom_node)
            if right_node:
                q_node = DAGNode(segment.right, s_node, right_node)
            else:
                q_node = DAGNode(segment.right, s_node, None)
            if left_node:
                p_node = DAGNode(segment.left, left_node, q_node)
            else:
                p_node = DAGNode(segment.left, None, q_node)

            # Replace the old trapezoid's node in the DAG
            D.node.modify(p_node)

        else:
            # CASE 2: The segment spans multiple trapezoids

            # Process leftmost trapezoid
            D0 = leftTrapezoid

            if not leftPointExists and segment.left.x > D0.left_p.x:
                left_trap = Trapezoid(D0.left_p, segment.left, D0.top, D0.bottom)
                left_node = DAGNode(left_trap)
                trap_dict[left_trap] = left_node
                self.new_trapezoids.append(left_trap)
            else:
                left_trap = None
                left_node = None

            left_top_trap = Trapezoid(segment.left, D0.right_p, D0.top, segment)
            left_bottom_trap = Trapezoid(segment.left, D0.right_p, segment, D0.bottom)
            left_top_node = DAGNode(left_top_trap)
            left_bottom_node = DAGNode(left_bottom_trap)
            self.new_trapezoids.extend([left_top_trap, left_bottom_trap])
            trap_dict[left_top_trap] = left_top_node
            trap_dict[left_bottom_trap] = left_bottom_node

            # Update neighbors for left trapezoids
            if left_trap:
                left_trap.right_neighbors = {left_top_trap, left_bottom_trap}
                left_top_trap.left_neighbors = {left_trap}
                left_bottom_trap.left_neighbors = {left_trap}
            else:
                left_top_trap.left_neighbors = D0.left_neighbors
                left_bottom_trap.left_neighbors = D0.left_neighbors

            # Process rightmost trapezoid
            Dk = rightTrapezoid

            if not rightPointExists and segment.right.x < Dk.right_p.x:
                right_trap = Trapezoid(segment.right, Dk.right_p, Dk.top, Dk.bottom)
                right_node = DAGNode(right_trap)
                trap_dict[right_trap] = right_node
                self.new_trapezoids.append(right_trap)
            else:
                right_trap = None
                right_node = None

            right_top_trap = Trapezoid(Dk.left_p, segment.right, Dk.top, segment)
            right_bottom_trap = Trapezoid(Dk.left_p, segment.right, segment, Dk.bottom)
            right_top_node = DAGNode(right_top_trap)
            right_bottom_node = DAGNode(right_bottom_trap)
            self.new_trapezoids.extend([right_top_trap, right_bottom_trap])
            trap_dict[right_top_trap] = right_top_node
            trap_dict[right_bottom_trap] = right_bottom_node

            # Update neighbors for right trapezoids
            if right_trap:
                right_trap.left_neighbors = {right_top_trap, right_bottom_trap}
                right_top_trap.right_neighbors = {right_trap}
                right_bottom_trap.right_neighbors = {right_trap}
            else:
                right_top_trap.right_neighbors = Dk.right_neighbors
                right_bottom_trap.right_neighbors = Dk.right_neighbors

            # Process middle trapezoids
            prev_top_trap = left_top_trap
            prev_bottom_trap = left_bottom_trap

            for t in intersectingTrapezoids[1:-1]:
                # Create new top and bottom trapezoids
                top_trap = Trapezoid(t.left_p, t.right_p, t.top, segment)
                bottom_trap = Trapezoid(t.left_p, t.right_p, segment, t.bottom)
                top_node = DAGNode(top_trap)
                bottom_node = DAGNode(bottom_trap)
                self.new_trapezoids.extend([top_trap, bottom_trap])
                trap_dict[top_trap] = top_node
                trap_dict[bottom_trap] = bottom_node

                # Update neighbors
                top_trap.left_neighbors = {prev_top_trap}
                bottom_trap.left_neighbors = {prev_bottom_trap}
                prev_top_trap.right_neighbors = {top_trap}
                prev_bottom_trap.right_neighbors = {bottom_trap}

                # Right neighbors inherit from the original trapezoid
                top_trap.right_neighbors = t.right_neighbors
                bottom_trap.right_neighbors = t.right_neighbors

                # Create segment node
                s_node = DAGNode(segment, top_node, bottom_node)

                # Replace the old trapezoid's node in the DAG
                t.node.modify(s_node)

                # Update previous traps for next iteration
                prev_top_trap = top_trap
                prev_bottom_trap = bottom_trap

            # Connect last middle trapezoids to rightmost trapezoids
            right_top_trap.left_neighbors = {prev_top_trap}
            right_bottom_trap.left_neighbors = {prev_bottom_trap}
            prev_top_trap.right_neighbors = {right_top_trap}
            prev_bottom_trap.right_neighbors = {right_bottom_trap}

            # Build the DAG nodes for leftmost trapezoid
            s_node_left = DAGNode(segment, left_top_node, left_bottom_node)
            if left_node:
                p_node = DAGNode(segment.left, left_node, s_node_left)
            else:
                p_node = DAGNode(segment.left, None, s_node_left)
            D0.node.modify(p_node)

            # Build the DAG nodes for rightmost trapezoid
            s_node_right = DAGNode(segment, right_top_node, right_bottom_node)
            if right_node:
                q_node = DAGNode(segment.right, s_node_right, right_node)
            else:
                q_node = DAGNode(segment.right, s_node_right, None)
            Dk.node.modify(q_node)

            # Update neighbor relationships for rightmost trapezoids
            if right_trap:
                right_trap.left_neighbors = {right_top_trap, right_bottom_trap}
                trap_dict[right_trap] = right_node

        for trap in self.new_trapezoids:
            if not hasattr(trap, 'label'):
                trap.label = f'T{self.trapezoid_counter}'
                self.trapezoid_counter += 1
