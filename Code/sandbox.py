from matplotlib import pyplot as plt
import networkx as nx
from coloring_algorithms_with_timer import (
    random_sequential,
    random_sequential_with_interchange,
)
from coloring_algorithms_with_timer import largest_first, largest_first_with_interchange
from coloring_algorithms_with_timer import smallest_last, smallest_last_with_interchange
from coloring_algorithms_with_timer import d_satur, d_satur_with_interchange
from wrapper import wrapper

G = nx.erdos_renyi_graph(100, 0.5)

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
    coloring, number, time, coloring_dict = wrapper(function, G)
    plt.plot(
        [i[1] for i in coloring_dict["coloring"]],
        [i[0] for i in coloring_dict["coloring"]],
        label=function.__name__,
    )

plt.legend()
plt.show()
