from queue import PriorityQueue, Queue
from typing import List, NewType, Optional, Set, Tuple, Union
import numpy as np


def maxflow(
    arcs: np.ndarray,
    v: int,
    flow: Optional[np.ndarray] = None,
    find_mincut: bool = True
) -> Union[Tuple[int, np.ndarray], Tuple[int, np.ndarray, List[int]]]:
    """
    Computes the maximum flow of the graph.

    Parameters
    ----------
    arcs: np.ndarray
        numpy array [v,3] - [[node1, node2, capacity]]
    v: int
        number of nodes (vertices)
    flow: Optional[np.ndarray]
        correct sub-optimal (optional) flow [v,3] - [[node1, node2, flow]]
    find_mincut: bool = False
        bool value that determines whether mincut should be returned

    Returns the value of the maximum flow, the flow as the edge list graph
    and (optionally) the minimum cut.
    """

    Node = NewType('Node', int)

    class ArcCapacity:
        """
        Container for storing the node's arc.

        Stores the arc's head node, its capacity and reference to paired arc.
        """

        def __init__(self, node: Node, capacity: int) -> None:
            self.node: Node = node
            self.capacity: int = capacity
            self.paired_arc: Optional[ArcCapacity] = None

        def __str__(self) -> str:
            return f"({self.node}, {self.capacity})"

    class NodeArcs:
        """Container for storing the graph adjacency list."""

        def __init__(self) -> None:
            self.arcs: List[ArcCapacity] = []

        # get: arc[node] -> capacity
        def __getitem__(self, node: Node) -> Optional[int]:
            for arc in self.arcs:
                if arc.node == node:
                    return arc.capacity
            return None

        # set: arc[node] = capacity
        def __setitem__(self, node: Node, capacity: int) -> None:
            for arc in self.arcs:
                if arc.node == node:
                    arc.capacity = capacity
                    return
            raise ValueError("Attempt to set capacity of non-existent arc")

        def get_arc(self, node: Node) -> Optional[ArcCapacity]:
            for arc in self.arcs:
                if arc.node == node:
                    return arc
            return None

        def append(self, node: Node, capacity: int) -> None:
            self.arcs.append(ArcCapacity(node, capacity))

        def __str__(self) -> str:
            if len(self.arcs) == 0:
                return "[]"

            string: str = "["
            for e in self.arcs:
                string += str(e) + ", "
            return string[:-2] + "]"

    def translate_from_arcs() -> None:
        """Transforms the edge list graph representation to the adjacency list."""

        for arc in arcs:
            sought_arc: Optional[ArcCapacity] = c[arc[0]].get_arc(arc[1])

            if sought_arc is None:
                c[arc[0]].append(arc[1], arc[2])
                sought_arc = c[arc[0]].arcs[-1]

                c[arc[1]].append(arc[0], 0)
                paired_arc = c[arc[1]].arcs[-1]

                sought_arc.paired_arc = paired_arc
                paired_arc.paired_arc = sought_arc
            else:
                sought_arc.capacity = arc[2]

    def residual_from_flow() -> None:
        """Computes the resideal graph from the given flow and returns the flow value."""

        for arc in flow:
            sought_arc: ArcCapacity = c[arc[0]].get_arc(arc[1])
            sought_arc.capacity -= arc[2]
            sought_arc.paired_arc.capacity += arc[2]

            if arc[1] == sink:
                x[sink] += arc[2]

    _M: int = arcs.shape[0] + v
    _gb_counter: int = _M - 1

    def global_relabeling() -> None:
        """Invokes global relabeling each M calls."""

        def height_as_distance(from_node: Node):
            nodes_to_check: 'Queue[Node]' = Queue()
            nodes_to_check.put(from_node)

            while not nodes_to_check.empty():
                node = nodes_to_check.get()

                for arc in c[node].arcs:
                    if arc.paired_arc.capacity > 0 and not nodes_checked[arc.node]:
                        h[arc.node] = h[node] + 1
                        nodes_checked[arc.node] = True
                        nodes_to_check.put(arc.node)

        nonlocal _gb_counter

        _gb_counter += 1
        if _gb_counter == _M:
            _gb_counter = 0

            nodes_checked: List[bool] = [True] + \
                [False for _ in range(v - 2)] + [True]
            height_as_distance(sink)
            height_as_distance(source)
            # print(h)

    def mincut() -> List[Node]:
        """Returns the minimum cut of the graph."""

        mincut_nodes: Set[Node] = set([source])
        nodes_to_check: 'Queue[Node]' = Queue()
        nodes_to_check.put(source)

        while not nodes_to_check.empty():
            node = nodes_to_check.get()

            for arc in c[node].arcs:
                if arc.capacity > 0 and arc.node not in mincut_nodes:
                    mincut_nodes.add(arc.node)
                    nodes_to_check.put(arc.node)

        return list(mincut_nodes)

    def push(node: Node, arc: ArcCapacity) -> None:
        """The maximum flow push operation."""

        delta = min(x[node], arc.capacity)
        x[node] -= delta
        x[arc.node] += delta
        arc.capacity -= delta
        arc.paired_arc.capacity += delta

        # print(f"push: {node} --{delta}-> {arc.node}")

    source: Node = 0
    sink: Node = v - 1

    # high level optimization
    node_queue: 'PriorityQueue[Node]' = PriorityQueue()
    q: List[bool] = [False for _ in range(v)]  # is node in queue

    def push_node_to_queue(node: Node) -> None:
        if not q[node]:
            node_queue.put((h[node], node))
            q[node] = True

    def pop_node_from_queue() -> Node:
        node = node_queue.get()[1]
        q[node] = False
        return node

    # height function
    h: List[int] = [v] + [2 * v for _ in range(v - 2)] + [0]

    # excess function
    x: List[int] = [0 for _ in range(v)]

    # residual capacity function
    c: List[NodeArcs] = [NodeArcs() for _ in range(v)]
    translate_from_arcs()

    if flow is not None:
        residual_from_flow()
        # print("\nFLOW:", x[sink])

    # initialization
    for arc in c[source].arcs:
        x[arc.node] = arc.capacity
        c[arc.node][source] = arc.capacity
        arc.capacity = 0

        # fisrt nodes to queue
        node_queue.put((0, arc.node))
        q[arc.node] = True

    global_relabeling()

    # main
    while not node_queue.empty():  # while there are some active nodes
        node = pop_node_from_queue()
        if node in (source, sink):
            continue

        # print(f"\nACTIVE: {node}")

        while x[node] != 0:
            height = 2 * v  # min height for relabeling
            # print("\n", x[node], c[node])

            for arc in c[node].arcs:
                if arc.capacity != 0:  # if the arc is admissible
                    # pushing
                    if h[node] == h[arc.node] + 1:
                        push(node, arc)
                        push_node_to_queue(arc.node)
                        global_relabeling()
                        if x[node] == 0:
                            break
                    # finding relabeling height
                    else:
                        # print(f"height update: n {arc.node} h {h[arc.node]}")
                        height = min(height, h[arc.node])

            # relabeling
            if x[node] != 0:
                # print(f"relabel (ex: {x[node]}): {h[node]} -> {height + 1}")#
                h[node] = height + 1
                global_relabeling()

    f = np.copy(arcs)
    for arc in f:
        arc[2] = arc[2] - c[arc[0]][arc[1]]
        if arc[2] < 0:
            arc[2] = 0

    # print("\nThe residual graph: node -> arc(node, capacity)")
    # for i in range(v):
    #     print(i, "->", c[i])
    # print("\nMAXFLOW:", x[sink])
    # print(f, end="\n\n")
    # print("Mincut:", mincut())

    if find_mincut:
        return x[sink], f, mincut()
    else:
        return x[sink], f


