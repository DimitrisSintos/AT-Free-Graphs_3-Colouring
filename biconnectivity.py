class TarjansBiconnectivity:
    """
    Tarjan's Biconnected Components Algorithm
    """
    def __init__(self,graph):
        self.graph = graph
        self.time = 0
        self.number = {}
        self.lowpt = {}
        self.edge_stack = []
        self.biconnected_components = [] 

    def biconnect(self,v,parent):
        self.time += 1
        self.number[v] = self.lowpt[v] = self.time

        for w in self.graph.adjacency_list[v]:
            if w not in self.number:
                self.edge_stack.append((v,w))
                self.biconnect(w,v)
                self.lowpt[v] = min(self.lowpt[v],self.lowpt[w])

                if self.lowpt[w] >= self.number[v]:
                    component = []
                    while True:
                        e = self.edge_stack.pop()
                        component.append(e)
                        if e[0] == v and e[1] == w:
                            break
                    self.biconnected_components.append(component)
            
            elif self.number[w] < self.number[v] and w != parent:
                self.edge_stack.append((v,w))
                self.lowpt[v] = min(self.lowpt[v],self.number[w])

    def find_biconnected_components(self):
        for vertex in self.graph.vertices:
            if vertex not in self.number:
                self.biconnect(vertex,None)
        return self.biconnected_components