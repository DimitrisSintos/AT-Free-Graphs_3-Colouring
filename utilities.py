CONTRACT_SYMBOL = "+"

def rename_vertices_to_contract(vertices_to_contract):
    return CONTRACT_SYMBOL.join(vertices_to_contract)

def expand_contracted_vertices(vertex):
    return vertex.split(CONTRACT_SYMBOL)

def get_next_colour(color=None):
    if color == "red":
        return "green"
    elif color == "green":
        return "blue"
    elif color == "blue":
        return "red"
    else:
        return "red"




    
