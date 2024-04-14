import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import networkx as nx
from netgraph import EditableGraph
import numpy as np
import tkinter as tk
from tkinter import simpledialog

# Define el grafo y sus atributos
g = nx.DiGraph()
edges_list = [(1, 2, {'weight': 1}), (1, 4, {'weight': 1.1}), (2, 5, {'weight': 0.5}),
              (4, 5, {'weight': 1.3}), (2, 3, {'weight': 0.8})]
g.add_edges_from(edges_list)

node_color = {1: 'tab:red', 2: 'tab:blue', 3: 'tab:red', 4: 'tab:blue', 5: 'tab:red'}

# Posiciones de los nodos
pos = {1: np.array([1, 1]), 2: np.array([1, 2]), 3: np.array([1, 3]), 4: np.array([1, 4]), 5: np.array([1, 5])}

# Diccionario para almacenar los colores de las aristas
edge_color = {}
for ii, (source, target) in enumerate(g.edges):
    edge_color[(source, target)] = 'tab:gray' if ii % 2 else 'tab:orange'

def dijkstra(g, start, end):
    shortest_path = nx.shortest_path(g, source=start, target=end)
    return shortest_path

def aplicar_dijkstra(event):
    global start_node, end_node
    root = tk.Tk()
    root.withdraw() # Oculta la ventana principal de tkinter
    start_end = simpledialog.askstring("Dijkstra", "Ingrese dos números separados por un espacio para representar el nodo de inicio y el nodo de fin:")
    if start_end:
        start_node, end_node = map(int, start_end.split())
        shortest_path = dijkstra(g, start_node, end_node)

        # Colorea el camino más corto de otro color
        path_edges = list(zip(shortest_path, shortest_path[1:]))
        for edge in g.edges():
            if edge in path_edges or edge[::-1] in path_edges:
                edge_color[edge] = 'tab:green'
            else:
                edge_color[edge] = 'tab:gray' # Simplemente asigna 'tab:gray' a las aristas no utilizadas

        # Elimina el gráfico actual
        ax.clear()

        # Redibuja el gráfico con los nuevos colores de las aristas
        plot_instance = EditableGraph(g, pos=pos, node_color=node_color, node_size=5, edge_labels=True, node_labels=True,
                                      edge_layout_kwargs=dict(k=0.025), node_label_fontdict=dict(size=20), edge_width=2,
                                      annotation_fontdict=dict(color='blue', fontsize=15), edge_label_fontdict=dict(fontweight='bold'),
                                      arrows=True, ax=ax, edge_color=edge_color) # Asegúrate de pasar edge_color aquí

        # Ajusta el tamaño del área de visualización del grafo y elimina las fronteras
        ax.set_position([0.05, 0.05, 0.75, 0.9]) # ajusta la posición del área del grafo
        ax.axis('off') # Elimina las fronteras del subplot

        plt.draw() # Redibuja la figura

# Crea la figura y los ejes para el gráfico con un tamaño más grande
fig = plt.figure(figsize=(12, 8)) # Ajusta el tamaño de la figura según tus necesidades
gs = gridspec.GridSpec(100, 100, figure=fig)
ax = fig.add_subplot(gs[0, 0])

# Ajusta el tamaño del área de visualización del grafo y elimina las fronteras
ax.set_position([0.05, 0.05, 0.75, 0.9]) # ajusta la posición del área del grafo
ax.axis('off') # Elimina las fronteras del subplot

# Crea el gráfico inicial
plot_instance = EditableGraph(g, pos=pos, node_color=node_color, node_size=5, edge_labels=True, node_labels=True,
                              edge_layout_kwargs=dict(k=0.025), node_label_fontdict=dict(size=20), edge_width=2,
                              annotation_fontdict=dict(color='blue', fontsize=15), edge_label_fontdict=dict(fontweight='bold'),
                              arrows=True, ax=ax)

# Agrega un botón para aplicar Dijkstra
ax_aplicar_dijkstra = plt.axes([0.85, 0.025, 0.1, 0.04])
btn_aplicar_dijkstra = plt.Button(ax_aplicar_dijkstra, 'Aplicar Dijkstra')
btn_aplicar_dijkstra.on_clicked(aplicar_dijkstra)

plt.show()
