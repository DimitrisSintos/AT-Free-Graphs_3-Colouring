from itertools import combinations
from pyvis.network import Network



class Graph:
    def __init__(self, vertices, edges):
        self.vertices = vertices
        self.edges = edges
        self.adjacency_list = { vertex: set() for vertex in self.vertices}
        for edge in self.edges:
            u, v = edge
            self.adjacency_list[u].add(v)
            self.adjacency_list[v].add(u)
        
    def add_vertex(self, vertex):
        self.vertices.add(vertex)
        
    def add_edge(self, edge):
        self.edges.add(edge)
        self.vertices.update(edge)
        
    def neighbors(self, vertex):
        return {v for u, v in self.edges if u == vertex} | {u for u, v in self.edges if v == vertex}
        
    def get_edges(self, vertex):
        return {(u, v) for u, v in self.edges if u == vertex or v == vertex}
    
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
    
    def block_cutpoint_decomposition(self):
        """
        Decomposes the graph into its biconnected components.

        Returns:
            - A list of blocks, where each block is represented as a set of edges.
            - A set of cutpoints (articulation points).
        """
        time = 0  # Discovery time
        blocks = []  # To store the biconnected components
        cutpoints = set()
        
        # Discovery and low values for each vertex
        disc = [-1] * len(self.vertices)
        low = [-1] * len(self.vertices)
        parent = [-1] * len(self.vertices)
        visited = {v: False for v in self.vertices}
        st = []  # An auxiliary stack
        
        def block_cutpoint_util(v):
            print("v:",v)
            nonlocal time
            children = 0
            visited[v] = True
            disc[v] = time
            low[v] = time
            time += 1
            for u in self.adjacency_list[v]:
                print("u:",u)
                # If u is not visited, make v its parent in DFS tree and recurse for it
                if not visited[u]:
                    children += 1
                    parent[u] = v
                    st.append((v, u))  # Store the edge in stack
                    block_cutpoint_util(u)
                    
                    # Update low value of v
                    low[v] = min(low[v], low[u])
                    
                    # If v is root of DFS tree and has two or more children
                    if parent[v] == -1 and children > 1:
                        cutpoints.add(v)
                        w = -1
                        block = set()
                        # Pop all edges from stack till we reach (v, u)
                        while w != u:
                            w, x = st.pop()
                            block.add((w, x))
                        blocks.append(block)
                    
                    # If v is not root and low value of one of its child is more than discovery value of v
                    elif parent[v] != -1 and low[u] >= disc[v]:
                        cutpoints.add(v)
                        w = -1
                        block = set()
                        while w != u:
                            w, x = st.pop()
                            block.add((w, x))
                        blocks.append(block)
                        
                elif u != parent[v]:
                    low[v] = min(low[v], disc[u])
                    print("Mpanei pote edw??", low[v], disc[u])
                    if disc[u] < disc[v]:
                        st.append((v, u))
        
        for v in self.vertices:
            if not visited[v]:
                block_cutpoint_util(v)
                block = set()
                while st:
                    block.add(st.pop())
                if block:
                    blocks.append(block)
                    
        return blocks, cutpoints
    
    def show(self):
        net = Network()
        net.add_nodes(self.vertices)
        net.add_edges(self.edges)
        net.show("graph.html")


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






# 5-wheel graph
# vertices_5_wheel = ['a','b','c','d','e','f']
# edges_5_wheel = [('a','b'),('a','c'),('a','d'),('b','c'),('c','d'),('b','e'),('c','e'),('c','f'),('d','f'),('e','f')]

# G_5_wheel = Graph(vertices_5_wheel, edges_5_wheel)

# G_5_wheel.show()

# is_condition_met, data = line_3_check(G_5_wheel)
# if is_condition_met:
#     print("data:",data)
#     u, v, common_neighbors = data
#     s = "".join(common_neighbors)
#     new_G_5_wheel = G_5_wheel.contract(common_neighbors)


#     print("IS K4 on recursion:",is_K4_on_recursion(new_G_5_wheel,s))
#     new_G_5_wheel.show()

# Testing:
g = Graph([0, 1, 2, 3, 4, 5], [(0, 1), (1, 2), (0, 2), (2, 3), (3, 4), (4, 5), (3, 5)])
blocks, cutpoints = g.block_cutpoint_decomposition()
print("Blocks:", blocks)
print("Cutpoints:", cutpoints)