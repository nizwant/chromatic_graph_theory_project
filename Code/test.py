import matplotlib.pyplot as plt
import networkx as nx
from coloring_algorithms import largest_first, largest_first_with_interchange
from wrapper import wrapper

G = nx.erdos_renyi_graph(100, 0.5)
H = nx.complete_graph(10)

# nx.draw(G, with_labels=True)
# plt.show()

wrapper(largest_first, G)
wrapper(largest_first_with_interchange, G)
wrapper(largest_first, H)
wrapper(largest_first_with_interchange, H)
