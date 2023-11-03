from graph import Graph
from tarjans_biconnectivity import TarjansBiconnectivity
from polynomial_time_algorithm import PolynomialTimeAlgorithm

def main():
    vertices = ['a','b','c','d','e','f','g','h']
    edges = [('a','c'),('b','c'),('c','d'),('c','e'),('c','f'),('b','g'),('e','f'),('e','g'),('f','h'),('d','h'),('g','h')]
    g = Graph(vertices, edges)
    g.show()
    algorithm = PolynomialTimeAlgorithm(g)
    algorithm.run()

    # vertices_K4 = ['x','y','z','w','a']
    # edges_K4 = [('x', 'y'), ('x', 'z'), ('x', 'w'), ('y', 'z'), ('y', 'w'), ('z', 'w'),('x','a')]
    # G_K4 = Graph(vertices_K4, edges_K4)
    # G_K4.show()
    # result = G_K4.find_triangle_in_neighborhood('x')

    # print("Has triangle:", result)

    # vertices = ['a','b','c']
    # edges = [('a','b'),('b','c'), ('a','c')]
    # g = Graph(vertices, edges)
    # # g.show()
    # biconnectivity_algorithm = TarjansBiconnectivity(g)
    # biconnected_components = biconnectivity_algorithm.find_biconnected_components()
    # print("biconnected_components:",biconnected_components)





if __name__ == "__main__":
    main()