# if __name__ == "__main__":
    # val, flow, mincut = maxflow(np.array([
    #     [0, 1, 1], [0, 2, 12], [1, 2, 2], [2, 1, 0],
    #     [1, 3, 10], [3, 2, 5], [2, 4, 14], [4, 3, 7],
    #     [4, 5, 2], [3, 5, 15],
    #     ]), 6)

    # maxflow(np.array([
    #     [0, 1, 16], [0, 2, 13], [1, 2, 10], [2, 1, 4],
    #     [1, 3, 12], [3, 2, 9], [2, 4, 14], [4, 3, 7],
    #     [4, 5, 4], [3, 5, 20],
    #     ]), 6, flow)

    # maxflow(np.array([
    #     [0, 1, 3], [1, 2, 4], [2, 5, 2], [0, 3, 5],
    #     [3, 5, 7], [0, 4, 2], [4, 3, 3], [4, 5, 1]
    #     ]), 6)

    # maxflow(np.array([
    #     [0, 1, 3], [0, 2, 3], [2, 1, 10], [1, 4, 2],
    #     [2, 4, 1], [4, 6, 2], [4, 3, 1], [0, 3, 4],
    #     [3, 5, 5], [4, 5, 1], [5, 6, 5]
    #     ]), 7)

    # maxflow(np.array([
    #     [0, 1, 10], [0, 2, 8], [2, 1, 4], [1, 2, 5],
    #     [2, 4, 10], [1, 3, 5], [3, 2, 7], [4, 3, 10],
    #     [3, 4, 6], [3, 5, 3], [4, 5, 14]
    #     ]), 6)
