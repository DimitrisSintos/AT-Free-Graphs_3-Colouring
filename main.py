from graph import Graph
from tarjans_biconnectivity import TarjansBiconnectivity
from polynomial_time_algorithm import PolynomialTimeAlgorithm

from graph_parser import GraphParser


import sys

def main(argv):
    file_path = None
    num_of_vertices = None
    num_of_edges = None
    edges = None
    AT_free_graph = None

    if argv != []:
        file_path = argv[0]
    
    if file_path is None:
        num_of_vertices = 8
        num_of_edges = 11
        edges = [
                (0,1),
                (1,2),
                (1,5),
                (1,3),
                (1,4),
                (2,6),
                (3,6),
                (3,4),
                (4,7),
                (6,7),
                (5,7)
            ]
        AT_free_graph = Graph(num_of_vertices, num_of_edges, edges)
    else:
        AT_free_graph = GraphParser.parse_graph_from_file(file_path)
    



    AT_free_graph.show()
    algorithm = PolynomialTimeAlgorithm(AT_free_graph)
    algorithm.run()


if __name__ == "__main__":
    main(argv=sys.argv[1:])