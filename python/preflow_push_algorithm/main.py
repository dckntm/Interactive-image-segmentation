import networkx as nx

g = {
    'source': 'A',
    'runoff': 'D',
    'edges': [
        {'u': 'A', 'v': 'C', 'capacity': 5.0},
        {'u': 'A', 'v': 'B', 'capacity': 8.0},
        {'u': 'B', 'v': 'C', 'capacity': 4.0},
        {'u': 'B', 'v': 'D', 'capacity': 3.0},
        {'u': 'C', 'v': 'D', 'capacity': 10.0},
    ]
}

# initial
#
# preflow for all edges from source node equals to capacity of edge
# for other edges preflow is 0.0
# source vertex label is V (number of nodes) and for all other nodes it is 0
#
# capacity and preflow are stored in edge
# excess flow and vertex height is stored in node


def interim_nodes_of(graph: nx.DiGraph):
    """Retuns all nodes except source and runoff nodes

    Args:
        graph (nx.DiDiGraph): Network

    Returns:
        [list]: of nodes in network except source and runoff
    """
    source = graph.graph['source']
    runoff = graph.graph['runoff']

    interim_nodes = [node for _, node in enumerate(
        graph.nodes) if node != source and node != runoff]

    return interim_nodes


def validate_network(graph: nx.DiGraph):
    """Checks if created directed graph


    Args:
        graph (nx.DiGraph): graph to be validated
    """
    # check if capacity is always more that preflow
    for edge in graph.edges:
        start = edge[0]
        end = edge[1]

        assert graph[start][end]['capacity'] >= graph[start][end]['preflow']

    # check if weakened flow saving rule works
    for u in interim_nodes_of(graph):
        assert graph.nodes[u]['excess_flow'] >= 0.0


def excess_flow_of(graph: nx.DiGraph, u):
    """Calculates excess flow for node u in graph

    Args:
        graph (nx.DiGraph): source graph
        u ([type]): node in graph for which we calculate excess flow

    Returns:
        float: excess flow value. If it's positive than node is overflowing
    """
    return sum([preflow_of(graph, v, u) for v in graph.nodes])


def find_overflowing_nodes_in(graph: nx.DiGraph):
    """Returns a list of nodes with excess flow more than 0.0

    Args:
        graph (nx.DiGraph): Network

    Returns:
        [list]: of nodes with excess flow more than 0.0
    """
    return [node for node in interim_nodes_of(graph) if excess_flow_of(graph, node) >= 0]


def initialize_network(raw_data) -> nx.DiGraph:
    """Creates networkx's DiGraph for PPA Algo

    Args:
        raw_data (dict): raw graph data
    """

    network = nx.DiGraph(source=raw_data['source'], runoff=raw_data['runoff'])

    for edge in raw_data['edges']:
        network.add_edge(
            edge['u'],
            edge['v'],
            capacity=edge['capacity'],
            preflow=edge['capacity'] if edge['u'] == raw_data['source'] else 0.0)

    node_num = len(network.nodes)
    enriched_nodes = {}

    for node in network.nodes:
        enriched_nodes[node] = {
            'vertex_label': node_num if node == network.graph['source'] else 0.0,
            'excess_flow': excess_flow_of(network, node)
        }

    print(enriched_nodes)

    nx.set_node_attributes(network, enriched_nodes)

    return network


def preflow_of(graph: nx.DiGraph, u, v) -> float:
    """Recalculates preflow for edge (as we do not store 2 way edges)

    Args:
        graph (nx.DiGraph): network
        u (str): start edge node
        v (str): end edge node

    Returns:
        [float]: preflow value for some edge (with direction info)
    """
    # TODO : theroetically might be optimized
    if graph.has_edge(u, v):
        return graph[u][v]['preflow']
    elif graph.has_edge(v, u):
        return -1 * graph[v][u]['preflow']
    else:
        return 0.0


def push(graph: nx.DiGraph, u, v) -> None:
    d = min(graph.nodes[u]['excess_flow'], graph[u]
            [v]['capacity'] - graph[u][v]['preflow'])

    graph[u][v]['preflow'] += d
    graph.nodes[u]['excess_flow'] -= d
    graph.nodes[v]['excess_flow'] += d


def relabel(graph: nx.DiGraph, u) -> None:
    min_vertex_label = min(graph.nodes[v]['vertex_label']
                           for v in graph.neighbors(u)
                           if residual_capacity(graph, u, v) > 0.0)

    graph.nodes[u]['vertex_label'] = min_vertex_label + 1


def residual_network_edges(graph: nx.DiGraph):
    return [edge for edge in graph.edges
            if residual_capacity(graph, edge[0], edge[1]) > 0.0]


def next_residual_network_edge(graph: nx.DiGraph):
    for edge in graph.edges:
        if residual_capacity(graph, edge[0], edge[1]) > 0.0:
            return edge

    return None


def residual_capacity(graph: nx.DiGraph, u, v):
    return graph[u][v]['capacity'] - graph[u][v]['preflow']


def try_find_next_push(graph: nx.DiGraph, u):
    if not graph.nodes[u]['excess_flow'] > 0.0:
        return None

    for v in graph.successors(u):
        if residual_capacity(graph, u, v) > 0 and graph.nodes[u]['vertex_label'] == graph.nodes[v]['vertex_label'] + 1:
            return v


def try_find_next_relabel(graph: nx.DiGraph, u):
    if not graph.nodes[u]['excess_flow'] > 0.0:
        return None

    for v in [edge[1] for edge in residual_network_edges(graph) if edge[0] == u]:
        if graph.nodes[u]['vertex_label'] <= graph.nodes[v]['vertex_label']:
            return v


if __name__ == '__main__':
    ntw = initialize_network(g)

    try:
        validate_network(ntw)
    except AssertionError:
        print(f'Validation error occurred')
        raise

    print(ntw.edges)
    print(residual_network_edges(ntw))
    print(next_residual_network_edge(ntw))

    for u in ntw.nodes:
        v = try_find_next_push(ntw, u)

        if v != None:
            push(ntw, u, v)

            print('Push made!!!')

        v = try_find_next_relabel(ntw, u)

        if v != None:
            relabel(ntw, u)

            print('Relabel made!!!')

    for node in ntw.nodes:
        print(ntw.nodes[node])
