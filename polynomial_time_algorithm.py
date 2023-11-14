from utilities import *
from graph import Graph
from tarjans_biconnectivity import TarjansBiconnectivity

class PolynomialTimeAlgorithm:
    def __init__(self,graph):
        self.graph = graph
        self.is_recursive_call = False
        self.graph_snapshots = []
        self.contracted_vertex = None

    def three_colouring(self):
        self.graph_snapshots.append(self.graph.copy())
        try:
            line_1_result = self.line_1_check()
            if line_1_result:
                print("Line 1 check failed. Not three-colorable.")
                return False

            line_3_condition, vertices_to_contract = self.line_3_check()
            if line_3_condition:
                
                self.perform_contraction(vertices_to_contract)
                return self.three_colouring()

            line_5_condition,minimal_stable_separator = self.line_5_check()

            if line_5_condition:
                self.perform_contraction(minimal_stable_separator)
                return self.three_colouring()

            return self.construct_three_colouring()
        except Exception as e:
            print(f"An exception occurred: {e}")
            raise

    def line_1_check(self):
        if self.is_recursive_call:
            return self.graph.find_triangle_in_neighborhood(self.contracted_vertex)
            # return self.graph.find_K4()
        else:
            return self.graph.find_K4()

    def line_3_check(self):
        result = self.graph.find_diamond()
        if result is None:
            return False , None
        else:
            return True , result


    def line_5_check(self):
        """
        this should run in O(n*m) time
        if G contains a minimal stable separator S with |S| ≥ 2 then
            Recursively find a 3-colouring of G/S
        """
        # Find the biconnected components of the graph
        biconnectivity_algorithm = TarjansBiconnectivity(self.graph)
        blocks, self.graph.cutpoints = biconnectivity_algorithm.find_biconnected_components()

        print("cutpoints:",self.graph.cutpoints)

        # delete old blocks from graph and add the new blocks
        self.graph.blocks = {}

        for i, block in enumerate(blocks):# i represents the block id
            self.graph.blocks[i] = block


        for vertex in self.graph.vertices:
            for block_id in self.graph.blocks:
               
                block = self.graph.blocks[block_id]
                if vertex in block.vertices and len(block.vertices) >= 3:
                    cond , minimal_stable_separator = block.find_minimal_stable_separator(vertex)
                    if cond:
                        return True,  minimal_stable_separator

        return False, None

    def perform_contraction(self, vertices_to_contract):
        old_graph = self.graph.copy()
        self.graph_snapshots.append(old_graph)
        self.graph = self.graph.contract(vertices_to_contract)
        self.contracted_vertex = rename_vertices_to_contract(vertices_to_contract)
        self.is_recursive_call = True
        self.graph.show("contracted-graph")
    
    def construct_three_colouring(self):
        print("constructing three colouring...")
        self.graph.vertices_color = {vertex: None for vertex in self.graph.vertices}

        if self.graph.blocks == {}:
            #Then the graph is a triangle or a triangular strip
            if self.graph.is_triangle():
                self.colour_triangle(self.graph)
            else:
                print("colouring triangular strip")
        else:
            #colour blocks
            for block_id in self.graph.blocks:
                block = self.graph.blocks[block_id]
                if block.num_of_vertices < 3:
                    pass # we will colour this block later
                elif block.num_of_vertices == 3:
                    self.colour_triangle(block)
                else: # block is a triangular strip
                    print("colouring triangular strip in block")

            
            


        self.colour_remaining_vertices()

        self.graph.show("three colouring before expansion") 
       

        initial_graph = self.colour_initial_graph()

        initial_graph.show("three-colouring")

    def colour_triangle(self,triangle):
        triangle_vertices = triangle.vertices

        available_colors = {'red', 'green', 'blue'}

        for vertex in triangle_vertices:
            self.graph.vertices_color[vertex] = available_colors.pop()

    def colour_remaining_vertices(self):
        none_coloured_vertices = [vertex for vertex in self.graph.vertices if self.graph.vertices_color[vertex] is None]
        for vertex in none_coloured_vertices:
            available_colors = {'red', 'green', 'blue'}
            for neighbour in self.graph.adjacency_list[vertex]:
                if self.graph.vertices_color[neighbour] in available_colors:
                    available_colors.remove(self.graph.vertices_color[neighbour])
            self.graph.vertices_color[vertex] = available_colors.pop()




    def colour_initial_graph(self):
        initial_graph = self.graph_snapshots[0]
        
        initial_graph.vertices_color = {vertex: None for vertex in initial_graph.vertices}

        for vertex in self.graph.vertices:
            expanded_vertices = expand_contracted_vertices(vertex)
            for expanded_vertex in expanded_vertices:
                initial_graph.vertices_color[expanded_vertex] = self.graph.vertices_color[vertex]

        return initial_graph

    
    
    def run(self):
        return self.three_colouring()