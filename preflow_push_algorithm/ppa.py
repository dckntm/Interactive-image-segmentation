import networkx as nx
from networkx.classes.graph import Graph
from networkx.classes.reportviews import NodeView

class PPA():
    """Class that provides an interface to the preflow push algorithm."""

    def __init__(self, graph: Graph) -> None:
        """Initialize PPA class.

        Args:
            graph (Graph): graph.
        """
        self.graph = graph

    def __excess(self, u: NodeView) -> float:
        """Calculate the excess flow entering the vertex u.

        Args:
            u (NodeView): u vertex.

        Returns:
            float: excess flow.
        """
        excess_flow = 0
        for (v1, v2, wt) in self.graph.edges.data('weight'):
            if v2 == u.data():
                excess_flow += wt['flow']
        return excess_flow
            

    def push(self, u: NodeView, v: NodeView) -> None:
        """Pushes the preflow from vertex u to vertex v.

        Args:
            u (NodeView): u vertex.
            v (NodeView): v vertex.
        """
        pass

    def ppa() -> float:
        """Find the maximum flow in the graph.

        Returns:
            float: maximum flow value.
        """
