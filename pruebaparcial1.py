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


edges = plot_instance.edge_label_artists 
edges_l = transform_edges(edges)
print(edges)
print(edges_l)

plt.show()