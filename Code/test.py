import matplotlib.pyplot as plt
import networkx as nx
from coloring_algorithms import largest_first, largest_first_with_interchange

G = nx.erdos_renyi_graph(100, 0.5)
H = nx.complete_graph(10)

# nx.draw(G, with_labels=True)
# plt.show()


print(largest_first(G))
print(largest_first_with_interchange(G))
print(largest_first_with_interchange(H))
