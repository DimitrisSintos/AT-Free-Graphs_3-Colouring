from block import Block

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

    def find_biconnected_components(self):
        for vertex in self.graph.vertices:
            if vertex not in self.number:
                self.biconnect(vertex,None)

        components_vertices, components_edges = self.process_biconnected_components(self.biconnected_components)
        blocks = self.create_blocks_from_components(components_vertices, components_edges)
        return blocks

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

    def process_biconnected_components(self,biconnected_components):
        # Initialize arrays for component vertices and edges
        components_vertices = []
        components_edges = []

        # Create a set for all vertices that are part of a component
        vertices_in_component = set()

        # Check each component
        for component in biconnected_components:
            unique_vertices = set(vertex for edge in component for vertex in edge)
            if len(unique_vertices) >= 3:
                # Add to the set of vertices that are part of a component
                vertices_in_component.update(unique_vertices)
                components_vertices.append(list(unique_vertices))
                components_edges.append(component)

        # Find the vertices that are not part of any component
        isolated_vertices = [vertex for vertex in self.graph.vertices if vertex not in vertices_in_component]

        # Add isolated vertices as separate components
        for vertex in isolated_vertices:
            components_vertices.append([vertex])
            components_edges.append([])  # No edges in a single-vertex component

        return components_vertices, components_edges

        
    
    def create_blocks_from_components(self, component_vertices, component_edges):
        blocks = []
        for i in range(len(component_vertices)):
            block = Block(set(component_vertices[i]), component_edges[i])
            blocks.append(block)
        return blocks
    