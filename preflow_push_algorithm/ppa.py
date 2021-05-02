import networkx as nx


def initialize_network(raw_data):
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
            # TODO : maybe add information about reverse_preflow
            preflow=edge['capacity'] if edge['u'] == raw_data['source'] else 0.0)

    node_num = len(network.nodes)
    enriched_nodes = {}

    for node in network.nodes:
        enriched_nodes[node] = {
            'vertex_label': node_num if node == network.graph['source'] else 0.0,
            'excess_flow': excess_flow_of(network, node)
        }

    nx.set_node_attributes(network, enriched_nodes)

    return network


def excess_flow_of(graph: nx.DiGraph, u):
    """Calculates excess flow for node u in graph

    Args:
        graph (nx.DiGraph): source graph 
        u ([type]): node in graph for which we calculate excess flow

    Returns:
        float: excess flow value. If it's positive than node is overflowing
    """
    return sum([preflow_of(graph, v, u) for v in graph.nodes])


def preflow_of(graph: nx.DiGraph, u, v):
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
