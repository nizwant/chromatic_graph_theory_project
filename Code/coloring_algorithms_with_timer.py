from collections import defaultdict
from networkx import Graph
from time import perf_counter
import random
from coloring_algorithms import try_interchanging_colors  # this function doesn't change


def _greedy(G: Graph, order: list, timing_dict, color_with_interchange=False):
    """
    A greedy coloring algorithm for coloring the nodes of a graph G in order given by list order.
    returns coloring and number of used colors
    """

    # if order is empty then return 0
    if not order:
        return None, 0

    assert len(order) == len(
        G
    ), "incorrect order provided, all nodes have to be in order"
    assert len(order) == len(
        set(order)
    ), "incorrect order provided, some nodes appear more than one"

    node_colors = {}  # A dictionary to keep track of the color assigned to each node
    max_color = 1  # additional variable to help with interchange of colors

    timing_list = []
    # Iterate over the nodes of the graph in given order
    for i, node in enumerate(order):
        # time it
        timing_list.append([i, perf_counter(), False, None])

        # color it
        node_colors, max_color = color_node(
            G, node, node_colors, max_color, color_with_interchange, i, timing_list
        )

    timing_dict["coloring"] = timing_list

    return node_colors, max(node_colors.values()), timing_dict


def color_node(
    G: Graph, node, node_colors, max_color, color_with_interchange, i, timing_list
):
    # Find the colors of the neighbors of node
    neighbor_colors = set(node_colors.get(neighbor) for neighbor in G.neighbors(node))
    # Find the first available color that is not used by any neighbor
    for color in range(1, len(G) + 1):
        if color not in neighbor_colors:
            if color_with_interchange and color > max_color:  # if new color is needed
                # time it
                timing_list.append([i, perf_counter(), True, None])
                old_color = color

                # try to interchange colors
                color = try_interchanging_colors(G, node, node_colors, color)

                # time it again
                timing_list.append([i, perf_counter(), True, old_color != color])

            # Assign the color to the node
            node_colors[node] = color
            return node_colors, max(color, max_color)


def random_sequential(G: Graph, timing_dict, color_with_interchange=False):
    # obtain list of nodes in graph G and shuffle it
    order = list(G.nodes())
    random.shuffle(order)

    # use greedy on it
    coloring, number_of_colors_used, timing_dict = _greedy(
        G, order, timing_dict, color_with_interchange
    )
    return coloring, number_of_colors_used, timing_dict


def random_sequential_with_interchange(G: Graph, timing_dict):
    return random_sequential(G, timing_dict, color_with_interchange=True)


def largest_first(G, timing_dict, color_with_interchange=False):
    # obtain list of nodes in graph G and sort it
    order = G.nodes()
    order = sorted(order, key=lambda x: G.degree(x), reverse=True)

    # use greedy on it
    coloring, number_of_colors_used, timing_dict = _greedy(
        G, order, timing_dict, color_with_interchange
    )
    return coloring, number_of_colors_used, timing_dict


def largest_first_with_interchange(G: Graph, timing_dict):
    return largest_first(G, timing_dict, color_with_interchange=True)


def smallest_last(G: Graph, timing_dict, color_with_interchange=False):
    degrees_vertices = defaultdict(set)
    min_degree = float("inf")

    # Iterate over all vertices in the graph in order to create degrees_vertices
    # dictionary with key:value pairs degree:{nodes_that_have_this_degree}
    for v in G:
        min_degree = min(min_degree, G.degree(v))
        degrees_vertices[G.degree(v)].add(v)

    H = G.copy()
    order = []

    while degrees_vertices:  # Loop until all vertices have been removed
        while min_degree not in degrees_vertices:
            min_degree += 1

        # Remove a vertex from set with the current minimum degree and delate set if empty
        min_degree_vertex = degrees_vertices[min_degree].pop()
        if len(degrees_vertices[min_degree]) == 0:
            degrees_vertices.pop(min_degree)

        # Update the degrees of the neighbors of the removed vertex (decrease degree by 1)
        # Transfer vertex from set 'degree' to 'degree - 1' to reflect the removal of its neighbor
        for neighbor in H.neighbors(min_degree_vertex):
            degree = H.degree(neighbor)
            degrees_vertices[degree].remove(neighbor)
            if len(degrees_vertices[degree]) == 0:
                degrees_vertices.pop(degree)
            degrees_vertices[degree - 1].add(neighbor)

        H.remove_node(min_degree_vertex)  # Remove the vertex from the graph
        order.append(min_degree_vertex)  # Add the removed vertex to the order list
        min_degree += -1

    coloring, number_of_colors_used, timing_dict = _greedy(
        G, order[::-1], timing_dict, color_with_interchange
    )  # greedy on reverse order
    return coloring, number_of_colors_used, timing_dict


def smallest_last_with_interchange(G: Graph, timing_dict):
    return smallest_last(G, timing_dict, color_with_interchange=True)


def d_satur(G: Graph, timing_dict, color_with_interchange=False):
    n = len(G)
    satur = {i: 0 for i in range(n)}  # We will be dropping colored nodes
    node_colors = {}  # A dictionary to keep track of the color assigned to each node
    max_color = 1

    timing_list = []
    for i in range(n):
        # time it
        timing_list.append([i, perf_counter(), False, None])

        nodes = [
            node
            for node, saturation in satur.items()
            if saturation == max(satur.values())
        ]
        # Looking all max saturation nodes
        degrees = {node: G.degree(node) for node in nodes}
        # Dict with all max saturation nodes and their degrees
        node = max(degrees, key=degrees.get)
        # Get node with max degree and color it
        node_colors, max_color = color_node(
            G, node, node_colors, max_color, color_with_interchange, i, timing_list
        )
        # Remove colored node from satur dict
        del satur[node]
        # Update saturation of uncolored neighbors of node
        for neighbor in G.neighbors(node):
            if neighbor in satur:
                satur[neighbor] += 1

    coloring, number_of_colors_used = node_colors, max_color
    timing_dict["coloring"] = timing_list
    return coloring, number_of_colors_used, timing_dict


def d_satur_with_interchange(G: Graph, timing_dict):
    return d_satur(G, timing_dict, color_with_interchange=True)
