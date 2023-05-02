from networkx import Graph
from time import perf_counter


def wrapper(coloring_func, G: Graph, report=True):
    """
    A wrapper function for coloring algorithms.
    Returns a dictionary of colors for each node and the number of used colors.
    """

    start = perf_counter()
    coloring, number_of_color_used = coloring_func(G)
    stop = perf_counter()
    time = stop - start

    if report:
        print(f"Time taken: {time:.3f}s, coloring function: {coloring_func.__name__}")
        print(f"color used: {number_of_color_used}, number of nodes: {len(G)}")
        print("")

    return coloring, number_of_color_used, time
