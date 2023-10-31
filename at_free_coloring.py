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
        print("Ftanw edw?!?!?", start)
        if start is None:
            start = next(iter(self.vertices))
        if visited is None:
            visited = set()
        visited.add(start)
        print("papapapaouuu")
        #check if adjacency_list is an empty set
        if not self.adjacency_list[start]:
            print("adjacency_list is empty set")
            return visited
        
        for neighbor in self.adjacency_list[start]:
            print("edw xalarwnei?!?!?")
            if neighbor not in visited:
                self.dfs(neighbor, visited)
        return visited

    def is_connected(self, start):
        print("adjacency_list:",self.adjacency_list)
        print("Start:",start)
        if not self.vertices:
            return True
        visited = self.dfs(start)
        print("visited:",visited)
        return len(visited) == len(self.vertices)


            




def is_K4(graph):

    for sub_vertices in combinations(graph.vertices, 4):  # all possible 4-vertex combinations
        if all((u, v) in graph.edges or (v, u) in graph.edges for u, v in combinations(sub_vertices, 2)):  # all pairs in subset are connected
            return True
    return False

def is_K4_on_recursion(graph, s):
    """
    Test if the neighborhood of vertex s in graph contains a triangle. 
    This function is designed to be called when Line 1 is reached via recursion.

    :param graph: The graph instance
    :param s: The contracted vertex in the graph
    :return: True if the neighborhood of s contains a triangle, otherwise False
    """
    neighbors = graph.adjacency_list[s]
    for vertex in neighbors:
        for edge in graph.edges:
            u, v = edge
            #If both vertices of the edge are neighbors of s and the edge is not incident to s, then we have a triangle
            if u != s and v != s and u in neighbors and v in neighbors:
                return True
    return False



def line_3_check(graph):
    for edge in graph.edges:
        u, v = edge
        print("u:",u,"v:",v)
        adj_u = graph.adjacency_list[u]
        print("adj_u:",adj_u)

        adj_v = graph.adjacency_list[v]
        print("adj_v:",adj_v)

        common_neighbors = adj_u & adj_v
        print(common_neighbors)
        if len(common_neighbors) >= 2:
            return True, (u, v, common_neighbors)
    return False, None

def has_minimal_stable_separator(block, x):
    x_neighbors = block.adjacency_list[x]
    cond, stable_cutset = is_stable_cutset(block, x, x_neighbors)
    print("cond:",cond)
    print("stable_cutset:",stable_cutset)
    if cond:
        has_minimal_stable_separator = reduce_it_to_minimal_stable_separator(block, x, stable_cutset)
        return True, has_minimal_stable_separator
    else:
        return False


def is_stable_cutset(block, x,S):
    unique_edge  = None
    #find if a unique edge exists in S
    for u, v in combinations(S, 2):
        if (u, v) in block.edges or (v, u) in block.edges:
            unique_edge = (u, v)
    print("exw unique_edge:",unique_edge)
    if unique_edge is None:
        #check if S is stable cutset of block
        print("\nS:",S)
        block_without_S = block.delete_vertices(S)
        print("block_without_S:",block_without_S.adjacency_list)
        if not block_without_S.is_connected(x):
            return True , S
        else:
            return False, None
    else:
        u, v = unique_edge
        S_without_u = S - {u}
        S_without_v = S - {v}
        block_without_S_u = block.delete_vertices(S_without_u)
        print("block_without_S_u:",block_without_S_u.adjacency_list)

        if not block_without_S_u.is_connected(x):
            return True, S_without_u
        
        block_without_S_v = block.delete_vertices(S_without_v)
        print("block_without_S_v:",block_without_S_v.adjacency_list)
        if not block_without_S_v.is_connected(x):
            return True, S_without_v
        
        return False, None
    
def reduce_it_to_minimal_stable_separator(block, x, S):
    separator = S.copy()
    for u in separator:
        if len(S) >= 3:
            S_without_u = S - {u}
            block_without_S_u = block.delete_vertices(S_without_u)
            if not block_without_S_u.is_connected(x):
                S = S_without_u.copy()
        else:
            break
    return S


def line_5_check(graph):
    # Find the biconnected components of the graph
    biconnectivity_algorithm = TarjansBiconnectivity(graph)
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

    for vertex in graph.vertices:
        for block in blocks:
            if vertex in block.vertices and len(block.vertices) >= 3:
                print("Pio vertexaki elenxw?!?!",vertex)
                cond , minimal_stable_separator = has_minimal_stable_separator(block, vertex)
                print("cond:",cond)
                print("minimal_stable_separator:",minimal_stable_separator)
                if cond:
                    return True, (block, minimal_stable_separator)



    return False, None

################### TESTS #####################


# 5-wheel graph
# vertices_5_wheel = ['a','b','c','d','e','f']
# edges_5_wheel = [('a','b'),('a','c'),('a','d'),('b','c'),('c','d'),('b','e'),('c','e'),('c','f'),('d','f'),('e','f')]

# G_5_wheel = Graph(vertices_5_wheel, edges_5_wheel)

# G_5_wheel.show()

# is_condition_met, data = line_3_check(G_5_wheel)
# if is_condition_met:
#     print("data:",data)
#     u, v, common_neighbors = data
#     new_G_5_wheel = G_5_wheel.contract(common_neighbors)


#     print("IS K4 on recursion:",is_K4_on_recursion(new_G_5_wheel,s))
#     new_G_5_wheel.show()

#my graph
# vertices = ['a','b','c','d','e','f','g','h']
# edges = [('a','c'),('b','c'),('c','d'),('c','e'),('c','f'),('b','g'),('e','f'),('e','g'),('f','h'),('d','h'),('g','h')]

# G= Graph(vertices, edges)

# G.show()

# is_condition_met, data = line_3_check(G)
# print("is_condition_met:",is_condition_met)






# Testing line 5:
vertices = ['a','b','c','d','e','f','g','h']
edges = [('a','c'),('b','c'),('c','d'),('c','e'),('c','f'),('b','g'),('e','f'),('e','g'),('f','h'),('d','h'),('g','h')]
g = Graph(vertices, edges)

is_condition_met, data = line_5_check(g)
print("is_condition_met:",is_condition_met)
print("data:",data)
block, minimal_stable_separator = data
new_graph = block.contract(minimal_stable_separator)

cond, data = line_3_check(new_graph)
if cond:
    u, v, common_neighbors = data
    new_graph = new_graph.contract(common_neighbors)
    cond, data = line_3_check(new_graph)
    if cond:
        u, v, common_neighbors = data
        new_graph = new_graph.contract(common_neighbors)

        new_graph.show()

# new_graph.show()


