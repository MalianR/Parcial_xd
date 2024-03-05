import networkx as nx
import matplotlib.pyplot as plt

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

# Dibujar el grafo con nodos y etiquetas personalizadas
pos = nx.spring_layout(G) # posición de los nodos
nx.draw(G, pos,
        with_labels=True,
        node_color=['orange', 'green', 'yellow', 'blue', 'red'],
        node_size=1500,
        edge_color='black',
        arrows=True,
        arrowstyle='->',
        arrowsize=10)

plt.show()
