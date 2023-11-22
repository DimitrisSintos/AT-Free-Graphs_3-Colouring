from utilities import *
from graph import Graph
from tarjans_biconnectivity import TarjansBiconnectivity
from block_cutpoint_tree import BlockCutpointTree
from itertools import combinations


#TODO:
# 1: check for you find the trinagles of degree 3
# 2: check for block connecting by a bridge and no a cutpoint

class PolynomialTimeAlgorithm:
    def __init__(self,graph):
        self.graph = graph
        self.is_recursive_call = False
        self.graph_snapshots = []
        self.contracted_vertex = None

        self.previous_triangle = None

    def three_colouring(self):
        self.graph_snapshots.append(self.graph.copy())
        try:
            line_1_result = self.line_1_check()
            if line_1_result:
                print("Line 1 check failed. There is a K4 in the graph so it is not 3-colourable.")
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

        if len(self.graph.blocks) == 1:
            #Then the graph is a triangle or a triangular strip
            if self.graph.is_triangle():
                self.colour_triangle(self.graph.vertices)
            else:#graph is a triangular strip
                self.colour_trianglular_strip(self.graph.copy())
        else:
            #create block-cutpoint tree
            block_cutpoint_tree = BlockCutpointTree(self.graph.blocks, self.graph.cutpoints)
            block_cutpoint_tree.show()
            for block_id in self.graph.blocks:
                print("block id:",block_id, "block vertices:",self.graph.blocks[block_id].vertices)

            next_block_id = block_cutpoint_tree.get_next_block()
            while next_block_id is not None:
                print("\nIm colouring block:",next_block_id)
                block = self.graph.blocks[next_block_id]
                print("block vertices:",block.vertices)
                if block.num_of_vertices < 3:
                    pass # we will colour this block later
                elif block.num_of_vertices == 3:
                    self.colour_triangle(block.vertices)
                else: # block is a triangular strip
                    triangular_strip = block.copy()
                    next_vertex = None
                    is_cutpoint = False
                    for vertex in triangular_strip.vertices:
                        if vertex in self.graph.cutpoints and self.graph.vertices_color[vertex] is not None:
                            next_vertex = vertex
                            is_cutpoint = True
                            break
                    self.colour_trianglular_strip(triangular_strip,next_vertex, is_cutpoint)



                next_block_id = block_cutpoint_tree.get_next_block()
                print("next block id:",next_block_id)


            self.colour_remaining_vertices()

        self.graph.show("three colouring before expansion") 
       

        initial_graph = self.colour_initial_graph()

        initial_graph.show("three-colouring")

    def colour_triangle(self,triangle_vertices):

        cutpoint = None
        available_colors = {'red', 'green', 'blue'}

        if self.graph.cutpoints:
            for vertex in triangle_vertices:
                if vertex in self.graph.cutpoints and self.graph.vertices_color[vertex] is not None:
                    available_colors.remove(self.graph.vertices_color[vertex])
                    cutpoint = vertex
                    break
                
    
        for vertex in triangle_vertices:
            if vertex  != cutpoint:
                self.graph.vertices_color[vertex] = available_colors.pop()

    def colour_trianglular_strip(self,triangular_strip, next_vertex=None,is_cutpoint=False):
        if triangular_strip.num_of_vertices == 6:
            #then the triangular strip is a prism
            print("next vertex:",next_vertex)
            self.colour_prism(triangular_strip, next_vertex)
            return
        
        if next_vertex is None:
            first_triangle,next_vertex = self.find_init_triangle_in_strip(triangular_strip)
            self.colour_triangle(first_triangle)
            self.previous_triangle = first_triangle
            triangular_strip = triangular_strip.delete_vertices(first_triangle)
            self.colour_trianglular_strip(triangular_strip, next_vertex)
        elif next_vertex is not None and is_cutpoint:
            triangle,next_vertex = self.find_triangle_in_strip(next_vertex,triangular_strip)
            self.colour_triangle(triangle)
            self.previous_triangle = triangle
            triangular_strip = triangular_strip.delete_vertices(triangle)
            self.colour_trianglular_strip(triangular_strip, next_vertex)
        else:
            triangle,next_vertex = self.find_triangle_in_strip(next_vertex,triangular_strip)
            self.colour_triangle_of_trianglular_strip(triangle)
            self.previous_triangle = triangle
            triangular_strip = triangular_strip.delete_vertices(triangle)
            self.colour_trianglular_strip(triangular_strip, next_vertex)
            
        

    def find_triangle_in_strip(self,vertex,triangular_strip):
        triangle = {vertex}
        next_vertex = None
        for neighbour in triangular_strip.adjacency_list[vertex]:
            if len(triangular_strip.adjacency_list[neighbour]) == 3:
                triangle.add(neighbour)
            
            else:
                next_vertex = neighbour

        return triangle, next_vertex

    def find_init_triangle_in_strip(self,triangular_strip):
        for vertex in triangular_strip.vertices:
            if len(triangular_strip.adjacency_list[vertex]) == 3:
                triangle,next_vertex = self.find_triangle_in_strip(vertex,triangular_strip)
                return triangle,next_vertex
            
    
            
    def colour_triangle_of_trianglular_strip(self,triangle):
        for vertex in triangle:
            for previous_vertex in self.previous_triangle:
                if previous_vertex in self.graph.adjacency_list[vertex]:
                    previous_vertex_color = self.graph.vertices_color[previous_vertex]
                    self.graph.vertices_color[vertex] = get_next_colour(previous_vertex_color)
                    break

    def colour_prism(self,prism,next_vertex):
        first_triangle, second_triangle = self.find_triangles_in_prism(prism)
        print('first triangle:', first_triangle)
        print('second triangle:', second_triangle)

        print("previous triangle:",self.previous_triangle)

        if next_vertex is None:
            self.colour_triangle(first_triangle)
            self.previous_triangle = first_triangle
            self.colour_triangle_of_trianglular_strip(second_triangle)

        else:
            if next_vertex in first_triangle:
                self.colour_triangle_of_trianglular_strip(first_triangle)
                self.previous_triangle = first_triangle
                self.colour_triangle_of_trianglular_strip(second_triangle)
            else:
                self.colour_triangle_of_trianglular_strip(second_triangle)
                self.previous_triangle = second_triangle
                self.colour_triangle_of_trianglular_strip(first_triangle)
            

    def find_triangles_in_prism(self,prism):
        first_triangle = set()
        second_triangle = set()
        prism_vertices = prism.vertices
        for vertices in combinations(prism_vertices,3):
           if self.graph.edge_exists(vertices[0],vertices[1]) and\
                self.graph.edge_exists(vertices[1],vertices[2]) and \
                    self.graph.edge_exists(vertices[2],vertices[0]):
               first_triangle = set(vertices)
               break


        second_triangle = prism_vertices - first_triangle

        return first_triangle, second_triangle

    def colour_remaining_vertices(self):
        none_coloured_vertices = [vertex for vertex in self.graph.vertices if self.graph.vertices_color[vertex] is None]
        print("none coloured vertices:",none_coloured_vertices)
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