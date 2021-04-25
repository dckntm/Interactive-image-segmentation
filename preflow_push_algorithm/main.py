import networkx as nx

if __name__ == '__main__':
    #graph = nx.DiGraph()
    f = open("preflow_push_algorithm/input.txt", "r")
    v_num, e_num = f.readline().split()
    v_num = int(v_num)
    e_num = int(e_num)
    g = list()
    for i in range(e_num):
        v1, v2, throughput = f.readline().split()
        #graph.add_weighted_edges_from([(int(v1), int(v2), float(throughput))])
        g.append((v1, v2, {"throughput": throughput, "flow": throughput}))
    graph = nx.DiGraph(g)

    for (u, v, wt) in graph.edges.data():
        print(u, v, wt)
