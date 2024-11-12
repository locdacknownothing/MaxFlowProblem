from collections import deque

class Graph:
    def __init__(self, vertices, graph):
        self.graph = graph # Input graph
        self.V = vertices  # Number of vertices
        self.residual_graph = [[0] * vertices for _ in range(vertices)]  # Residual capacity matrix
        self.create_residual_graph(graph)

    # Add edge with given capacity
    def add_edge(self, u, v, capacity):
        self.residual_graph[u][v] = capacity
        
    def create_residual_graph(self, graph):
        for i in range(len(graph)):
            for j in range(len(graph[i])):
                self.add_edge(i, j, graph[i][j])
                
    def create_result_graph(self):
        result = []
        for u in range(len(self.graph)):
            row = []
            for v in range(len(self.graph)):
                if self.graph[u][v] > 0:  # Only include edges with initial capacity
                    row.append(f"{self.residual_graph[v][u]}/{self.graph[u][v]}")
                else:
                    row.append(0)
            result.append(row)
        return result
    
    # Perform BFS to find an augmenting path
    def bfs(self, source, sink, parent):
        visited = [False] * self.V
        queue = deque([source])
        visited[source] = True

        while queue:
            u = queue.popleft()

            for v in range(self.V):
                if not visited[v] and self.residual_graph[u][v] > 0:  # Capacity left in the edge
                    queue.append(v)
                    visited[v] = True
                    parent[v] = u
                    if v == sink:
                        return True
        return False

    # Implement Edmonds-Karp algorithm (BFS for finding augmenting paths)
    def edmonds_karp(self, source, sink):
        parent = [-1] * self.V  # To store the path
        max_flow = 0  # Initialize max flow

        # Augment the flow while there is an augmenting path
        while self.bfs(source, sink, parent):
            # Find the maximum flow through the path found by BFS
            path_flow = float('Inf')
            s = sink
            while s != source:
                path_flow = min(path_flow, self.residual_graph[parent[s]][s])
                s = parent[s]

            # Update residual capacities of the edges and reverse edges along the path
            v = sink
            while v != source:
                u = parent[v]
                self.residual_graph[u][v] -= path_flow
                self.residual_graph[v][u] += path_flow
                v = parent[v]

            max_flow += path_flow  # Add path flow to the total flow

        return max_flow