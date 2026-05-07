from .base import *

def dummy_cds(graph: Graph):
    if not is_connected(graph, V(graph)):
        return None
    
    result = V(graph)
    current_cds = set()
    
    def iter_vertex(v: Vertex):
        nonlocal result, current_cds
        if (v == len(graph)):
            if is_cds(graph, current_cds) and len(result) > len(current_cds):
                result = current_cds.copy()
            return
        
        iter_vertex(v + 1)
        current_cds.add(v)

        iter_vertex(v + 1)
        current_cds.remove(v)
    
    iter_vertex(0)
                
    return result
