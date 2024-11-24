class MPM:
    class FlowEdge:
        def __init__(self, start_node, end_node, cap, flow=0):
            self.start_node = start_node
            self.end_node = end_node
            self.cap = cap
            self.flow = flow

    def __init__(self, nums_of_node=0, source_node=0, sink_node=0):
        self.flow_inf = int(1e18)
        self.edges = []
        self.alive = []
        self.pin = []
        self.pout = []
        self.in_edges = []
        self.out_edges = []
        self.adj = []
        self.ex = []
        self.nums_of_node = nums_of_node
        self.nums_of_edge = 0
        self.source_node = source_node
        self.sink_node = sink_node
        self.level = []
        self.q = []
        self.qh = 0
        self.qt = 0
        if nums_of_node > 0:
            self.resize(nums_of_node)

    def resize(self, nums_of_node):
        self.nums_of_node = nums_of_node
        self.ex = [0] * nums_of_node
        self.q = [0] * nums_of_node
        self.pin = [0] * nums_of_node
        self.pout = [0] * nums_of_node
        self.adj = [[] for _ in range(nums_of_node)]
        self.level = [-1] * nums_of_node
        self.in_edges = [[] for _ in range(nums_of_node)]
        self.out_edges = [[] for _ in range(nums_of_node)]

    def add_edge(self, start_node, end_node, cap):
        self.edges.append(self.FlowEdge(start_node, end_node, cap))
        self.edges.append(self.FlowEdge(end_node, start_node, 0))
        self.adj[start_node].append(self.nums_of_edge)
        self.adj[end_node].append(self.nums_of_edge + 1)
        self.nums_of_edge += 2

    def bfs(self):
        self.qh = 0
        self.qt = 1
        self.q[0] = self.source_node
        self.level = [-1] * self.nums_of_node
        self.level[self.source_node] = 0

        while self.qh < self.qt:
            start_node = self.q[self.qh]
            self.qh += 1
            for id in self.adj[start_node]:
                if self.edges[id].cap - self.edges[id].flow < 1:
                    continue
                end_node = self.edges[id].end_node
                if self.level[end_node] == -1:
                    self.level[end_node] = self.level[start_node] + 1
                    self.q[self.qt] = end_node
                    self.qt += 1
        return self.level[self.sink_node] != -1

    def pot(self, start_node):
        return min(self.pin[start_node], self.pout[start_node])

    def remove_node(self, start_node):
        for i in self.in_edges[start_node]:
            end_node = self.edges[i].start_node
            self.out_edges[end_node].remove(i)
            self.pout[end_node] -= self.edges[i].cap - self.edges[i].flow
        for i in self.out_edges[start_node]:
            end_node = self.edges[i].end_node
            self.in_edges[end_node].remove(i)
            self.pin[end_node] -= self.edges[i].cap - self.edges[i].flow

    def push(self, from_node, to_node, f, forw):
        self.qh = self.qt = 0
        self.ex = [0] * self.nums_of_node
        self.ex[from_node] = f
        self.q[self.qt] = from_node
        self.qt += 1

        while self.qh < self.qt:
            start_node = self.q[self.qh]
            self.qh += 1
            if start_node == to_node:
                break
            must = self.ex[start_node]
            it = iter(self.out_edges[start_node] if forw else self.in_edges[start_node])
            while True:
                edge_index = next(it, None)
                if edge_index is None:
                    break
                end_node = self.edges[edge_index].end_node if forw else self.edges[edge_index].start_node
                pushed = min(must, self.edges[edge_index].cap - self.edges[edge_index].flow)
                if pushed == 0:
                    break
                if forw:
                    self.pout[start_node] -= pushed
                    self.pin[end_node] -= pushed
                else:
                    self.pin[start_node] -= pushed
                    self.pout[end_node] -= pushed
                if self.ex[end_node] == 0:
                    self.q[self.qt] = end_node
                    self.qt += 1
                self.ex[end_node] += pushed
                self.edges[edge_index].flow += pushed
                self.edges[edge_index ^ 1].flow -= pushed
                must -= pushed
                if self.edges[edge_index].cap - self.edges[edge_index].flow == 0:
                    next_edge = next(it, None)
                    if forw:
                        self.in_edges[end_node].remove(edge_index)
                        self.out_edges[start_node].remove(edge_index)
                    else:
                        self.out_edges[end_node].remove(edge_index)
                        self.in_edges[start_node].remove(edge_index)
                    if next_edge is None:
                        break
                    edge_index = next_edge
                if must == 0:
                    break

    def flow(self):
        ans = 0
        while True:
            self.pin = [0] * self.nums_of_node
            self.pout = [0] * self.nums_of_node
            self.level = [-1] * self.nums_of_node
            self.alive = [True] * self.nums_of_node
            if not self.bfs():
                break
            for i in range(self.nums_of_node):
                self.out_edges[i].clear()
                self.in_edges[i].clear()
            for i in range(self.nums_of_edge):
                if self.edges[i].cap - self.edges[i].flow == 0:
                    continue
                start_node, end_node = self.edges[i].start_node, self.edges[i].end_node
                if self.level[start_node] + 1 == self.level[end_node] and (self.level[end_node] < self.level[self.sink_node] or end_node == self.sink_node):
                    self.in_edges[end_node].append(i)
                    self.out_edges[start_node].append(i)
                    self.pin[end_node] += self.edges[i].cap - self.edges[i].flow
                    self.pout[start_node] += self.edges[i].cap - self.edges[i].flow
            self.pin[self.source_node] = self.pout[self.sink_node] = self.flow_inf

            while True:
                start_node = -1
                for i in range(self.nums_of_node):
                    if not self.alive[i]:
                        continue
                    if start_node == -1 or self.pot(i) < self.pot(start_node):
                        start_node = i
                if start_node == -1:
                    break
                if self.pot(start_node) == 0:
                    self.alive[start_node] = False
                    self.remove_node(start_node)
                    continue
                f = self.pot(start_node)
                ans += f
                self.push(start_node, self.source_node, f, False)
                self.push(start_node, self.sink_node, f, True)
                self.alive[start_node] = False
                self.remove_node(start_node)
        return ans
    
    def pre_process(self, start, sink, value_matrix):
        mpm = MPM(len(value_matrix[0]), start, sink)
        for i in range(0, len(value_matrix[0])):
            for j in range(0, len(value_matrix[0])):
                if value_matrix[i][j] != 0:
                    mpm.add_edge(i, j, value_matrix[i][j])
        return mpm
    
    def post_process(self, value_matrix):
        for i in range(0, len(self.edges)):
            start_node = self.edges[i].start_node
            end_node = self.edges[i].end_node
            if self.edges[i].cap > 0:
                value_matrix[start_node][end_node] = str(self.edges[i].flow) + '/' + str(self.edges[i].cap)
        return value_matrix