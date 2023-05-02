from collections import defaultdict
from matplotlib import pyplot as plt
import networkx as nx
from coloring_algorithms import random_sequential, random_sequential_with_interchange
from coloring_algorithms import largest_first, largest_first_with_interchange
from coloring_algorithms import smallest_last, smallest_last_with_interchange
from coloring_algorithms import d_satur, d_satur_with_interchange
from wrapper import wrapper
import random
from time import perf_counter


def random_sequential_with_timer(G, timing_dict, color_with_interchange=False):
    # obtain list of nodes in graph G and shuffle it
    order = list(G.nodes())
    random.shuffle(order)
    timing_dict["preparation_end"] = perf_counter()

    # use greedy on it
    coloring, number_of_colors_used, timing_dict = _greedy_with_time(
        G, order, timing_dict, color_with_interchange
    )
    return coloring, number_of_colors_used, timing_dict


def _greedy_with_time(G, order: list, timing_dict, color_with_interchange=False):
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
        node_colors, max_color = color_node_with_time(
            G, node, node_colors, max_color, color_with_interchange, timing_list, i
        )
        timing_list.append([i, perf_counter(), False, None])

    timing_dict["coloring"] = timing_list
    return node_colors, max(node_colors.values()), timing_dict


def color_node_with_time(
    G, node, node_colors, max_color, color_with_interchange, timing_list, i
):
    # Find the colors of the neighbors of node
    neighbor_colors = set(node_colors.get(neighbor) for neighbor in G.neighbors(node))
    # Find the first available color that is not used by any neighbor
    for color in range(1, len(G) + 1):
        if color not in neighbor_colors:
            if color_with_interchange and color > max_color:  # if new color is needed
                # try to interchange colors
                timing_list.append([i, perf_counter(), True, None])
                tmp = color
                color = try_interchanging_colors(G, node, node_colors, color)
                timing_list.append([i, perf_counter(), True, tmp != color])
            # Assign the color to the node
            node_colors[node] = color
            return node_colors, max(color, max_color)


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
            if i not in colors_neighbor_neighbors and i != color:
                node_colors[valid_neighbor] = i
                best_color = color
                breaker = True
                break

        if breaker:
            break

    return best_color


for i in range(1):
    G = nx.erdos_renyi_graph(2000, 0.5, seed=42)

    timing_dict = defaultdict(float)
    timing_dict["start"] = perf_counter()
    coloring, number = smallest_last(G, color_with_interchange=True)
    timing_dict["end"] = perf_counter()
    print(timing_dict["end"] - timing_dict["start"])


# # kolorowanie
# fig, ax = plt.subplots()
# ax.plot(
#     [i[1] for i in timing_dict["coloring"]],
#     [i[0] for i in timing_dict["coloring"]],
#     linewidth=3,
# )
# # for i in timing_dict["coloring"]:
# #     if i[2] and i[3]:
# #         (green_x,) = ax.plot(i[1], i[0], "Xg", markersize=6)
# #     if i[2] and i[3] is not None and not i[3]:
# #         (red_dot,) = ax.plot(i[1], i[0], "or", markersize=6)
# plt.xlabel("time [s]")
# plt.ylabel("node (its like progress)")
# # ax.legend([green_x, red_dot], ["interchange", "new color needed"])
# plt.show()


# number = 10_000
# start = perf_counter()
# counter = 0
# counter1 = 0
# counter2 = 0
# counter3 = 0
# counter4 = 0
# time = []
# for i in range(number):
#     counter = counter + 1
#     counter1 = counter1 + 1
#     counter2 = counter2 + 1
#     counter3 = counter3 + 1
#     counter4 = counter4 + 1
#     time.append([perf_counter(), None, True])
# end = perf_counter()
# tmp1 = end - start
# print(end - start)

# start = perf_counter()
# counter = 0
# counter1 = 0
# counter2 = 0
# counter3 = 0
# counter4 = 0
# for i in range(number):
#     counter = counter + 1
#     counter1 = counter1 + 1
#     counter2 = counter2 + 1
#     counter3 = counter3 + 1
#     counter4 = counter4 + 1
# end = perf_counter()
# tmp2 = end - start
# print(end - start)
# print(tmp1 - tmp2)
