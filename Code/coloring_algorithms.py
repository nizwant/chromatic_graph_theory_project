import networkx as nx
import random

G = nx.cycle_graph(5)
G.add_edge(1, 4)
G.add_edge(4, 2)


def greedy(G, nodes: list):
    """
    A greedy coloring algorithm for coloring the nodes of a graph G in order given by list order.
    returns coloring and number of used colors
    """

    # if nodes is empty then return 0
    if not nodes:
        return None, 0

    assert len(nodes) == len(
        G
    ), "incorrect order provided, all nodes have to be in order"
    assert len(nodes) == len(
        set(nodes)
    ), "incorrect order provided, some nodes appear more than one"

    node_colors = {}  # A dictionary to keep track of the color assigned to each node

    # Iterate over the nodes of the graph in descending order of degree
    for node in nodes:
        # Find the colors of the neighboring nodes
        neighbor_colors = set(
            node_colors.get(neighbor) for neighbor in G.neighbors(node)
        )

        # Find the first available color that is not used by any neighbor
        for color in range(1, len(G) + 1):
            if color not in neighbor_colors:
                # Assign the color to the node
                node_colors[node] = color
                break

    return node_colors, max(node_colors.values())


def random_sequential(G):
    # obtain list of nodes in graph G and shuffle it
    order = list(G.nodes())
    random.shuffle(order)

    # use greedy on it
    coloring, chromatic_number = greedy(G, order)
    return coloring, chromatic_number


def largest_first(G):
    # obtain list of nodes in graph G and sort it
    order = G.nodes()
    order = sorted(order, key=lambda x: G.degree(x), reverse=True)
    print(order)

    # use greedy on it
    coloring, chromatic_number = greedy(G, order)
    return coloring, chromatic_number


def smallest_last(G):
    pass


print(random_sequential(G))
