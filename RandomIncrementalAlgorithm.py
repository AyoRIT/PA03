from DAGNode import Point, LineSegment, DAGNode
from DAG import DAG
from Trapezoid import Trapezoid
import random


class RandomizedIncrementalConstruction:
    def __init__(self, segments):
        for segment in segments:
            assert isinstance(segment, LineSegment)
        self.segements = segments
        self.DAG = None
        self.computeDecomposition()

    def computeDecomposition(self):
        self.computeBoundingBox()
        for segment in self.segements:
            self.insert_segment()

    def computeBoundingBox(self, topRightPoint, bottomLeftPoint):
        topRight = topRightPoint
        bottomLeft = bottomLeftPoint

        # Now add the bounding box as a trapezoid
        B = Trapezoid(bottomLeft, topRight,
                      LineSegment(Point(bottomLeft.x, topRight.y), topRight),
                      LineSegment(bottomLeft, Point(topRight.x, bottomLeft.y)))
        
        self.DAG = DAG(DAGNode(B))

    def getIntersectingTrapezoids(self, line_seg):
        assert isinstance(line_seg, LineSegment)
        left_trap = self.DAG.root.getQueryResult(line_seg.left, line_seg)
        right_trap = self.DAG.root.getQueryResult(line_seg.right, line_seg)
        current_trapezoid = left_trap[0].graph_object
        intersecting_trapezoids = [current_trapezoid]

        while current_trapezoid != right_trap[0].graph_object:
            for right_nei in current_trapezoid.right_neighbors:
                if current_trapezoid.right_p != right_nei.left_p:
                    l = LineSegment(current_trapezoid.right_p, right_nei.left_p)
                else:
                    if right_nei.left_p == right_nei.bottom.left:
                        l = right_nei.top
                        y = l.slope * right_nei.left_p.x + l.intercept
                        l = LineSegment(right_nei.left_p, Point(right_nei.left_p.x, y))
                    elif right_nei.left_p == right_nei.top.left:
                        l = right_nei.bottom
                        y = l.slope * right_nei.left_p.x + l.intercept
                        l = LineSegment(Point(right_nei.left_p.x, y), right_nei.left_p)
                    else:
                        l = right_nei.bottom
                        bottom_y = l.slope * right_nei.left_p.x + l.intercept
                        l = right_nei.top
                        top_y = l.slope * right_nei.left_p.x + l.intercept
                        l = LineSegment(Point(right_nei.left_p.x, bottom_y), Point(right_nei.left_p.x, top_y))

                if l.intersects(line_seg):
                    intersecting_trapezoids.append(right_nei)
                    current_trapezoid = right_nei
                    break

        return intersecting_trapezoids, left_trap, right_trap

    def insert_segment(self, segment):
        # assert segment
        assert isinstance(segment, LineSegment)
        
        # find all trapezoids intersected by segment
        intersectingTrapezoids, (leftTrapNode, leftPointExists), (rightTrapNode, rightPointExists) = self.getIntersectingTrapezoids(segment)
        leftTrapezoid, rightTrapezoid = leftTrapNode.graph_object, rightTrapNode.graph_object

        # CASE 1: p and q lie in the same trapezoid
        if len(intersectingTrapezoids) == 1:
            # we always need to split the trapezoid
            newTopTrapezoid = Trapezoid(segment.left, segment.right, leftTrapezoid.top, segment)
            newBottomTrapezoid = Trapezoid(segment.left, segment.right, segment, leftTrapezoid.bottom)

            # if the right point of the segment already existed within the DAG, a right trapezoid would not be created so we have to update the neighbors of the top and bottom trapezoids
            if rightPointExists:
                newBottomTrapezoid.updateLeftNeighbors(leftTrapezoid.right_neighbors)
                newTopTrapezoid.updateRightNeighbors(leftTrapezoid.right_neighbors)
            # else create right trapezoid, set neighbors 
            else:
                newRightTrapezoid = Trapezoid(segment.left, leftTrapezoid.right_p, leftTrapezoid.top, leftTrapezoid.bottom)
                # Set neigbors for new right trapezoid
                newRightTrapezoid.updateLeftNeighbors({newBottomTrapezoid, newTopTrapezoid})
                newRightTrapezoid.updateRightNeighbors(leftTrapezoid.right_neighbors)
            
            # repeat process for left point, left trapezoid
            if leftPointExists:
                newBottomTrapezoid.updateLeftNeighbors(leftTrapezoid.right_neighbors)
                newTopTrapezoid.updateRightNeighbors(leftTrapezoid.right_neighbors)
            else:
                newLeftTrapezoid = Trapezoid(leftTrapezoid.left_p, segment.left, leftTrapezoid.top, leftTrapezoid.bottom)
                # Set neigbors for new left trapezoid
                newLeftTrapezoid.updateLeftNeighbors({newBottomTrapezoid, newTopTrapezoid})
                newRightTrapezoid.updateRightNeighbors(leftTrapezoid.right_neighbors) 

            # create node replacement for trapezoids (see slides for naming conventions, case 2)
            s_node = DAGNode(segment, newTopTrapezoid.node, newBottomTrapezoid.node)
            q_node = DAGNode(segment.right, s_node, newRightTrapezoid)
            p_node = DAGNode(segment.left, newLeftTrapezoid, q_node)
            leftTrapNode.modify(p_node)
        
        else:
            # Divide left trapezoid into bottom, top trapezoids (left trapezoid only exists if leftPoint does not exist)
            newLeftBottomTrapezoid = Trapezoid(segment.left, leftTrapezoid.right_p, segment, leftTrapezoid.bottom)

            # DONT UNDERSTAND
            # newLeftBottomTrapezoid.updateRightNeighbors(
            #     {n for n in leftTrapezoid.right_neighbors if not segment.aboveLine(n.top.right)})

            newLeftTopTrapezoid = Trapezoid(segment.left, leftTrapezoid.right_p, leftTrapezoid.top, segment)
            
            # DONT UNDERSTAND
            # newLeftTopTrapezoid.updateRightNeighbors(
            #     {n for n in leftTrapezoid.right_neighbors if segment.aboveLine(n.bottom.right)})


            if not leftPointExists:
                newLeftTrapezoid = Trapezoid(leftTrapezoid.left_p, segment.left, leftTrapezoid.top, leftTrapezoid.bottom)
                newLeftTrapezoid.updateLeftNeighbors(leftTrapezoid.left_neighbors)
                newLeftTrapezoid.updateRightNeighbors({newLeftTopTrapezoid, newLeftBottomTrapezoid})
            else:
                # update neighbours if right point exists
                newLeftTopTrapezoid.updateLeftNeighbors(leftTrapezoid.left_neighbors)
                newLeftBottomTrapezoid.updateLeftNeighbors(leftTrapezoid.left_neighbors)

            # repeat process for right point trapezoids
            newRightBottomTrapezoid = Trapezoid(rightTrapezoid.left_p, segment.right, segment, rightTrapezoid.bottom)

            # DONT UNDERSTAND
            # newRightBottomTrapezoid.updateLeftNeighbors(
            #     {n for n in rightTrapezoid.left_neighbors if not segment.aboveLine(n.top.right)})

            newRightTopTrapezoid = Trapezoid(rightTrapezoid.left_p, segment.right, rightTrapezoid.top, segment)

            # DONT UNDERSTAND
            # newRightTopTrapezoid.updateLeftNeighbors(
            #     {n for n in rightTrapezoid.left_neighbors if segment.aboveLine(n.bottom.right)})

            if not rightPointExists:
                newRightTrapezoid = Trapezoid(segment.right, rightTrapezoid.right_p, rightTrapezoid.top, rightTrapezoid.bottom)
                newRightTrapezoid.updateLeftNeighbors({newRightTopTrapezoid, newRightBottomTrapezoid})
                newRightTrapezoid.updateRightNeighbors(rightTrapezoid.right_neighbors)
            else:
                newRightTopTrapezoid.updateRightNeighbors(rightTrapezoid.right_neighbors)
                newRightBottomTrapezoid.updateRightNeighbors(rightTrapezoid.right_neighbors)
            
            # Walk to the right along the new segment and split
            # each trapezoid into upper and lower ones
            newTopTrapezoids, newBottomTrapezoids = [newLeftTopTrapezoid], [newLeftBottomTrapezoid]
            trap_dict = dict()
            trap_dict[leftTrapezoid] = (newLeftTopTrapezoid, newLeftBottomTrapezoid)
            for t in intersectingTrapezoids[1:-1]:
                # create new top and bottom trapezoids
                newTopTrapezoid = Trapezoid(t.left_p, t.right_p, t.top, segment)
                newBottomTrapezoid = Trapezoid(t.left_p, t.right_p, segment, t.bottom)
                
                # DONT UNDERSTAND
                # Update neighbors of the new top and bottom
                # for n in t.left_neighbors:
                #     if segment.aboveLine(n.bottom.right):
                #         newTopTrapezoid.updateLeftNeighbors({n})
                #     if not segment.aboveLine(n.top.right):
                #         newBottomTrapezoid.updateLeftNeighbors({n})
                # newTopTrapezoid.updateLeftNeighbors({newTopTrapezoids[-1]})
                # newBottomTrapezoid.updateLeftNeighbors({newBottomTrapezoids[-1]})

                # Add it to the list and dict
                newTopTrapezoids.append(newTopTrapezoid)
                newBottomTrapezoids.append(newBottomTrapezoid)
                trap_dict[t] = (newTopTrapezoid, newBottomTrapezoid)

                # repeat for right top, bottom trapezoids
                newRightTopTrapezoid.updateLeftNeighbors({newTopTrapezoids[-1]})
                newRightBottomTrapezoid.updateLeftNeighbors({newBottomTrapezoids[-1]})
                newTopTrapezoids.append(newRightTopTrapezoid)
                newBottomTrapezoids.append(newRightBottomTrapezoid)
                trap_dict[rightTrapezoid] = (newRightTopTrapezoid, newRightBottomTrapezoid)