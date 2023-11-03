import unittest
from graph import Graph, is_K4, line_3_check

class Test(unittest.TestCase):
    def setUp(self):
        self.vertices = ['a','b','c','d','e','f','g','h']
        self.edges = [('a','c'),('b','c'),('c','d'),('c','e'),('c','f'),('b','g'),('e','f'),('e','g'),('f','h'),('d','h'),('g','h')]
        self.G = Graph(self.vertices, self.edges)
        
        self.vertices_K4 = ['x','y','z','w','a']
        self.edges_K4 = [('x', 'y'), ('x', 'z'), ('x', 'w'), ('y', 'z'), ('y', 'w'), ('z', 'w'),('x','a')]
        self.G_K4 = Graph(self.vertices_K4, self.edges_K4) 

        self.vertices_5_wheel = ['a','b','c','d','e', 'f']
        self.edges_5_wheel = [('a','b'),('a','c'),('a','d'),('b','c'),('c','d'),('b','e'),('c','e'),('c','f'),('d','f'),('e','f')]
        self.G_5_wheel = Graph(self.vertices_5_wheel, self.edges_5_wheel)

    def tearDown(self):
        pass

    def test_is_K4(self):
        result = is_K4(self.G)
        self.assertEqual(result, False)
        result = is_K4(self.G_K4)
        self.assertEqual(result, True)

    
    
   



if __name__ == '__main__':
    unittest.main()
    



 