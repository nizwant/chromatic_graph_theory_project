import networkx as nx
from coloring_algorithms import random_sequential, random_sequential_with_interchange
from coloring_algorithms import largest_first, largest_first_with_interchange
from coloring_algorithms import smallest_last, smallest_last_with_interchange
from coloring_algorithms import d_satur, d_satur_with_interchange


function_list = [
    random_sequential,
    random_sequential_with_interchange,
    largest_first,
    largest_first_with_interchange,
    smallest_last,
    smallest_last_with_interchange,
    d_satur,
    d_satur_with_interchange,
]

probabilities = [0.1, 0.3, 0.5, 0.7, 0.9]

for p in probabilities:
    G = nx.gnp_random_graph(1000, p, seed=2137)
    for function in function_list:
        coloring, number_of_colors_used = function(G)
        for edge in G.edges():
            assert (
                coloring[edge[0]] != coloring[edge[1]]
            ), f"{function.__name__} created invalid coloring, two adjacent nodes have the same color"
