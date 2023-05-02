import random
from time import perf_counter
import networkx as nx
import matplotlib.pyplot as plt

# test shuffle
number_of_repetitions = 30
graph_sizes = list(range(50, 3000, 50))
times = []
for i in graph_sizes:
    list_of_graphs = [
        nx.erdos_renyi_graph(i, 0.5) for _ in range(number_of_repetitions)
    ]
    start = perf_counter()
    for i in range(number_of_repetitions):
        # operation done in random.shuffle

        # maybe remove list creation out of timing
        order = list(list_of_graphs[i].nodes())
        random.shuffle(order)
    stop = perf_counter()
    time = stop - start
    times.append(time)

# plotting results
plt.plot(graph_sizes, times)
plt.plot([0, 3000], [0, times[-1]])
plt.xlabel("number of nodes")
plt.ylabel("time taken to shuffle")
plt.title("time taken to shuffle vs number of nodes")
plt.show()


# test sort
number_of_repetitions = 10
graph_sizes = list(range(50, 3000, 50))
times = []
for i in graph_sizes:
    list_of_graphs = [
        nx.erdos_renyi_graph(i, 0.5) for _ in range(number_of_repetitions)
    ]
    start = perf_counter()
    for i in range(number_of_repetitions):
        # operation done in random.shuffle
        order = list(list_of_graphs[i].nodes())
        order = sorted(order, key=lambda x: list_of_graphs[i].degree(x), reverse=True)
    stop = perf_counter()
    time = stop - start
    times.append(time)

# plotting results
plt.plot(graph_sizes, times)
plt.plot([0, 3000], [0, times[-1]])
plt.xlabel("number of nodes")
plt.ylabel("time taken to sort")
plt.title("time taken to sort vs number of nodes")
plt.show()
