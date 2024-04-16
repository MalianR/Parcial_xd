import tkinter as tk
import matplotlib.pyplot as plt
import networkx as nx
from netgraph import EditableGraph
import numpy as np
import random

# Función para generar una lista de aristas aleatoria que cumpla con los requisitos de Kruskal
def generate_random_edges(n_nodes, density=0.5, weight_range=(1, 10)):
    edges = []
    for i in range(n_nodes):
        for j in range(i+1, n_nodes):
            if random.random() < density:
                weight = random.randint(*weight_range)
                edges.append((i+1, j+1, {'weight': weight}))
    return edges

# Función para obtener un árbol de expansión mínima utilizando el algoritmo de Kruskal
def kruskal_minimum_spanning_tree(edges):
    g = nx.Graph()
    g.add_edges_from(edges)
    mst = nx.minimum_spanning_tree(g, algorithm='kruskal')
    return sorted(mst.edges(data=True))

# Función para visualizar el grafo
def visualize_graph(g, tour_path=None):
    # Limpia la figura anterior
    plt.clf()
    
    # Crea la figura y los ejes para el gráfico
    fig, ax = plt.subplots(figsize=(6, 6))

    # Grafica el grafo editable con sus atributos y posiciones definidos
    plot_instance = EditableGraph(g, ax=ax)

    # Si se proporciona un camino, pinta las aristas del camino de rojo
    if tour_path:
        nx.draw_networkx_edges(g, pos=nx.spring_layout(g), edgelist=tour_path, edge_color='red', ax=ax)

    # Muestra el gráfico
    plt.show()

# Función para mostrar el resultado en la GUI
def show_result(original_graph, result_graph):
    plt.subplot(1, 2, 1)
    plt.title("Grafo Original")
    nx.draw(original_graph, with_labels=True, font_weight='bold')
    
    plt.subplot(1, 2, 2)
    plt.title("Árbol de Expansión Mínima (Kruskal)")
    nx.draw(result_graph, with_labels=True, font_weight='bold')
    
    plt.show()

# Función para manejar el clic en el botón de Kruskal
def on_button_click():
    # Genera una lista de aristas aleatorias
    edges_list = generate_random_edges(n_nodes=5, density=0.6, weight_range=(1, 10))
    
    # Crea el grafo original
    original_graph = nx.Graph()
    original_graph.add_edges_from(edges_list)
    
    # Obtiene el árbol de expansión mínima utilizando Kruskal
    mst_edges = kruskal_minimum_spanning_tree(edges_list)
    
    # Crea el grafo del árbol de expansión mínima
    result_graph = nx.Graph()
    result_graph.add_edges_from(mst_edges)
    
    # Muestra el resultado
    show_result(original_graph, result_graph)

# Crea la ventana de Tkinter
root = tk.Tk()
root.geometry("800x400")  # Establece el tamaño de la ventana principal

# Crea el botón para Kruskal
btn_kruskal = tk.Button(root, text="Kruskal", command=on_button_click)

# Coloca el botón en la ventana
btn_kruskal.pack()

# Muestra la ventana de la GUI
root.mainloop()
