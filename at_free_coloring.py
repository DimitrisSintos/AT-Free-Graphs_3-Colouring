from itertools import combinations
from pyvis.network import Network

from biconnectivity import TarjansBiconnectivity



class Graph:
    def __init__(self, vertices, edges):
        self.vertices = vertices
        self.edges = edges
        self.adjacency_list = { vertex: set() for vertex in self.vertices}
        for edge in self.edges:
            u, v = edge
            self.adjacency_list[u].add(v)
            self.adjacency_list[v].add(u)

    def find_K4(self):

        for sub_vertices in combinations(self.vertices, 4):  # all possible 4-vertex combinations
            if all((u, v) in self.edges or (v, u) in self.edges for u, v in combinations(sub_vertices, 2)):  # all pairs in subset are connected
                return True
        return False

    def find_triangle_in_neighborhood(self, contracted_vertex):#TODO
        """
        Test if the neighborhood of contracted_vertex in graph contains a triangle. 
        This function is designed to be called when Line 1 is reached via recursion.

        :param graph: The graph instance
        :param contracted_vertex: The contracted vertex in the graph
        :return: True if the neighborhood of s contains a triangle, otherwise False
        """
        neighbors = self.adjacency_list[contracted_vertex]
        for edge in self.edges:
            u, v = edge
            #If both vertices of the edge are neighbors of s and the edge is not incident to s, then we have a triangle
            if u != contracted_vertex and v != contracted_vertex and u in neighbors and v in neighbors:
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
    
    def copy(self):
        return Graph(self.vertices.copy(), self.edges.copy())
    

    def show(self):
        net = Network()
        net.add_nodes(self.vertices)
        net.add_edges(self.edges)
        net.show("graph.html")


class Block(Graph):
    def __innit__(self,vertices, edges):
        super().__init__(vertices, edges)


    def delete_vertices(self, vertices_to_delete):
        """
        Delete a set of vertices from the block.
        
        :param vertices_to_delete: set of vertices to delete
        :return: A new Block instance with the vertices deleted.
        """
        new_veriteces = self.vertices - vertices_to_delete
        new_edges = [e for e in self.edges if e[0] not in vertices_to_delete and e[1] not in vertices_to_delete]
        return Block(new_veriteces,new_edges)
    
    def dfs(self, start=None, visited=None):
        if start is None:
            start = next(iter(self.vertices))
        if visited is None:
            visited = set()
        visited.add(start)

        if not self.adjacency_list[start]:
            return visited
        
        for neighbor in self.adjacency_list[start]:
            if neighbor not in visited:
                self.dfs(neighbor, visited)
        return visited

    def is_connected(self, start):
        if not self.vertices:
            return True
        visited = self.dfs(start)

        return len(visited) == len(self.vertices)
    
    def find_minimal_stable_separator(self, x):
        x_neighbors = self.adjacency_list[x]
        cond, stable_cutset = self.find_stable_cutset(x, x_neighbors)
        print("cond:",cond)
        print("stable_cutset:",stable_cutset)
        if cond:
            minimal_stable_separator = self.reduce_cutset_to_minimal_stable_separator(x, stable_cutset)
            return True, minimal_stable_separator
        else:
            return False
        
    
    def find_stable_cutset(self, starting_vertex, S):
        unique_edge  = None
        #find if a unique edge exists in S
        for u, v in combinations(S, 2):
            if (u, v) in self.edges or (v, u) in self.edges:
                unique_edge = (u, v)
        print("exw unique_edge:",unique_edge)
        if unique_edge is None:
            #check if S is stable cutset of block
            print("\nS:",S)
            block_without_S = self.delete_vertices(S)
            print("block_without_S:",block_without_S.adjacency_list)
            if not block_without_S.is_connected(starting_vertex):
                return True , S
            else:
                return False, None
        else:
            u, v = unique_edge
            S_without_u = S - {u}
            S_without_v = S - {v}
            block_without_S_u = self.delete_vertices(S_without_u)

            if not block_without_S_u.is_connected(starting_vertex):
                return True, S_without_u
            
            block_without_S_v = self.delete_vertices(S_without_v)
            if not block_without_S_v.is_connected(starting_vertex):
                return True, S_without_v
            
            return False, None
        
    def reduce_cutset_to_minimal_stable_separator(self, starting_vertex, S):
        separator = S.copy()
        for u in separator:
            if len(S) >= 3:#TODO
                S_without_u = S - {u}
                block_without_S_u = self.delete_vertices(S_without_u)
                if not block_without_S_u.is_connected(starting_vertex):
                    S = S_without_u.copy()
            else:
                break
        return S
    

