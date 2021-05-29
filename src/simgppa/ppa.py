from queue import Queue, PriorityQueue
from typing import Optional, Union, List, Tuple, Dict, Set, NewType
import numpy as np
from collections import namedtuple

Vertex = NewType('Vertex', int)


class Edge:

    def __init__(self, start, end, capacity) -> None:

        self.start = start
        self.end = end
        self.capacity = capacity


class EdgeCapacity:

    def __init__(self, capacity: Union[int, float]) -> None:
        self.capacity = capacity
        self.pair = None


class VertexEdges:

    def __init__(self) -> None:
        self.edges: Dict[int, EdgeCapacity] = dict()

    def __getitem__(self, vertex: Vertex) -> Optional[int]:
        arc = self.edges.get(vertex)

        if arc is not None:
            return arc.capacity

        return None

    def __setitem__(self, vertex: Vertex, capacity: int) -> None:
        arc = self.edges.get(vertex)
        if arc is not None:
            arc.capacity = capacity
            return

        raise ValueError("Atempt to set capacity of non-existent arc")

    def get_edge_capacity(self, vertex: Vertex) -> Optional[EdgeCapacity]:
        return self.edges.get(vertex)

    def set_edge_capacity(self, vertex: Vertex, capacity: int) -> None:
        self.edges[vertex] = EdgeCapacity(capacity)


class PPA:
    def __init__(self,
                 vertex_num: int,
                 edges: List[Edge],
                 flow: Optional[List[Edge]] = None) -> None:
        self.edges = edges
        self.vertex_num = vertex_num

        self.__max_flow = None
        self.__min_cut = None

        self._M: int = len(edges) + vertex_num
        self.relabeling_counter: int = self._M - 1
        self.capacity: List[VertexEdges] = [VertexEdges()
                                            for _ in range(self.vertex_num)]

        self.v_queue: PriorityQueue[Vertex] = PriorityQueue()
        self.in_queue: List[bool] = [False for _ in range(
            self.vertex_num)]

        self.height: List[int] = \
            [self.vertex_num] + \
            [2 * self.vertex_num for _ in range(self.vertex_num - 2)] + \
            [0]

        self.excess: List[int] = [0 for _ in range(self.vertex_num)]

        self.runoff = self.vertex_num - 1
        self.source = 0
        self.__flow = None
        self.__read_edges()

        if flow:
            self.__apply_flow()

        for vertex, ec in self.capacity[self.source].edges.items():
            self.excess[vertex] = ec.capacity
            self.capacity[vertex][self.source] = ec.capacity
            ec.capacity = 0.0

            # fisrt nodes to queue
            self.v_queue.put((0, vertex))
            self.in_queue[vertex] = True

        self.__relabel()

    def __read_edges(self) -> None:

        for edge in self.edges:
            fedge: Optional[EdgeCapacity] = self.capacity[edge.start].get_edge_capacity(
                edge.end)

            if fedge is None:
                self.capacity[edge.start].set_edge_capacity(
                    edge.end, edge.capacity)
                fedge = self.capacity[edge.start].get_edge_capacity(edge.end)

                self.capacity[edge.end].set_edge_capacity(edge.start, 0)
                paired_arc = self.capacity[edge.end].get_edge_capacity(
                    edge.start)

                fedge.pair = paired_arc
                paired_arc.pair = fedge
            else:
                fedge.capacity = edge.capacity

    def __apply_flow(self, flow) -> None:

        for edge in flow:
            fedge: EdgeCapacity = self.capacity[edge.start].get_edge_capacity(
                edge.end)
            fedge.capacity -= edge.capacity
            fedge.pair.capacity += edge.capacity

            if edge.end == self.runoff:
                self.excess[self.runoff] += edge.capacity

    def __push(self, vertex: Vertex, edge_vertex: Vertex, ec: EdgeCapacity) -> None:

        delta = min(self.excess[vertex], ec.capacity)
        self.excess[vertex] -= delta
        self.excess[edge_vertex] += delta
        ec.capacity -= delta
        ec.pair.capacity += delta

    def __relabel(self):
        def height_as_distance(vertex: Vertex):
            to_check: 'Queue[Vertex]' = Queue()
            to_check.put(vertex)

            while not to_check.empty():
                edge = to_check.get()

                for v, ce in self.capacity[edge].edges.items():
                    if ce.pair.capacity > 0 and not nodes_checked[v]:
                        self.height[v] = self.height[edge] + 1
                        nodes_checked[v] = True
                        to_check.put(v)

        self.relabeling_counter += 1
        if self.relabeling_counter == self._M:
            self.relabeling_counter = 0

            nodes_checked: List[bool] = \
                [True] + \
                [False for _ in range(self.vertex_num - 2)] + \
                [True]
            height_as_distance(self.runoff)
            height_as_distance(self.source)

    def __push_vertex(self, vertex: Vertex) -> None:
        if not self.in_queue[vertex]:
            self.v_queue.put((self.height[vertex], vertex))
            self.in_queue[vertex] = True

    def __pop_vertex(self) -> Vertex:
        node = self.v_queue.get()[1]
        self.in_queue[node] = False
        return node

    def min_cut(self) -> List[Vertex]:

        if self.__min_cut:
            return self.min_cut

        if not self.__max_flow:
            self.max_flow()

        mincut_nodes: Set[Vertex] = set([self.source])
        to_check: 'Queue[Vertex]' = Queue()
        to_check.put(self.source)

        while not to_check.empty():
            node = to_check.get()

            for vertex, ec in self.capacity[node].edges.items():
                if ec.capacity > 0 and vertex not in mincut_nodes:
                    mincut_nodes.add(vertex)
                    to_check.put(vertex)

        return list(mincut_nodes)

    def flow(self):

        if self.__flow:
            return self.__flow

        if not self.__max_flow:
            self.__max_flow()

        f = [[0, 0, 0] for i in range(len(self.edges))]
        for i in range(len(f)):
            f[i][0] = self.edges[i].start
            f[i][1] = self.edges[i].end
            f[i][2] = self.edges[i].capacity - \
                self.capacity[self.edges[i].start][self.edges[i].end]
            if f[i][2] < 0:
                f[i][2] = 0

        self.__flow = f

        return f

    def max_flow(self):

        if self.__max_flow:
            return self.__max_flow

        while not self.v_queue.empty():  # while there are some active nodes
            vertex = self.__pop_vertex()
            if vertex in (self.source, self.runoff):
                continue

            while self.excess[vertex] != 0.0:
                height = 2 * self.vertex_num

                for v, ec in self.capacity[vertex].edges.items():
                    if ec.capacity != 0:  # if the arc is admissible
                        # pushing
                        if self.height[vertex] == self.height[v] + 1:
                            self.__push(vertex, v, ec)
                            self.__push_vertex(v)
                            self.__relabel()
                            if self.excess[vertex] == 0:
                                break
                        else:
                            height = min(height, self.height[v])

                if self.excess[vertex] != 0:
                    self.height[vertex] = height + 1
                    self.__relabel()

        self.__max_flow = self.excess[self.runoff]

        return self.__max_flow
