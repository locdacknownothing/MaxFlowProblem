from collections import deque

class Graph:
    def __init__(self, vertices):
        self.V = vertices  # Number of vertices
        self.graph = [[0] * vertices for _ in range(vertices)]  # Residual capacity matrix
        self.max_capacity = 0  # Maximum capacity in the graph

    # Add edge with given capacity
    def add_edge(self, u, v, capacity):
        self.graph[u][v] = capacity
        self.max_capacity = max(self.max_capacity, capacity)
    
    # Perform BFS to find an augmenting path with residual capacity >= scaling factor
    def bfs(self, source, sink, parent, scaling_factor):
        visited = [False] * self.V
        queue = deque([source])
        visited[source] = True

        while queue:
            u = queue.popleft()

            for v in range(self.V):
                if not visited[v] and self.graph[u][v] >= scaling_factor:  # Residual capacity >= scaling factor
                    queue.append(v)
                    visited[v] = True
                    parent[v] = u
                    if v == sink:
                        return True
        return False

    # Implement Capacity Scaling algorithm
    def capacity_scaling(self, source, sink):
        parent = [-1] * self.V  # To store the path
        max_flow = 0  # Initialize max flow

        # Start with the largest scaling factor
        scaling_factor = 1
        while scaling_factor <= self.max_capacity:
            scaling_factor *= 2

        # Iterate while scaling_factor is reduced to 1
        while scaling_factor > 0:
            # Perform BFS to find augmenting paths with residual capacity >= scaling_factor
            while self.bfs(source, sink, parent, scaling_factor):
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

            # Reduce scaling factor
            scaling_factor //= 2

        return max_flow
