from itertools import combinations
from pyvis.network import Network


class Graph:
    show_count = 0 # Class-level variable to keep track of show calls

    def __init__(self, vertices, edges):
        self.vertices = vertices
        self.edges = edges
        self.adjacency_list = { vertex: set() for vertex in self.vertices}
        for edge in self.edges:
            u, v = edge
            self.adjacency_list[u].add(v)
            self.adjacency_list[v].add(u)

        self.blocks = {}

    def find_K4(self):

        for sub_vertices in combinations(self.vertices, 4):  # all possible 4-vertex combinations
            if all((u, v) in self.edges or (v, u) in self.edges for u, v in combinations(sub_vertices, 2)):  # all pairs in subset are connected
                return True
        return False

    def find_triangle_in_neighborhood(self, contracted_vertex):
        """
        Test if the neighborhood of contracted_vertex in graph contains a triangle. 
        This function is designed to be called when Line 1 is reached via recursion.

        :param graph: The graph instance
        :param contracted_vertex: The contracted vertex in the graph
        :return: True if the neighborhood of s contains a triangle, otherwise False
        """
        neighbors = self.adjacency_list[contracted_vertex]
        if len(neighbors) <= 3:
            return False
        else:
            for sub_vertices in combinations(neighbors, 3):
                if all((u, v) in self.edges or (v, u) in self.edges for u, v in combinations(sub_vertices, 2)):
                    return True             

        return False
    
    def find_diamond(self):
        for edge in self.edges:
            u, v = edge
            adj_u = self.adjacency_list[u]

            adj_v = self.adjacency_list[v]

            common_neighbors = adj_u & adj_v

            if len(common_neighbors) >= 2:
                return common_neighbors
        return None
    
    def contract(self, vertices_to_contract):
        """
        Contract a set of vertices into a single vertex.
        
        :param vertices_to_contract: set of vertices to contract
        :return: A new Graph instance with the vertices contracted.
        """

        #All vertices to contract will be replaced by a new vertex
        new_vertex = "".join(vertices_to_contract)
        new_vertices = [v for v in self.vertices if v not in vertices_to_contract] + [new_vertex]

        # All edges incident to a vertex in vertices_to_contract will now be incident to new_vertex
        new_edges = []
        for u, v in self.edges:
            if u in vertices_to_contract and v in vertices_to_contract:
                # Ignore edges within the contracted set
                continue
            elif u in vertices_to_contract:
                new_edges.append((new_vertex, v))
            elif v in vertices_to_contract:
                new_edges.append((u, new_vertex))
            else:
                new_edges.append((u, v))
        
        return Graph(new_vertices, new_edges)
    
    def update_adjacency_list(self):
        new_vertices = []
        new_edges = []
        for block_id in self.blocks:
            block = self.blocks[block_id]
            new_vertices += block.vertices
            new_edges += block.edges


        print("new vertices:",new_vertices)
        #delete adjacency list

        self.vertices = new_vertices
        self.edges = new_edges


        self.adjacency_list = { vertex: set() for vertex in new_vertices}

        for block in self.blocks.values():
            print("block:",block)
            for vertex in block.vertices:
                self.adjacency_list[vertex] = block.adjacency_list[vertex]
        print("updated adjacency list:",self.adjacency_list)

        

    
    def copy(self):
        return Graph(self.vertices.copy(), self.edges.copy())
    

    def show(self):
        Graph.show_count += 1
        print("Showing graph:",Graph.show_count)
        net = Network()

        if self.blocks != {}:
            for block_id in self.blocks:
                block = self.blocks[block_id]
                net.add_nodes(block.vertices)
                net.add_edges(block.edges)
        else:
            net.add_nodes(self.vertices)
            net.add_edges(self.edges)
        
        file_name = f"graph-{Graph.show_count}.html"
        net.show(file_name)







