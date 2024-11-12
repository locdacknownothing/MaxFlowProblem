# from ford_fulkerson import Graph
#from edmonds_karp import Graph
from capacity_scaling import Graph

input = [
    [0, 16, 13, 0, 0, 0],
    [0, 0, 10, 12, 0, 0],
    [0, 4, 0, 0, 14, 0],
    [0, 0, 9, 0, 0, 20],
    [0, 0, 0, 7, 0, 4],
    [0, 0, 0, 0, 0, 0]
]

g = Graph(len(input), input)

source = 0  # Source node
sink = 5    # Sink node

print("Maximum Flow:", g.capacity_scaling(source, sink))
print("Result: ", g.create_result_graph())