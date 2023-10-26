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
        visited = {vertex : False for vertex in self.vertices}
        disc = {vertex : -1 for vertex in self.vertices}
        low = {vertex : -1 for vertex in self.vertices}
        parent = {vertex : None for vertex in self.vertices}
        st = []
        time = 0
        blocks = []
        cutpoints = set()

        def tarjan_DFS(u, visited, disc, low, st, parent,time, blocks,cutpoints):
            children = 0
            visited[u] = True
            st.append(u)
            print("not visited vertex in st:",st)


            disc[u] = time
            low[u] = time
            time += 1

            for v in self.adjacency_list[u]:
                if not visited[v]:
                    children +=1
                    parent[v] = u
                    tarjan_DFS(v, visited, disc, low, st, parent,time, blocks,cutpoints)

                    low[u] = min(low[u], low[v])
                    
                    print("aaaaaaaaaaaaaaaa",u)

                    if parent[u] is None and children > 1:
                        print("children", children)
                        cutpoints.add(u)
                        block = []
                        while st[-1] != u:
                            block.append(st.pop())
                        block.append(st.pop())
                        blocks.append(block)

                    elif parent[u] is not None and low[v] >= disc[u]:
                        print("low[v]", low[v])
                        print("disc[u]", disc[u])
                        cutpoints.add(u)
                        block = []
                        while st[-1] != u:
                            block.append(st.pop())
                        block.append(st.pop())
                        blocks.append(block)

                elif v != parent[u]:#back edge
                    low[u] = min(low[u], disc[v])

                    


        for vertex in self.vertices:
            if not visited[vertex]:
                print("not viseted vertex:",vertex)
                tarjan_DFS(vertex, visited, disc, low, st, parent,time, blocks,cutpoints)
            
            if st:
                block = []
                while st:
                    block.append(st.pop())
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

def is_stable_cutset(graph, block, x):
    # Define the neighbors of x within the block
    neighbors = graph.adjacency_list[x].intersection(block)
    unique_edges = [(u, v) for u in neighbors for v in graph.adjacency_list[u].intersection(neighbors)]
    
    # Check if NB(x) is a stable cutset of B
    if len(unique_edges) <= 1 and not any((u, v) in graph.edges or (v, u) in graph.edges for u, v in combinations(neighbors, 2)):
        return True, neighbors
    
    # Check the other conditions (NB(x) \ {u} and NB(x) \ {v})
    for u, v in unique_edges:
        cutset_minus_u = neighbors - {u}
        cutset_minus_v = neighbors - {v}
        
        if not any((a, b) in graph.edges or (b, a) in graph.edges for a, b in combinations(cutset_minus_u, 2)):
            return True, cutset_minus_u
        if not any((a, b) in graph.edges or (b, a) in graph.edges for a, b in combinations(cutset_minus_v, 2)):
            return True, cutset_minus_v

    return False, None

def line_5_check(graph):
    blocks, _ = graph.block_cutpoint_decomposition()

    for block in blocks:
        print("block:", block)
        if len(block) < 3:
            continue
        for x in graph.vertices:
            if x not in block:
                continue
            is_cutset, cutset = is_stable_cutset(graph, block, x)
            if is_cutset:
                # Reducing to a minimal stable separator
                for vertex in cutset:
                    temp_cutset = cutset - {vertex}
                    temp_is_cutset, _ = is_stable_cutset(graph, block, x)
                    if temp_is_cutset:
                        cutset = temp_cutset
                if len(cutset) >= 2:
                    return True, cutset
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
is_condition_met, cutset = line_5_check(g)
print("is_condition 5 met :",is_condition_met)
print("cutset:",cutset, type(cutset))
if is_condition_met and cutset:
    new_g = g.contract(cutset)
    new_g.show()



