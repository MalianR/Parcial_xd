import plotly.graph_objects as go
import networkx as nx

g = nx.house_x_graph()

# Calcular las posiciones de los nodos usando el algoritmo spring_layout
pos = nx.spring_layout(g)

node_color = ['red' if node % 2 else 'blue' for node in g.nodes]  # Usar colores válidos aceptados por Plotly

edge_color = 'gray'  # Usar un color válido aceptado por Plotly

edge_annotations = [
    (0, 1, {'text': 'This is not a node.', 'font': {'color': 'red'}})
]

node_annotations = [
    (4, {'text': 'This is the representation of a node.', 'font': {'color': 'blue', 'size': 15}})
]

edge_x = []
edge_y = []

for edge in g.edges():
    x0, y0 = pos[edge[0]]  # Acceder a las posiciones calculadas
    x1, y1 = pos[edge[1]]
    edge_x.extend([x0, x1, None])
    edge_y.extend([y0, y1, None])

edge_trace = go.Scatter(
    x=edge_x,
    y=edge_y,
    line=dict(width=2, color=edge_color),  # Usar un solo color para todos los bordes
    hoverinfo='none',
    mode='lines'
)

node_x = [pos[node][0] for node in g.nodes()]  # Extraer las coordenadas x de las posiciones calculadas
node_y = [pos[node][1] for node in g.nodes()]  # Extraer las coordenadas y de las posiciones calculadas

node_trace = go.Scatter(
    x=node_x,
    y=node_y,
    mode='markers',
    hoverinfo='text',
    marker=dict(size=20, color=node_color),  # Usar colores válidos aceptados por Plotly
    text=[f'Node {node}' for node in g.nodes]
)

fig = go.Figure(data=[edge_trace, node_trace])

for source, target, annotation in edge_annotations:
    fig.add_annotation(
        x=(pos[source][0] + pos[target][0]) / 2,
        y=(pos[source][1] + pos[target][1]) / 2,
        text=annotation['text'],
        showarrow=False,
        font=annotation['font']
    )

for node, annotation in node_annotations:
    fig.add_annotation(
        x=pos[node][0],
        y=pos[node][1],
        text=annotation['text'],
        showarrow=False,
        font=annotation['font']
    )

fig.show()
