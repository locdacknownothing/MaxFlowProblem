from ford_fulkerson import Graph
# from edmonds_karp import Graph
# from capacity_scaling import Graph

def create_graph(graph):
    g = Graph(len(graph))
    for i in range(len(graph)):
        for j in range(len(graph[i])):
            g.add_edge(i, j, graph[i][j])
    return g

graph = [
    [0, 16, 13, 0, 0, 0],
    [0, 0, 10, 12, 0, 0],
    [0, 4, 0, 0, 14, 0],
    [0, 0, 9, 0, 0, 20],
    [0, 0, 0, 7, 0, 4],
    [0, 0, 0, 0, 0, 0]
]

g = create_graph(graph)

source = 0  # Source node
sink = 5    # Sink node

max_flow = g.ford_fulkerson(source, sink)

print(g.graph)

print("Maximum Flow:", max_flow)