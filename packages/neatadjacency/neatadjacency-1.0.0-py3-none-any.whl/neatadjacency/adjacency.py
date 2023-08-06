import abc
import copy
import logging
import random
from operator import attrgetter
from typing import Iterable, Callable, Dict, List, Iterator

from .edge import Edge
from .vertex import Vertex
from sortedcontainers import SortedList
import pickle

log = logging.getLogger(__name__)
log.setLevel(logging.INFO)


class AdjacencyListener(object, metaclass=abc.ABCMeta):
    """
    Listens to events on an AdjacencyList.

    Inherit and override the methods to implement event listeners.
    """

    def on_add(self, shape):
        """Called when a shape is added to the Adjacency List."""
        pass

    def on_update(self, old_shape, new_shape):
        """Called when a shape is updated in the Adjacency List."""
        pass

    def on_remove(self, shape):
        """Called when a shape is removed from the Adjacency List."""
        pass

    def on_group_change(self):
        """
        Called when multiple shapes change in the Adjacency List such as connecting
        edges, moving vertices, etc.
        """
        pass


def _equals_in(items: Iterable, find_item):
    """Return True if find_item is in items using equality check."""
    # Can't use implicit boolean because the returned index could be zero
    return _equals_index(items, find_item) is not None


def _equals_index(items: Iterable, find_item):
    """Return index of item in the list using equality check or None if item is not in list."""
    for i, item in enumerate(items):
        if item == find_item:
            return i
    return None