class PolynomialTimeAlgorithm:
    def __init__(self,graph):
        self.graph = graph
        self.is_recursive_call = False
        self.graph_snapshots = []
        self.contracted_vertex = None

    def three_colouring(self):
        try:
            line_1_result = self.line_1_check()
            if line_1_result:
                print("Line 1 check failed. Not three-colorable.")
                return False

            line_3_condition, vertices_to_contract = self.line_3_check()
            if line_3_condition:
                print("Contracting based on line 3 check...")
                self.perform_contraction(vertices_to_contract)
                return self.three_colouring()

            line_5_condition, (block, minimal_stable_separator) = self.line_5_check()
            print("line_5_ result:",  minimal_stable_separator,block)
            if line_5_condition:
                print("Contracting based on line 5 check...")
                self.perform_contraction(minimal_stable_separator,block)
                return self.three_colouring()

            return self.construct_three_colouring()
        except Exception as e:
            print(f"An exception occurred: {e}")
            raise

    def perform_contraction(self, vertices_to_contract,block=None,):
        old_graph = self.graph.copy()
        self.graph_snapshots.append(old_graph)
        print("block:",block)
        if block:
            self.graph = block.contract(vertices_to_contract)
        else:
            self.graph = self.graph.contract(vertices_to_contract)
        self.contracted_vertex = "".join(vertices_to_contract)
        self.is_recursive_call = True
        self.graph.show()
    
    def construct_three_colouring(self):
        print("constructing three colouring...")
        pass
    
    
    def line_1_check(self):
        if self.is_recursive_call:
            print("Line 1 check on recursion...", self.contracted_vertex)
            #TODO
            # return self.graph.find_triangle_in_neighborhood(self.contracted_vertex)
            return self.graph.find_K4()
        else:
            return self.graph.find_K4()

    def line_3_check(self):
        result = self.graph.find_diamond()
        if result is None:
            return False , None
        else:
            return True , result


    def line_5_check(self):
        # Find the biconnected components of the graph
        biconnectivity_algorithm = TarjansBiconnectivity(self.graph)
        biconnected_components = biconnectivity_algorithm.find_biconnected_components()
        print("biconnected_components:",biconnected_components, len(biconnected_components))
        blocks = []
        for component in biconnected_components:
            vertices = set()
            edges = set()
            for edge in component:
                u, v = edge
                vertices.add(u)
                vertices.add(v)
                edges.add(edge)
            blocks.append(Block(vertices, edges))

        for vertex in self.graph.vertices:
            for block in blocks:
                if vertex in block.vertices and len(block.vertices) >= 3:
                    cond , minimal_stable_separator = block.find_minimal_stable_separator(vertex)
                    print("minimal_stable_separator:",minimal_stable_separator)
                    if cond:
                        return True, (block, minimal_stable_separator)



        return False, None
    
    def run(self):
        return self.three_colouring()



if __name__ == "__main__":
    vertices = ['a','b','c','d','e','f','g','h']
    edges = [('a','c'),('b','c'),('c','d'),('c','e'),('c','f'),('b','g'),('e','f'),('e','g'),('f','h'),('d','h'),('g','h')]
    g = Graph(vertices, edges)
    g.show()
    algorithm = PolynomialTimeAlgorithm(g)
    algorithm.run()


