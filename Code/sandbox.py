import networkx as nx
from coloring_algorithms import random_sequential, random_sequential_with_interchange
from coloring_algorithms import largest_first, largest_first_with_interchange
from coloring_algorithms import smallest_last, smallest_last_with_interchange
from coloring_algorithms import d_satur, d_satur_with_interchange
from wrapper import wrapper

G = nx.erdos_renyi_graph(1000, 0.5)

# nx.draw(G, with_labels=True)
# plt.show()

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

for function in function_list:
    coloring, number, time = wrapper(function, G)
