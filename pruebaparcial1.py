import matplotlib.pyplot as plt
import networkx as nx
from ._interactive_variants import EditableGraph

g = nx.house_x_graph()

edge_color = dict()
for ii, (source, target) in enumerate(g.edges):
    edge_color[(source, target)] = 'tab:gray' if ii%2 else 'tab:orange'

node_color = dict()
for node in g.nodes:
    node_color[node] = 'tab:red' if node%2 else 'tab:blue'

annotations = {
    4 : 'This is the representation of a node.',
    (0, 1) : dict(s='This is not a node.', color='red')
}

fig, ax = plt.subplots(figsize=(4, 4))

plot_instance = EditableGraph(
    g, node_color=node_color, node_size=5,
    node_labels=True, node_label_offset=0.1, node_label_fontdict=dict(size=20),
    edge_color=edge_color, edge_width=2,
    annotations=annotations, annotation_fontdict = dict(color='blue', fontsize=15),
    arrows=True, ax=ax)

def transform_edges(edges_dict):
    transformed_edges = []
    for edge, text_obj in edges_dict.items():
        # Obtener el texto del objeto Text
        text = text_obj.get_text()
        # Verificar si el texto está vacío
        if text == '':
            # Asignar un valor predeterminado al peso o simplemente omitir la conversión
            weight = 0.0 # Valor predeterminado
        else:
            # Convertir el texto a float si no está vacío
            weight = float(text)
        # Crear una tupla con los dos primeros elementos de la clave del diccionario y un diccionario con el peso
        transformed_edge = (edge[0], edge[1], {'weight': weight})
        transformed_edges.append(transformed_edge)
    return transformed_edges


plt.draw() # Redibuja la figura

# Crea la figura y los ejes para el gráfico con un tamaño más grande
fig = plt.figure(figsize=(12, 8)) # Ajusta el tamaño de la figura según tus necesidades
gs = gridspec.GridSpec(100, 100, figure=fig)
ax = fig.add_subplot(gs[0, 0])

# Ajusta el tamaño del área de visualización del grafo y elimina las fronteras
ax.set_position([0.08, 0.20, 0.75, 0.9]) # ajusta la posición del área del grafo
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

# Agrega un botón para guardar el grafo
ax_save_graph = plt.axes([0.85, 0.075, 0.1, 0.04])
btn_save_graph = plt.Button(ax_save_graph, 'Guardar Grafo')
btn_save_graph.on_clicked(save_graph)

# Agrega un botón para cargar el grafo
ax_load_graph = plt.axes([0.85, 0.85, 0.1, 0.04])
btn_load_graph = plt.Button(ax_load_graph, 'Cargar Grafo')
btn_load_graph.on_clicked(load_graph)

plt.show()
