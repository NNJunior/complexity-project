Vertex = int
Graph = dict[Vertex, set]

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

def V(graph: Graph):
    return set(range(len(graph)))

def free(graph: Graph, S: set, D: set):
    return V(graph).difference(set.union(*(graph[v] for v in S)))

def available(graph: Graph, S: set, D: set):
    return V(graph).difference(S).difference(D)

def candidates(graph: Graph, S: set, D: set):
    return available(graph, S, D).intersection(set.union(*(graph[v] for v in S)))

def is_promise(graph: Graph, S: set, D: set, v: Vertex):
    return (v in available(graph, S, D)) and not is_cds(graph, set(range(len(graph))).difference(D.union({v})))

def is_correct(graph: Graph, S: set, D: set):
    return is_cds(graph, V(graph).difference(D)) or (not S.isdisjoint(D))




def reduction(graph: Graph, S: set, D: set):
    def perform_a():
        for v in graph:
            if is_promise(graph, S, D, v):
                S.add(v)
                return True
        return False
    
    def perform_b():
        for v in candidates(graph, S, D):
            for u in candidates(graph, S, D):
                v_set = free(graph, S, D).intersection(graph[v])
                u_set = free(graph, S, D).intersection(graph[u])

                if v_set.issubset(u_set):
                    D.add(v)
                    return True
        return False
    
    def perform_c():
        for v in available(graph, S, D):
            if graph[v].isdisjoint(free(graph, S, D)):
                D.add(v)
                return True
        return False
    
    while perform_a(): ...
    while perform_b(): ...
    while perform_c(): ...

def recursion(graph: Graph, S: set, D: set):
    S = S.copy()
    D = D.copy()

    def try_A():
        for v in candidates(graph, S, D):
            if len(graph[v].intersection(free(graph, S, D))) >= 3:
                return (
                    run(graph, S.union({v}), D),
                    run(graph, S, D.union({v}))
                )
            
            for u in graph[v].intersection(available(graph, S, D)):
                if graph[u].intersection(free(graph, S, D)).isdisjoint(graph[v]):
                    return (
                        run(graph, S.union({v}), D),
                        run(graph, S, D.union({v}))
                    )

    def try_B():
        for v in candidates(graph, S, D):
            if len(graph[v].intersection(free(graph, S, D))) == 1:
                w = list(graph[v].intersection(free(graph, S, D)))[0]

                U = graph[w].intersection(available(graph, S, D)).difference(graph[v].union({v}))

                return (
                    run(graph, S, D.union({v})),
                    run(graph, S.union({v, w}), D),
                    run(graph, S.union({v}), D.union({w}).union(U)),
                )

    def try_C():
        for v in candidates(graph, S, D):
            if len(graph[v].intersection(free(graph, S, D))) == 1:
                w = list(graph[v].intersection(free(graph, S, D)))

                if (w[1] not in available(graph, S, D) and w[0] in available(graph, S, D)):
                    w[0], w[1] = w[1], w[0]
                
                if (not is_promise(graph, S, D, w[1]) and is_promise(graph, S, D, w[0])):
                    w[0], w[1] = w[1], w[0]

                U = [graph[w[i]].intersection(available(graph, S, D)).difference(graph[v].union({v}))
                     for i in [0, 1]]

                if (w[1] in graph[w[0]] and w[1] in available(graph, S, D) and w[0] in D):
                    return (
                        run(graph, S, D.union({v})),
                        run(graph, S.union({v, w[0]}), D),
                        run(graph, S.union({v}), D.union({w[0]}).union(U[0])),
                    )
                elif (w[1] in graph[w[0]] and w[1] in available(graph, S, D) and w[0] in available(graph, S, D)):
                    return (
                        run(graph, S, D.union({v})),
                        run(graph, S.union({v, w[0]}), D),
                        run(graph, S.union({v, w[1]}), D.union({w[0]})),
                        run(graph, S.union({v}), D.union({w[0], w[1]}).union(U[0]).union(U[1])),
                    )
                else:
                    return (
                        run(graph, S, D.union({v})),
                        run(graph, S.union({v, w[0]}), D),
                        run(graph, S.union({v, w[1]}), D.union({w[0]})),
                        run(graph, S.union({v}), D.union({w[0], w[1]}).union(U[0])),
                        run(graph, S.union({v}), D.union({w[0], w[1]}).union(U[1])),
                    )


    result = try_A()

    if result is None:
        result = try_B()
    
    if result is None:
        result = try_C()
    
    return result


def run(graph: Graph, S: set, D: set):
    S = S.copy()
    D = D.copy()

    if is_cds(graph, S):
        return S

    if not is_correct(graph, S, D):
        return None
    
    reduction(graph, S, D)
    answers = recursion(graph, S, D)

    if answers is None:
        return None

    result = None

    for answ in answers:
        if (answ is not None) and (result is None or (len(answ) < len(result))):
            result = answ
    
    return result

def find_cds(graph: Graph):
    answers = []

    for i1 in V(graph):
        for i2 in range(i1 + 1, len(graph)):
            answers.append(run(graph, {i1, i2}, set()))

    result = None

    for answ in answers:
        if (answ is not None) and (result is None or (len(answ) < len(result))):
            result = answ
    
    return result
