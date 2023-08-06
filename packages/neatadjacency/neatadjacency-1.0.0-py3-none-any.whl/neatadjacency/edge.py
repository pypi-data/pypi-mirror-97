import math
from typing import Union

from .shape import Shape
from .vertex import Vertex


def ccw(p1, p2, p3):
    return (p3.y - p1.y) * (p2.x - p1.x) > (p2.y - p1.y) * (p3.x - p1.x)


class Edge(Shape):
    """
    An edge represents a line. It has a start and end vertex and useful methods
    for operating on a line.
    """
    __slots__ = ("start", "end")
    start: Vertex
    end: Vertex

    def __init__(self, start: Vertex, end: Vertex):
        """
        The start vertex will always be the top/left one. Even if they are given
        in a different order.

        :param start: Start Vertex.
        :param end: End Vertex.
        """
        # Start is always top/left
        if end < start:
            self.start = end
            self.end = start
        else:
            self.start = start
            self.end = end

    def __gt__(self, other):
        return self.start > other.start

    def __lt__(self, other):
        return self.start < other.start

    def __eq__(self, other):
        return self.start == other.start and self.end == other.end

    def __hash__(self):
        return hash((self.start, self.end))

    def __json__(self, *args, **kwargs):
        return {
            "type": "line",
            "start": {"x": self.start.x, "y": self.start.y},
            "end": {"x": self.end.x, "y": self.end.y},
        }

    def __str__(self):
        return f"<Edge start={self.start} end={self.end}>"

    @property
    def length(self) -> float:
        """
        The length of the edge.

        len() can't be used because length is a float.
        """
        return math.sqrt(
            math.pow(self.end.x - self.start.x, 2)
            + math.pow(self.end.y - self.start.y, 2)
        )

    def angle_degrees(self, other: "Edge") -> float:
        """
        Return the angle between this edge and the other edge in degrees.

        :param other:
        :return: Angle in degrees. Will always be between 0 and 180
        """
        theta1 = math.atan2(self.start.y - self.end.y, self.start.x - self.end.x)

        theta2 = math.atan2(other.start.y - other.end.y, other.start.x - other.end.x)
        radians = abs(theta1 - theta2)
        degrees = radians * (180 / math.pi)
        return min(degrees, abs(180 - degrees))

    def copy(self) -> "Edge":
        """Return a new Edge instance copied from this one."""
        return Edge(self.start, self.end)

    def intersects(self, other: "Edge") -> bool:
        """Return True if the other edge intersects this one."""
        p1 = self.start
        p2 = self.end
        p3 = other.start
        p4 = other.end

        return ccw(p1, p3, p4) != ccw(p2, p3, p4) and ccw(p1, p2, p3) != ccw(p1, p2, p4)

    def intersection_point(self, other: "Edge") -> Union[Vertex, bool]:
        """
        Return the vertex where this edge and the other intersect.

        Returns None if there is no intersection. This is slower than using
        :meth:`intersects`.
        """
        x1 = self.start.x
        x2 = self.end.x
        y1 = self.start.y
        y2 = self.end.y

        x3 = other.start.x
        x4 = other.end.x
        y3 = other.start.y
        y4 = other.end.y

        s1_x = x2 - x1
        s2_x = x4 - x3
        s1_y = y2 - y1
        s2_y = y4 - y3

        s = (-s1_y * (x1 - x3) + s1_x * (y1 - y3)) / (-s2_x * s1_y + s1_x * s2_y)
        t = (s2_x * (y1 - y3) - s2_y * (x1 - x3)) / (-s2_x * s1_y + s1_x * s2_y)

        if 0 <= s <= 1 and 0 <= t <= 1:
            xi = x1 + t * s1_x
            yi = y1 + t * s1_y

            return Vertex(round(xi), round(yi))

        return False

    def is_parallel(self, other: "Edge") -> bool:
        """Return True if the other edge is parallel to this one."""
        return self.angle_degrees(other) in (0, 180)

    def midpoint(self) -> Vertex:
        """Return the midpoint along this edge."""
        return Vertex(
            round((self.start.x + self.end.x) / 2),
            round((self.start.y + self.end.y) / 2),
        )

    def common_vertex(self, other: "Edge") -> Union[bool, Vertex]:
        """
        If this Edge has a start or end vertex in common with the given edge, then
        return that Vertex.

        Otherwise return False.
        """
        if self.start == other.start or self.start == other.end:
            return self.start
        elif self.end == other.start or self.end == other.end:
            return self.end
        return False

    def slope(self) -> float:
        "Return the slope of this edge."
        return (self.start.y - self.end.y) / (self.start.x - self.end.x)
