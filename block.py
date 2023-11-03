from itertools import combinations
from graph import Graph

class Block(Graph):
    def __innit__(self,vertices, edges):
        super().__init__(vertices, edges)    
    
    def find_minimal_stable_separator(self, x):
        x_neighbors = self.adjacency_list[x]
        cond, stable_cutset = self.find_stable_cutset(x, x_neighbors)
        
        if cond:
            minimal_stable_separator = self.reduce_cutset_to_minimal_stable_separator(x, stable_cutset)
            return True, minimal_stable_separator
        else:
            return False, None
    
    def find_stable_cutset(self, starting_vertex, S):
        unique_edge  = None
        #find if a unique edge exists in S
        for u, v in combinations(S, 2):
            if (u, v) in self.edges or (v, u) in self.edges:
                unique_edge = (u, v)
        if unique_edge is None:
            #check if S is stable cutset of block
            block_without_S = self.delete_vertices(S)
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
            if len(S) >= 3:
                S_without_u = S - {u}
                block_without_S_u = self.delete_vertices(S_without_u)
                if not block_without_S_u.is_connected(starting_vertex):
                    S = S_without_u.copy()
            else:
                break
        return S
    
    def delete_vertices(self, vertices_to_delete):
        """
        Delete a set of vertices from the block.
        
        :param vertices_to_delete: set of vertices to delete
        :return: A new Block instance with the vertices deleted.
        """
        new_veriteces = self.vertices - vertices_to_delete
        new_edges = [e for e in self.edges if e[0] not in vertices_to_delete and e[1] not in vertices_to_delete]
        return Block(new_veriteces,new_edges)
    
    def is_connected(self, start):
        if not self.vertices:
            return True
        visited = self.dfs(start)

        return len(visited) == len(self.vertices)
    
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
        
    
    
        
    