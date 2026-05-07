import algorithm
from algorithm import base

def test_simple_1():
    graph = {
        0: {3},
        1: {2, 3},
        2: {1},
        3: {1, 0},
    }
    
    cds = algorithm.find_cds(graph)

    assert cds == {1, 3}

def test_simple_2():
    graph = {
        0: {1, 2, 3, 4},
        1: {0},
        2: {0},
        3: {0},
        4: {0}
    }

    cds = algorithm.find_cds(graph)
    dummy_cds = algorithm.dummy_cds(graph)

    assert base.is_cds(graph, cds)
    assert base.is_cds(graph, dummy_cds)
    assert len(cds) == len(dummy_cds)

def test_simple_3():
    graph = {
        0: {1, 4},
        1: {0, 2},
        2: {1, 3},
        3: {2, 4},
        4: {3, 0}
    }

    cds = algorithm.find_cds(graph)
    dummy_cds = algorithm.dummy_cds(graph)

    assert base.is_cds(graph, cds)
    assert base.is_cds(graph, dummy_cds)
    assert len(cds) == len(dummy_cds)

def test_4_vertices():
    pass

def test_5_vertices():
    pass

def test_6_vertices():
    pass

def test_7_vertices():
    pass

def test_8_vertices():
    pass

