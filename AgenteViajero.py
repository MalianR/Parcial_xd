import networkx as nx
import matplotlib.pyplot as plt
import numpy as np

# Creamos un grafo completo aleatorio
G = nx.complete_graph(5)
for (u, v, w) in G.edges(data=True):
    w['weight'] = np.random.randint(1, 10)

# Imprimimos las aristas con sus pesos
print("Datos originales del grafo:")
for (u, v, w) in G.edges(data=True):
    print(f"Arista: ({u}, {v}), Peso: {w['weight']}")

# Visualizamos el grafo original
plt.figure(figsize=(6, 6))
pos = nx.spring_layout(G)
nx.draw(G, pos, with_labels=True, node_size=700, node_color='lightblue', font_size=12, font_weight='bold')
labels = nx.get_edge_attributes(G, 'weight')
nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)
plt.title("Grafo original")
plt.show()

# Algoritmo del Agente Viajero
def traveling_salesman(graph):
    shortest_path = nx.approximation.traveling_salesman_problem(graph)
    return shortest_path

# Obtenemos la solución del Agente Viajero
tsp_solution = traveling_salesman(G)

# Mostramos la solución
plt.figure(figsize=(6, 6))
nx.draw(G, pos, with_labels=True, node_size=700, node_color='lightblue', font_size=12, font_weight='bold')
nx.draw_networkx_edges(G, pos, edgelist=tsp_solution + [tsp_solution[0]], width=2, edge_color='red')
labels = nx.get_edge_attributes(G, 'weight')
nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)
plt.title("Solución del Agente Viajero")
plt.show()

print("Camino del Agente Viajero:", tsp_solution)
