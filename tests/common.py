import algorithm
from algorithm import common
import tempfile
import networkx as nx
import os
import requests
import time
import pandas as pd

def get_graphs(url: str):
    with tempfile.TemporaryDirectory() as tmpdirname:
        tmp_filepath = os.path.join(tmpdirname, "graph4c.g6")
        
        response = requests.get(url)
        
        with open(tmp_filepath, "wb") as f:
            f.write(response.content)
        
        graphs = nx.read_graph6(tmp_filepath)
    
    graphs = [nx.to_dict_of_lists(g) for g in graphs]

    for g in graphs:
        for key in g:
            g[key] = set(g[key])
    
    return graphs

def _test_url(url: str):
    graphs = get_graphs(url)

    data = []

    for graph in graphs:
        if not common.is_connected(graph, common.V(graph)):
            continue

        cds_start = time.perf_counter_ns()
        cds = algorithm.find_cds(graph)
        cds_end = time.perf_counter_ns()

        dummy_start = time.perf_counter_ns()
        dummy_cds = algorithm.dummy_cds(graph)
        dummy_end = time.perf_counter_ns()

        data.append(((dummy_end - dummy_start) / 1000, (cds_end - cds_start) / 1000, graph, cds, dummy_cds))

        assert common.is_cds(graph, cds)
        assert common.is_cds(graph, dummy_cds)
        assert len(cds) == len(dummy_cds)

    name = url.removeprefix("https://users.cecs.anu.edu.au/~bdm/data/").removesuffix(".g6")

    df = pd.DataFrame(data=data, columns=["dummy_time", "fomin_time", "graph", "fomin_cds", "dummy_cds"])
    df.to_pickle(f"tests_data/{name}.pkl")

