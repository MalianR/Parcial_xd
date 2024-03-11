import numpy as np
import matplotlib.pyplot as plt
import networkx as nx
import netgraph as ng

def update_graph():
    global I
    plt.clf()  # Borra la figura actual
    I = ng.InteractiveGraph(G,
                            node_positions=pos,
                            node_labels=True,
                            node_label_bbox=dict(fc="lightgreen", ec="black", boxstyle="square", lw=3),
                            node_size=12)
    plt.ion()
    plt.show()


def add_new_graph(event):
    # Esta función se activará cuando se presione una tecla
    if event.key == 'a':
        # Agrega nodos con atributos al grafo existente
        G.add_node(6, nombre='Tarea 6', duracion=3, costo=15, prerrequisitos=[], postrequisitos=[])
        G.add_node(7, nombre='Tarea 7', duracion=6, costo=25, prerrequisitos=[6], postrequisitos=[])
        
        # Agrega aristas al grafo existente según necesites
        G.add_edge(6, 7)
        
        # Actualiza y redibuja el gráfico
        update_graph()
# Crear un grafo dirigido vacío
G = nx.DiGraph()

# Añadir nodos con atributos
G.add_node(1, nombre='Tarea 1', duracion=5, costo=20, prerrequisitos=[], postrequisitos=[2,4])
G.add_node(2, nombre='Tarea 2', duracion=4, costo=20, prerrequisitos=[1], postrequisitos=[3,5])
G.add_node(3, nombre='Tarea 3', duracion=10, costo=50, prerrequisitos=[2], postrequisitos=[5])
G.add_node(4, nombre='Tarea 4', duracion=4, costo=20, prerrequisitos=[1], postrequisitos=[5])
G.add_node(5, nombre='Tarea 5', duracion=5, costo=30, prerrequisitos=[2, 3, 4], postrequisitos=[])

# Añadir aristas al grafo según la imagen
G.add_edge(1, 2)
G.add_edge(1, 4)
G.add_edge(2, 5)
G.add_edge(4, 5)
G.add_edge(2, 3)

# Definir posiciones iniciales de los nodos
pos = {1: np.array([1, 1]), 2: np.array([1, 2]), 3: np.array([1, 3]), 4: np.array([1, 4]), 5: np.array([1, 5])}

# Verificar y ajustar posiciones para evitar divisiones por cero
for node, position in pos.items():
    if np.linalg.norm(position) == 0:
        pos[node] = np.array([0, 0]) # Ajustar posición a un vector no nulo

# Crear un gráfico interactivo con netgraph
I = ng.InteractiveGraph(G,
                              node_positions=pos,
                              node_labels=True,
                              node_label_bbox=dict(fc="lightgreen", ec="black", boxstyle="square", lw=3),
                              node_size=12)

# Registrar la función para activar cuando se presione una tecla
plt.gcf().canvas.mpl_connect('key_press_event', add_new_graph)

# Mostrar el gráfico interactivo
plt.ion()
plt.show()
plt.pause(10000) # Pausa para mantener la ventana abierta

