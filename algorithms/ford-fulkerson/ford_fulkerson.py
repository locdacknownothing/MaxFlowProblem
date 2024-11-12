class Graph:
    def __init__(self, vertices):
        self.V = vertices  # Number of vertices
        self.graph = [[0] * vertices for _ in range(vertices)]  # Residual capacity matrix

    # Add edge with given capacity
    def add_edge(self, u, v, capacity):
        self.graph[u][v] = capacity

    # Perform DFS to find an augmenting path
    def dfs(self, s, t, parent):
        visited = [False] * self.V
        stack = [s]
        visited[s] = True

        while stack:
            u = stack.pop()
            for v in range(self.V):
                if not visited[v] and self.graph[u][v] > 0:
                    stack.append(v)
                    visited[v] = True
                    parent[v] = u
                    if v == t:
                        return True
        return False

    # Implement Ford-Fulkerson algorithm
    def ford_fulkerson(self, source, sink):
        parent = [-1] * self.V  # To store the path
        max_flow = 0  # Start with zero flow

        # Augment the flow while there is an augmenting path
        while self.dfs(source, sink, parent):
            # Find the maximum flow through the path found by DFS
            path_flow = float('Inf')
            s = sink
            while s != source:
                path_flow = min(path_flow, self.graph[parent[s]][s])
                s = parent[s]

            # Update residual capacities in the reverse direction
            v = sink
            while v != source:
                u = parent[v]
                self.graph[u][v] -= path_flow
                self.graph[v][u] += path_flow
                v = parent[v]

            max_flow += path_flow  # Add path flow to the total flow

        return max_flow