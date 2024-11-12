class FifoPushRelabel:
    def __init__(self, graph, source, sink):
        self.graph = graph
        self.residual_graph = [row[:] for row in graph]  # Create a copy for the residual graph
        self.source = source
        self.sink = sink
        self.n = len(graph)

    def print_graph(self):
        print("Residual graph:")
        for u in range(self.n):
            for v in range(self.n):
                print(f"{self.residual_graph[u][v]:3}", end=" ")
            print()  # Newline for the next row

    def result_flow_graph(self):
        result = []
        for u in range(self.n):
            row = []
            for v in range(self.n):
                if self.graph[u][v] > 0:  # Only include edges with initial capacity
                    row.append(f"{self.residual_graph[v][u]}/{self.graph[u][v]}")
                else:
                    row.append(0)
            result.append(row)
        return result

    # Implements the FIFO Push-Relabel algorithm on the residual graph
    def process(self):
        # Initialize pre-flow values
        queue = []
        excess = {u: 0 for u in range(self.n)}
        height = {u: 0 for u in range(self.n)}
        inQueue = {u: False for u in range(self.n)}

        # Set the height of the source vertex to the number of vertices
        height[self.source] = self.n

        # Initialize pre-flow from the source
        for v in range(len(self.residual_graph[self.source])):
            capacity = self.residual_graph[self.source][v]
            if capacity > 0:
                # Set forward edge capacity to 0 and reverse edge capacity to original capacity
                self.residual_graph[self.source][v] = 0
                self.residual_graph[v][self.source] = capacity

                # Update the excess flow for the adjacent vertex
                excess[v] = capacity

                # Add the adjacent vertex to the queue if it is not the sink
                if v != self.sink:
                    queue.append(v)
                    inQueue[v] = True

        # Print the graph after initialization
        self.print_graph()

        # Process each vertex in the queue
        while queue:
            u = queue.pop(0)
            inQueue[u] = False
            self.relabel(u, height)  # Relabel the vertex to update its height
            self.push(u, excess, height, queue, inQueue)  # Push flow from the vertex

        # Return the maximum flow, which is the excess flow at the sink
        return excess[self.sink]

    # Relabel operation: Increases the height of vertex u
    def relabel(self, u, height):
        minHeight = float("inf")
        for v in range(len(self.residual_graph[u])):
            if self.residual_graph[u][v] > 0:
                minHeight = min(minHeight, height[v])
        height[u] = minHeight + 1

    # Push operation: Pushes excess flow from vertex u to its neighbors
    def push(self, u, excess, height, queue, inQueue):
        for v in range(len(self.residual_graph[u])):
            if excess[u] == 0:
                break
            if self.residual_graph[u][v] > 0 and height[v] < height[u]:
                flow = min(excess[u], self.residual_graph[u][v])
                self.residual_graph[u][v] -= flow
                self.residual_graph[v][u] += flow
                excess[u] -= flow
                excess[v] += flow
                if not inQueue[v] and v != self.source and v != self.sink:
                    queue.append(v)
                    inQueue[v] = True
        if excess[u] != 0:
            queue.append(u)
            inQueue[u] = True


# Example usage
source = 0
sink = 5
# Original adjacency matrix
dg = [
    [0, 16, 13, 0, 0, 0], 
    [0, 0, 10, 12, 0, 0], 
    [0, 4, 0, 0, 14, 0], 
    [0, 0, 9, 0, 0, 20], 
    [0, 0, 0, 7, 0, 4], 
    [0, 0, 0, 0, 0, 0]
]

# Create MaxFlow object with separate residual graph
maxFlow = FifoPushRelabel(dg, source, sink)
print("Max flow:", maxFlow.process())
print("Result graph with flow/capacity:\n", maxFlow.result_flow_graph())