from graph import Graph

class CheckAlgorithmCorrectness:
    def __init__(self,graph:Graph):
        self.graph = graph

    def check_colors(self):
        for vertex in self.graph.vertices:
            for neighbor in self.graph.adjacency_list[vertex]:
                if self.graph.vertices_color[vertex] == self.graph.vertices_color[neighbor]:
                    return False
        return True
    
    def run(self):
        return "The graph is correct 3-colourable" if  "The graph is 3-colourable" else "Wrong 3-colouring"