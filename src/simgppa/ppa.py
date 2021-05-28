from __future__ import annotations

from queue import PriorityQueue, Queue
from typing import Any, List, NewType, Optional, Set


Vertex = NewType('Vertex', int)


class Edge:

    def __init__(self, start: int, end: int, capacity: int) -> None:
        self.start = start
        self.end = end
        self.capacity = capacity


class VertexEdges:

    def __init__(self,
                 vertex: Vertex,
                 capacity: int,
                 pair: Optional[VertexEdges] = None) -> None:

        self.vertex = vertex
        self.capacity = capacity
        self.pair = pair


class AdjacencyList:
    '''Adjacency List'''

    def __init__(self) -> None:

        self.edges: List[VertexEdges] = []

    def get_capacity(self, vertex: Vertex) -> Optional[int]:

        for edge in self.edges:
            if edge.vertex == vertex:
                return edge.capacity
        return None

    def set_capacity(self, vertex: Vertex, capacity: int) -> None:

        for edge in self.edges:
            if edge.vertex == vertex:
                edge.capacity = capacity
                return

        # TODO replace with custom exception
        raise ValueError("Attempt to set capacity of non-existent edge")

    def get_edge(self, vertex: Vertex) -> Optional[VertexEdges]:

        for edge in self.edges:
            if edge.vertex == vertex:
                return edge
        return None

    def add_edge(self, vertex: Vertex, capacity: int) -> None:

        self.edges.append(VertexEdges(vertex, capacity))


class PPA:

    def __init__(self,
                 vertex_num: int,
                 edges: List[Edge],
                 flow: Optional[List[Edge]] = None) -> None:

        # preparing basic vars for calculation
        self.__maxflow = None
        self.__mincut = None
        self.__edge_num = len(edges)
        self.__vertex_num = vertex_num
        self.__source: Vertex = 0
        self.__runoff: Vertex = self.__vertex_num - 1

        # vertex queue for high level optimization
        self.__vertex_queue: PriorityQueue[Vertex] = PriorityQueue()
        self.__vertex_in_queue: List[bool] = [False for _ in range(
            self.__vertex_num)]

        # list of heights for vertices
        self.__height: List[int] = \
            [self.__vertex_num] + \
            [2 * self.__vertex_num for _ in range(self.__vertex_num - 2)] + \
            [0]

        # list of excess for vertices
        self.__excess: List[int] = [0 for _ in range(self.__vertex_num)]

        # list of residual capacities
        self.__als: List[AdjacencyList] = [AdjacencyList()
                                           for _ in range(self.__vertex_num)]

        # converting edges to als
        for edge in edges:
            ve: Optional[VertexEdges] = self.__als[edge.start] \
                .get_edge(edge.end)

            if ve is None:
                self.__als[edge.start].add_edge(edge.end, edge.capacity)
                ve = self.__als[edge.start].edges[-1]

                self.__als[edge.end].add_edge(edge.start, 0)
                to = self.__als[edge.end].edges[-1]

                ve.pair = to
                to.to = ve
            else:
                ve.capacity = edge.capacity

        # merge flow results
        if flow is not None:
            for edge in flow:
                ve: VertexEdges = self.__als[edge.start].get_edge(edge.end)
                ve.capacity -= edge.capacity
                ve.pair.capacity += edge.capacity

                if edge.pair == self.__runoff:
                    self.__excess[self.__runoff] += edge.capacity

        # initialization excess and queue of vertices
        for edge in self.__als[self.__source].edges:
            self.__excess[edge.vertex] = edge.capacity
            self.__als[edge.vertex].set_capacity(self.__source, edge.capacity)
            edge.capacity = 0

            # put vertex to queue
            self.__vertex_queue.put((0, edge.vertex))
            self.__vertex_in_queue[edge.vertex] = True

        # perform global relabling before execution
        self.__gr_counter = self.__vertex_num + self.__edge_num - 1
        self.__relabel()

    def __relabel(self) -> None:

        self.__gr_counter += 1
        if self.__gr_counter == self.__vertex_num + self.__edge_num - 1:
            self.__gr_counter = 0
            checked: List[bool] = \
                [True] + \
                [False for _ in range(self.__vertex_num - 2)] + \
                [True]

            self.__heightened_distance(self.__runoff, checked)
            self.__heightened_distance(self.__source, checked)

    def __heightened_distance(self, vertex: Vertex, checked: List[bool]) -> None:
        to_check: Queue[Vertex] = Queue()
        to_check.put(vertex)

        while not to_check.empty():

            vertex = to_check.get()

            for edge in self.__als[vertex].edges:

                if edge.pair.capacity > 0 and not checked[edge.vertex]:

                    self.__height[edge.vertex] = self.__height[vertex] + 1
                    checked[edge.vertex] = True
                    to_check.put(edge.vertex)

    def __push_vertex(self, vertex: Vertex) -> None:

        if not self.__vertex_in_queue[vertex]:
            self.__vertex_queue.put((self.__height[vertex], vertex))
            self.__vertex_in_queue[vertex] = True

    def __pop_vertex(self) -> Vertex:

        vertex = self.__vertex_queue.get()[1]
        self.__vertex_in_queue[vertex] = False
        return vertex

    def __push(self, vertex: Vertex, ve: VertexEdges) -> None:

        d = min(self.__excess[vertex], ve.capacity)
        self.__excess[vertex] -= d
        self.__excess[ve.vertex] += d
        ve.capacity -= d
        ve.pair.capacity += d

    def mincut(self) -> List[Vertex]:

        if self.__mincut:
            return self.__mincut

        mincut_value: Set[Vertex] = set([self.__source])
        to_check: Queue[Vertex] = Queue()
        to_check.put(self.__source)

        while not to_check.empty():
            vertex = to_check.get()

            for edge in self.__als[vertex].edges:

                if edge.capacity > 0 and edge.vertex not in mincut_value:

                    mincut_value.add(edge.vertex)
                    to_check.put(edge.vertex)

        self.__mincut = list(mincut_value)

        return self.__mincut

    def maxflow(self) -> int:

        if self.__maxflow:
            return self.__maxflow

        while not self.__vertex_queue.empty():
            vertex = self.__pop_vertex()

            if vertex is self.__source or vertex is self.__runoff:
                continue
            while self.__excess[vertex] != 0:
                h = 2 * self.__vertex_num

                for edge in self.__als[vertex].edges:
                    if edge.capacity != 0:
                        if self.__height[vertex] == self.__height[edge.vertex] + 1:
                            self.__push(vertex, edge)
                            self.__push_vertex(edge.vertex)
                            self.__relabel()

                            if self.__excess[vertex] != 0:
                                break

                        else:
                            h = min(h, self.__height[edge.vertex])

                if self.__excess[vertex] != 0:

                    self.__height[vertex] = h + 1
                    self.__relabel()

        self.__maxflow = self.__excess[self.__runoff]

        return self.__maxflow
