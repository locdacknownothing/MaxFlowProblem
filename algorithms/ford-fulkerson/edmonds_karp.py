from collections import deque

class Graph:
    def __init__(self, vertices):
        self.V = vertices  # Number of vertices
        self.graph = [[0] * vertices for _ in range(vertices)]  # Residual capacity matrix

    # Add edge with given capacity
    def add_edge(self, u, v, capacity):
        self.graph[u][v] = capacity
    
    # Perform BFS to find an augmenting path
    def bfs(self, source, sink, parent):
        visited = [False] * self.V
        queue = deque([source])
        visited[source] = True

        while queue:
            u = queue.popleft()

            for v in range(self.V):
                if not visited[v] and self.graph[u][v] > 0:  # Capacity left in the edge
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
                path_flow = min(path_flow, self.graph[parent[s]][s])
                s = parent[s]

            # Update residual capacities of the edges and reverse edges along the path
            v = sink
            while v != source:
                u = parent[v]
                self.graph[u][v] -= path_flow
                self.graph[v][u] += path_flow
                v = parent[v]

            max_flow += path_flow  # Add path flow to the total flow

        return max_flow