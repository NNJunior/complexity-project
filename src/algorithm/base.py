Vertex = int
Graph = dict[Vertex, set]


def V(graph: Graph):
    return set(range(len(graph)))

def is_connected(graph: Graph, X: set):
    visited = {v: False for v in X}

    start = list(X)[0]

    queue = [start]

    while queue:
        v = queue.pop(0)
        visited[v] = True

        for u in graph[v].intersection(X):
            if visited[u]:
                continue
            queue.append(u)
    
    return all(visited.values())

def is_cds(graph: Graph, X: set):
    for v in graph:
        if X.isdisjoint(graph[v]) and v not in X:
            return False
    
    return is_connected(graph, X)
