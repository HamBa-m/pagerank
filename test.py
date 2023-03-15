import networkx as nx
import matplotlib.pyplot as plt

# adjacency list
adj_list = {0: [1, 2], 1: [0, 3], 2: [0, 3], 3: [1, 2]}

# create graph
G = nx.Graph(adj_list)

# draw graph
nx.draw(G, with_labels=True)
plt.show()
