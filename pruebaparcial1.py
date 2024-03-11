import matplotlib.pyplot as plt  
import networkx as nx 
from netgraph import EditableGraph 
import numpy as np  

# Crea un grafo dirigido
g = nx.DiGraph()

# Lista de tuplas de aristas con sus atributos (pesos)
edges_list = [
    (1, 2, {'weight': 1}),
    (1, 4, {'weight': 1.1}),
    (2, 5, {'weight': 0.5}),
    (4, 5, {'weight': 1.3}),
    (2, 3, {'weight': 0.8})
]

# Añade las aristas al grafo
g.add_edges_from(edges_list)

# Crea un diccionario para almacenar los pesos de las aristas
edges_weight = {}
for i in range(len(edges_list)):
    edges_weight[(edges_list[i][0], edges_list[i][1])] = edges_list[i][2]['weight']

# Diccionario para almacenar los colores de las aristas
edge_color = dict()
for ii, (source, target) in enumerate(g.edges):
    edge_color[(source, target)] = 'tab:gray' if ii % 2 else 'tab:orange'

# Diccionario para almacenar los colores de los nodos y define los atributos de los nodos
node_color = dict()
g.add_nodes_from([
     (1, {"nombre": 'Tarea 1', "duracion": 4, "costo": 20, "prerrequisitos": [1], "postrequisitos": [3, 5]}),
     (2, {"nombre": 'Tarea 2', "duracion": 10, "costo": 50, "prerrequisitos": [2], "postrequisitos": [5]}),
     (3, {"nombre": 'Tarea 3', "duracion": 15, "costo": 20, "prerrequisitos": [1], "postrequisitos": [5]}),
     (4, {"nombre": 'Tarea 4', "duracion": 15, "costo": 20, "prerrequisitos": [1], "postrequisitos": [5]}),
     (5, {"nombre": 'Tarea 5', "duracion": 15, "costo": 20, "prerrequisitos": [1], "postrequisitos": [5]}),
])

# Define los colores de los nodos
for node in g.nodes:
    node_color[node] = 'tab:red' if node % 2 else 'tab:blue'

# Crea la figura y los ejes para el gráfico
fig, ax = plt.subplots(figsize=(10, 10))

# Posiciones de los nodos
pos = {1: np.array([1, 1]), 2: np.array([1, 2]), 3: np.array([1, 3]), 4: np.array([1, 4]), 5: np.array([1, 5])}

# Grafica el grafo editable con sus atributos y posiciones definidos
plot_instance = EditableGraph(g, pos=pos,
    node_color=node_color, node_size=5, edge_labels=edges_weight,
    node_labels=True, edge_layout_kwargs=dict(k=0.025),
    node_label_fontdict=dict(size=20),
    edge_color=edge_color, edge_width=2,
    annotation_fontdict=dict(color='blue', fontsize=15), edge_label_fontdict=dict(fontweight='bold'),
    arrows=True, ax=ax)
    
# Muestra el gráfico
plt.show()
