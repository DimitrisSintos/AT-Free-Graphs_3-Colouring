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
        try:
            line_1_result = self.line_1_check()
            if line_1_result:
                print("Line 1 check failed. Not three-colorable.")
                return False

            line_3_condition, vertices_to_contract = self.line_3_check()
            if line_3_condition:
                
                self.perform_contraction(vertices_to_contract)
                return self.three_colouring()

            line_5_condition,data = self.line_5_check()

            if line_5_condition:
                block_id, minimal_stable_separator = data
                self.perform_contraction(minimal_stable_separator,block_id)
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
        # Find the biconnected components of the graph
        biconnectivity_algorithm = TarjansBiconnectivity(self.graph)
        blocks = biconnectivity_algorithm.find_biconnected_components()

        # delete old blocks from graph and add the new blocks
        self.graph.blocks = {}

        for i, block in enumerate(blocks):
            self.graph.blocks[i] = block

        for vertex in self.graph.vertices:
            for block_id in self.graph.blocks:
               
                block = self.graph.blocks[block_id]
                if vertex in block.vertices and len(block.vertices) >= 3:
                    cond , minimal_stable_separator = block.find_minimal_stable_separator(vertex)
                    if cond:
                        return True, (block_id, minimal_stable_separator)

        return False, None

    def perform_contraction(self, vertices_to_contract,block_id=None,):
        old_graph = self.graph.copy()
        self.graph_snapshots.append(old_graph)
        if block_id != None:
            print("Type of block:",type(self.graph.blocks[block_id]))
            self.graph.blocks[block_id] = self.graph.blocks[block_id].contract_block(vertices_to_contract)
            self.graph.update_adjacency_list()
        else:
            self.graph = self.graph.contract(vertices_to_contract)
        self.contracted_vertex = rename_vertices_to_contract(vertices_to_contract)
        self.is_recursive_call = True
        self.graph.show()
    
    def construct_three_colouring(self):
        print("constructing three colouring...")
        self.graph.show()
        pass
    
    
    
    def run(self):
        return self.three_colouring()