class AdjacencyList(object):
    """Adjacency list to keep track of edges and vertices."""

    _edges: List[Edge]
    _vertex_edges: Dict
    _on_add: Callable[[Edge], None] = lambda _: None
    _on_remove: Callable[[Edge], None] = lambda _: None
    _on_update: Callable[[Edge, Edge], None] = lambda a, b: None
    _on_group_change: Callable[[], None] = lambda: None

    def __init__(self, listener: AdjacencyListener = None):
        self._edges = []
        self._vertex_edges = {}

        if listener:
            self.set_listener(listener)

    def __bool__(self):
        return True

    def __contains__(self, edge: Edge) -> bool:
        # Searching the for loop is required to get the custom equality check.
        # Edges can be equal without the same identity; "in" operator can't be used.
        return _equals_in(self._edges, edge)

    def __deepcopy__(self, memodict=None):
        """Deep copy will remove any listener on the instance when copying."""
        obj = self.__class__()
        obj._edges = copy.copy(self._edges)
        obj._vertex_edges = copy.copy(self._vertex_edges)
        return obj

    def __len__(self):
        return len(self._edges)

    @classmethod
    def deserialize(cls, load_file, listener=None) -> "AdjacencyList":
        """
        Return a new instance of this class restored from the given serialized version.

        Serialized instances do not have listeners attached. Pass in a new listener
        to attach to the restored instance.
        """
        obj = pickle.load(load_file)
        if listener:
            obj.set_listener(listener)
        return obj

    def add(self, edge: Edge) -> bool:
        """Add an edge."""
        log.debug("Adding edge %s", edge)
        if edge.length < 3:
            log.debug("Short edge %s", edge)
        if edge in self:
            return False
        self._add_to_edges(edge)
        self._vertex_edges.setdefault(edge.start, []).append(edge)
        self._vertex_edges.setdefault(edge.end, []).append(edge)
        self._on_add(edge)
        return True

    def connect_edges(self, edge: Edge, other_edge: Edge):
        """
        Connect the mid-points of the given edges with a new edge.

        Each each will be split into two edges starting/stopping at the midpoint.
        """
        mid1 = self.split_edge(edge)
        mid2 = self.split_edge(other_edge)
        self.add(Edge(mid1, mid2))
        self._on_group_change()

    def connected_edges(self, edge: Edge) -> Iterable[Edge]:
        """Generate all the edges that share a vertex with the given edge."""
        for other_edge in self._vertex_edges[edge.start]:
            if other_edge != edge:
                yield other_edge
        for other_edge in self._vertex_edges[edge.end]:
            if other_edge != edge:
                yield other_edge

    def edges(self, vertex: Vertex = None) -> Iterable[Edge]:
        """
        Generate edges in the adjacency list.

        :param vertex: If given, only edges attached to this vertex are yielded. These
            will not be sorted.
        """
        edge_list = self._edges
        if vertex:
            edge_list = self._vertex_edges[vertex]

        for edge in edge_list:
            yield edge

    def edges_by_length(self) -> List[Edge]:
        """Iterator that returns edges in list from longest to shortest."""
        return sorted(self._edges, key=attrgetter("length"), reverse=True)

    def extend(self, edges: Iterable[Edge]):
        """Add multiple edges."""
        for edge in edges:
            self.add(edge)

    def has_intersection(self, edge: Edge, excluding: Iterable[Edge] = None) -> bool:
        """
        Return True if the given edge intersects with any other edge excluding those
        in the excluding list.
        """
        for current_edge in self._edges:
            if edge.intersects(current_edge) and not _equals_in(
                excluding, current_edge
            ):
                return True
        return False

    def longest_edge(self) -> Edge:
        """Return the longest edge."""
        return self.edges_by_length()[-1]

    def move_vertex(self, vertex: Vertex, new_location: Vertex):
        """
        Move the given vertex to a new location.

        Edges attached to the vertex will be removed and re-created attached
        to the new location.

        The listener on_change method will be called.
        """

        for old_edge in self.edges(vertex):
            new_edge = None

            if old_edge.start == vertex:
                new_edge = Edge(new_location, old_edge.end)

            if old_edge.end == vertex:
                new_edge = Edge(old_edge.start, new_location)

            if new_edge:
                self.remove(old_edge)
                self.add(new_edge)

        self._on_group_change()

    def serialize(self, save_file):
        """
        Return a binary-serialized version of this adjacency list using Pickle.

        Any listeners on the object will be removed before serialization.
        """
        obj = copy.deepcopy(self)
        return pickle.dump(obj, save_file)

    def random_edge(self) -> Edge:
        """Return a random edge from the list."""
        return random.choice(self._edges)

    def remove(self, edge: Edge):
        """Remove an edge."""
        for i, current_edge in enumerate(self._edges):
            if edge == current_edge:
                self._remove(i, current_edge)
                break

    def set_listener(self, listener: AdjacencyListener, add_existing=True):
        """
        Add an AdjacencyListener that will be sent any events from this AdjacencyList.

        :param listener: An :class:`AdjacencyListener` instance.
        :param add_existing: Set to True to call on on_add for every current Edge.
        """
        self._on_add = listener.on_add
        self._on_remove = listener.on_remove
        self._on_update = listener.on_update
        self._on_group_change = listener.on_group_change

        if add_existing:
            log.debug("Calling listener with deserialized edges.")
            for edge in self._edges:
                listener.on_add(edge)
            listener.on_group_change()

    def split_edge(self, edge: Edge, point: Vertex = None) -> Vertex:
        """
        Split an edge at the given point on the edge.

        If no point is given the edge is split on the midpoint.
        """
        if point is None:
            point = edge.midpoint()
        self.remove(edge)
        self.add(Edge(edge.start, point))
        self.add(Edge(point, edge.end))
        return point

    def vertices(self) -> Iterable[Vertex]:
        """Return list of vertices."""
        return self._vertex_edges.keys()

    def unconnected_edges(self) -> Iterator[Edge]:
        """Generate edges that are not connected to any other edge."""
        for edge in self.edges():
            if len(list(self.connected_edges(edge))) == 0:
                yield edge

    def _add_to_edges(self, edge: Edge):
        """
        Add edge to edges collection.

        Sub-classes can override this method to use other container implementations such
        as set(), which requires using add() instead of append().
        """
        self._edges.append(edge)

    def _remove(self, i, edge: Edge):
        """Remove edge including removing vertex lists if necessary."""
        log.debug("Removing edge %s %s", i, edge)

        # Re-assignment of a small list is faster than mutating the list directly
        new_start_list = list(
            filter(lambda item: item != edge, self._vertex_edges.get(edge.start, []))
        )
        if new_start_list:
            self._vertex_edges[edge.start] = new_start_list
        else:
            # There are no other edges with this vertex.
            log.debug("Remove vertex list %s", edge.start)
            try:
                del self._vertex_edges[edge.start]
            except KeyError:
                pass
        # Re-assignment of a small list is faster than mutating the list directly
        new_end_list = list(
            filter(lambda item: item != edge, self._vertex_edges.get(edge.end, []))
        )
        if new_end_list:
            self._vertex_edges[edge.end] = new_end_list
        else:
            # There are no other edges with this vertex.
            log.debug("Remove vertex list %s", edge.start)
            try:
                del self._vertex_edges[edge.end]
            except KeyError:
                pass

        del self._edges[i]
        self._on_remove(edge)


