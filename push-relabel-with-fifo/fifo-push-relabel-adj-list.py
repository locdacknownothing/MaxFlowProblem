import matplotlib.pyplot as plt
import networkx as nx


# Represents a vertex (or edge endpoint) in the graph with an index and edge capacity
class Vertex:
    def __init__(self, i, capacity):
        # i: Index of the vertex this edge points to
        # capacity: Capacity of the edge
        self.i = i
        self.capacity = capacity


# Represents a directed graph using an adjacency list
class DirectedGraph:
    def __init__(self):
        # Adjacency list to store edges for each vertex
        self.adjacencyList = {}

    # Adds a directed edge from vertex u to vertex v with the given capacity
    def addEdge(self, u, v, capacity):
        # Ensure the adjacency list has entries for both u and v
        if u not in self.adjacencyList:
            self.adjacencyList[u] = []
        if v not in self.adjacencyList:
            self.adjacencyList[v] = []

        # Add the edge to the adjacency list
        self.adjacencyList[u].append(Vertex(v, capacity))

    # Checks if there is an edge from vertex u to vertex v
    def hasEdge(self, u, v):
        if u not in self.adjacencyList:
            return False

        # Iterate through the adjacency list of u to find v
        for vertex in self.adjacencyList[u]:
            if vertex.i == v:
                return True
        return False

    # Returns the edge from vertex u to vertex v if it exists, otherwise None
    def getEdge(self, u, v):
        if u not in self.adjacencyList:
            return None

        for vertex in self.adjacencyList[u]:
            if vertex.i == v:
                return vertex
        return None

    # Prints the entire graph (adjacency list)
    def printGraph(self):
        print("Graph adjacency list:")
        for u in self.adjacencyList:
            print(f"Vertex {u}: ", end="")
            for v in self.adjacencyList[u]:
                print(f"-> {v.i} (capacity: {v.capacity})", end=" ")
            print()  # Newline for the next vertex


# Represents the max flow calculation using the Push-Relabel algorithm
class MaxFlow:
    def __init__(self, graph, source, sink):
        self.graph = graph
        self.source = source
        self.sink = sink

    # Initializes the residual graph with the same vertices as the original graph
    def initResidualGraph(self):
        self.residualGraph = DirectedGraph()

        # Iterate over each vertex and its adjacency list
        for u in self.graph.adjacencyList:
            for v in self.graph.adjacencyList[u]:
                # If the edge already exists in the residual graph, increase its capacity
                if self.residualGraph.hasEdge(u, v.i):
                    self.residualGraph.getEdge(u, v.i).capacity += v.capacity
                else:
                    # Add the forward edge with the original capacity
                    self.residualGraph.addEdge(u, v.i, v.capacity)

                # Ensure a reverse edge exists with zero capacity
                if not self.residualGraph.hasEdge(v.i, u):
                    self.residualGraph.addEdge(v.i, u, 0)

    # Implements the FIFO Push-Relabel algorithm to compute the maximum flow
    def FIFOPushRelabel(self):
        self.initResidualGraph()

        # Initialize pre-flow values
        queue = []
        excess = {u: 0 for u in self.graph.adjacencyList}  # Excess flow for each vertex
        height = {u: 0 for u in self.graph.adjacencyList}  # Height of each vertex
        inQueue = {
            u: False for u in self.graph.adjacencyList
        }  # To track if a vertex is in the queue

        # Set the height of the source vertex to the number of vertices
        height[self.source] = len(self.graph.adjacencyList)

        # Initialize pre-flow from the source
        for v in self.graph.adjacencyList[self.source]:
            # Set forward edge capacity to 0 and reverse edge capacity to original capacity
            self.residualGraph.getEdge(self.source, v.i).capacity = 0
            self.residualGraph.getEdge(v.i, self.source).capacity = v.capacity

            # Update the excess flow for the adjacent vertex
            excess[v.i] = v.capacity

            # Add the adjacent vertex to the queue if it is not the sink
            if v.i != self.sink:
                queue.append(v.i)
                inQueue[v.i] = True

        # While there are vertices in the queue to process
        while queue:
            u = queue.pop(0)  # Dequeue a vertex
            inQueue[u] = False
            self.relabel(u, height)  # Relabel the vertex to update its height
            self.push(u, excess, height, queue, inQueue)  # Push flow from the vertex

        # Return the maximum flow, which is the excess flow at the sink
        return excess[self.sink]

    # Relabel operation: Increases the height of vertex u to enable pushing flow
    def relabel(self, u, height):
        minHeight = float("inf")

        # Find the minimum height of adjacent vertices that have positive capacity
        for v in self.residualGraph.adjacencyList[u]:
            if v.capacity > 0:
                minHeight = min(minHeight, height[v.i])

        # Set the new height of u to 1 more than the minimum height of its neighbors
        height[u] = minHeight + 1

    # Push operation: Pushes excess flow from vertex u to its neighbors
    def push(self, u, excess, height, queue, in_queue):
        # Iterate over the neighbors of u in the residual graph
        for v in self.residualGraph.adjacencyList[u]:
            # Stop if there is no excess flow at u
            if excess[u] == 0:
                break

            # Push flow if possible
            if v.capacity > 0 and height[v.i] < height[u]:
                # Determine the amount of flow to push
                flow = min(excess[u], v.capacity)

                # Update the capacities in the residual graph
                v.capacity -= flow
                self.residualGraph.getEdge(v.i, u).capacity += flow

                # Update excess flow for u and v
                excess[u] -= flow
                excess[v.i] += flow

                # Add v to the queue if it now has excess flow and is not in the queue
                if not in_queue[v.i] and v.i != self.source and v.i != self.sink:
                    queue.append(v.i)
                    in_queue[v.i] = True

        # If u still has excess flow, re-add it to the queue
        if excess[u] != 0:
            queue.append(u)
            in_queue[u] = True


# Example usage
source = 0
sink = 5

# Create the graph
dg = DirectedGraph()

# Add edges with capacities
dg.addEdge(0, 1, 16)
dg.addEdge(0, 2, 13)
dg.addEdge(1, 2, 10)
dg.addEdge(2, 1, 4)
dg.addEdge(1, 3, 12)
dg.addEdge(3, 2, 9)
dg.addEdge(2, 4, 14)
dg.addEdge(4, 5, 4)
dg.addEdge(4, 3, 7)
dg.addEdge(3, 5, 20)

# Print the graph's adjacency list
dg.printGraph()

# Calculate the maximum flow using FIFO Push-Relabel algorithm
maxFlow = MaxFlow(dg, source, sink)
print("Max flow:", maxFlow.FIFOPushRelabel())