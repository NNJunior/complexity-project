import algorithm
from algorithm import common

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

    assert common.is_cds(graph, cds)
    assert common.is_cds(graph, dummy_cds)
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

    assert common.is_cds(graph, cds)
    assert common.is_cds(graph, dummy_cds)
    assert len(cds) == len(dummy_cds)
