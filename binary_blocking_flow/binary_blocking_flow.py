from collections import deque

class Graph:
    def __init__(self, vertices):
        self.V = vertices 
        self.graph = [[0 for _ in range(vertices)] for _ in range(vertices)] 


    def add_edge(self, u, v, capacity):
        self.graph[u][v] = capacity

    def bfs(self, source, sink, parent):
        visited = [False] * self.V
        queue = deque([source])
        visited[source] = True

        while queue:
            u = queue.popleft()

            for v in range(self.V):
                if not visited[v] and self.graph[u][v] > 0: 
                    parent[v] = u
                    if v == sink:
                        return True
                    queue.append(v)
                    visited[v] = True

        return False

    def binary_blocking_flow(self, source, sink):
        total_flow = 0
        parent = [-1] * self.V 

        while self.bfs(source, sink, parent):
            path_flow = float('Inf')
            s = sink
            while s != source:
                path_flow = min(path_flow, self.graph[parent[s]][s])
                s = parent[s]

            total_flow += path_flow
            v = sink
            while v != source:
                u = parent[v]
                self.graph[u][v] -= path_flow
                self.graph[v][u] += path_flow
                v = parent[v]

        return total_flow


# g = Graph(6)

# g.add_edge(0, 1, 16)
# g.add_edge(0, 2, 13)
# g.add_edge(1, 2, 10)
# g.add_edge(1, 3, 12)
# g.add_edge(2, 1, 4)
# g.add_edge(2, 4, 14)
# g.add_edge(3, 2, 9)
# g.add_edge(3, 5, 20)
# g.add_edge(4, 3, 7)
# g.add_edge(4, 5, 4)


# source = 0
# sink = 5
# max_flow = g.binary_blocking_flow(source, sink)

# print("The maximum possible flow is", max_flow)
