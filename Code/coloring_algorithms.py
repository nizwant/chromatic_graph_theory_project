from collections import defaultdict
import networkx as nx
import matplotlib.pyplot as plt
import random


G = nx.erdos_renyi_graph(100, 0.5)

nx.draw(G, with_labels=True)
plt.show()


def greedy(G, order: list, color_with_interchange=False):
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

    # Iterate over the nodes of the graph in given order
    for node in order:
        node_colors, max_color = color_node(
            G, node, node_colors, max_color, color_with_interchange
        )

    return node_colors, max(node_colors.values())


def color_node(G, node, node_colors, max_color, color_with_interchange):
    # Find the colors of the neighbors of node
    neighbor_colors = set(node_colors.get(neighbor) for neighbor in G.neighbors(node))
    # Find the first available color that is not used by any neighbor
    for color in range(1, len(G) + 1):
        if color not in neighbor_colors:
            if color_with_interchange and color > max_color:  # if new color is needed
                color = try_interchanging_colors(G, node, node_colors, color)
            # Assign the color to the node
            node_colors[node] = color
            return node_colors, max(color, max_color)


def random_sequential(G):
    # obtain list of nodes in graph G and shuffle it
    order = list(G.nodes())
    random.shuffle(order)

    # use greedy on it
    coloring, chromatic_number = greedy(G, order)
    return coloring, chromatic_number


def random_sequential_with_interchange(G):
    # obtain list of nodes in graph G and shuffle it
    order = list(G.nodes())
    random.shuffle(order)

    # use greedy on it
    coloring, chromatic_number = greedy(G, order, color_with_interchange=True)
    return coloring, chromatic_number


def largest_first(G):
    # obtain list of nodes in graph G and sort it
    order = G.nodes()
    order = sorted(order, key=lambda x: G.degree(x), reverse=True)

    # use greedy on it
    coloring, chromatic_number = greedy(G, order)
    return coloring, chromatic_number


def largest_first_with_interchange(G):
    # obtain list of nodes in graph G and sort it
    order = G.nodes()
    order = sorted(order, key=lambda x: G.degree(x), reverse=True)

    # use greedy on it
    coloring, chromatic_number = greedy(G, order, color_with_interchange=True)
    return coloring, chromatic_number


def smallest_last(G):
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

    coloring, chromatic_number = greedy(G, order[::-1])  # greedy on reverse order
    return coloring, chromatic_number


def smallest_last_with_interchange(G):
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

    coloring, chromatic_number = greedy(
        G, order[::-1], color_with_interchange=True
    )  # greedy on reverse order
    return coloring, chromatic_number


def d_satur(G):
    order = []
    # TODO inplementacja ona tu i tu powinna byc identyczna
    # wiem że mozna to zrobic ładniej ale chce funkcje z osobnymi nazwami a nie np jako argument
    coloring, chromatic_number = greedy(G, order[::-1])
    return coloring, chromatic_number


def d_satur_with_interchange(G):
    order = []
    # TODO inplementacja
    coloring, chromatic_number = greedy(G, order[::-1], color_with_interchange=True)
    return coloring, chromatic_number


def try_interchanging_colors(G, node, node_colors, proposed_color):
    best_color = proposed_color
    colors_neighbors = defaultdict(set)

    # Iterate over all neighbors of the node in order to create colors_neighbors
    # dictionary with key:value pairs color:{nodes_that_have_this_color}
    for neighbor in G.neighbors(node):
        if neighbor in node_colors:
            colors_neighbors[node_colors[neighbor]].add(neighbor)

    valid_neighbors = []
    # select nodes that have unique color in set of neighbor
    for color, set_of_neighbors in colors_neighbors.items():
        if len(set_of_neighbors) == 1:
            valid_neighbors.append([set_of_neighbors.pop(), color])

    breaker = False
    for valid_neighbor, color in valid_neighbors:
        colors_neighbor_neighbors = set()
        for neighbor_of_valid_neighbor in G.neighbors(valid_neighbor):
            if neighbor_of_valid_neighbor in node_colors:
                colors_neighbor_neighbors.add(node_colors[neighbor_of_valid_neighbor])

        for i in range(1, proposed_color):
            if i not in colors_neighbor_neighbors:
                node_colors[valid_neighbor] = i
                best_color = color
                breaker = True
                break

        if breaker:
            break

    return best_color


print(largest_first(G))
print(largest_first_with_interchange(G))