class AdjacencySortedList(AdjacencyList):
    """
    Uses a SortedList to store edges.

    The edges method will return edges sorted by the Edge sort implementation (the start
    vertex).

    This class has addition methods for sweeping over the lines in order.

    The "in" operation and has_intersection method use a line-sweep to improve performance.
    """

    _edges: SortedList
    _edges_by_length: SortedList

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._edges = SortedList()
        self._edges_by_length = SortedList(key=attrgetter("length"))

    def __contains__(self, edge: Edge) -> bool:
        # Searching for the index required to get the custom equality check.
        # Edges can be equal without the same identity; "in" operator can't be used.
        return _equals_in(self.sweep_to(edge), edge)

    def __deepcopy__(self, memodict=None):
        obj = super().__deepcopy__(memodict)
        obj._edges_by_length = self._edges_by_length
        return obj

    def add(self, edge: Edge):
        """Add an edge."""
        if super().add(edge):
            self._edges_by_length.add(edge)
            return True
        return False

    def edges_by_length(self) -> Iterator[Edge]:
        """Iterator that returns edges in list from longest to shortest."""
        return reversed(self._edges_by_length)

    def remove(self, edge: Edge):
        super().remove(edge)
        i = _equals_index(self._edges_by_length, edge)
        if i:
            del self._edges_by_length[i]

    def has_intersection(self, edge: Edge, excluding: Iterable[Edge] = None) -> bool:
        """
        Return True if the given edge intersects with any other edge excluding those
        in the excluding list.
        """
        for current_edge in self.sweep_left(edge):
            if edge.intersects(current_edge) and not _equals_in(
                excluding, current_edge
            ):
                return True
        return False

    def sweep_centered(self, from_edge: Edge) -> Iterable[Edge]:
        """
        Yield edges starting from the given edge moving outward in both X directions.

        :param from_edge: Edge to start from. This is not included in the values.
        """
        li = self._edges.bisect_left(from_edge)
        ri = self._edges.bisect_right(from_edge)
        maxi = len(self._edges) - 1

        while li >= 0 or ri <= maxi:
            if li >= 0:
                yield self._edges[li]
            if ri <= maxi:
                yield self._edges[ri]

            li -= 1
            ri += 1

    def sweep_to(self, to_edge: Edge) -> Iterable[Edge]:
        """
        Yield edges in order starting from lowest start.x to to_edge.end.x
        """
        for edge in self.edges():
            # edge.end is always to the right of edge.start as
            # part of Edge implementation.
            if edge.start.x > to_edge.end.x:
                return
            yield edge

    def sweep_left(self, from_edge: Edge) -> Iterable[Edge]:
        """
        Yield edges in reverse order from from_edge.end to the first edge.
        """
        # edge.start has to be lower (x,y) value for bisect_right below
        # and we need to bisect on from_edge.end
        furthest = Edge(from_edge.end, Vertex(from_edge.end.x + 1, from_edge.end.x + 1))
        li = self._edges.bisect_right(furthest)

        for i in reversed(range(li)):
            yield self._edges[i]

    def _add_to_edges(self, edge: Edge):
        self._edges.add(edge)
