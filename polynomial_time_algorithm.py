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
        blocks = biconnectivity_algorithm.find_biconnected_components()

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
        self.graph.show()
        self.graph.vertices_color = {vertex: None for vertex in self.graph.vertices}
        # check if graph is a triangular strip
        if self.graph.is_triangular_strip():
            print("graph is a triangular strip")
            # if so, colour the graph
            # colour_triangular_strip()
        # if not check for all blocks if they are triangular strips
        else:
            for block_id in self.graph.blocks:
                self.colour_block(block_id)

        self.graph.show("three-colouring")

            
    def colour_block(self,block_id):
        if self.graph.blocks[block_id].num_of_vertices < 3:
            return
        if self.graph.blocks[block_id].is_triangle():
            triangle_vertices = self.graph.blocks[block_id].vertices
            posible_colors = self.check_for_possible_colors(triangle_vertices)
            for vertex in triangle_vertices:
                if self.graph.vertices_color[vertex] is None:
                    self.graph.vertices_color[vertex] = posible_colors.pop()
            return
            
            
    def check_for_possible_colors(self,vertices):
        possible_colors = ['red','green','blue']
        for vertex in vertices:
            if self.graph.vertices_color[vertex] is not None:
                possible_colors.remove(self.graph.vertices_color[vertex])

        return possible_colors
    
    
    def run(self):
        return self.three_colouring()