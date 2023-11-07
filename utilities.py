CONTRACT_SYMBOL = "+"
INDEX = -1

def rename_vertices_to_contract(vertices_to_contract):
    return CONTRACT_SYMBOL.join(vertices_to_contract)

def expand_contracted_vertices(vertex):
    return vertex.split(CONTRACT_SYMBOL)

def alternate_color():
    global INDEX
    colors = ['red', 'green', 'blue']
   
    INDEX = (INDEX + 1) % len(colors)  
    return colors[INDEX]






    
