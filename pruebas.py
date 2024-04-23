import sys
import json
import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas, NavigationToolbar2QT
from matplotlib.figure import Figure
from PyQt5 import QtWidgets, QtCore
import networkx as nx
import tkinter as tk
from tkinter import simpledialog
from ._interactive_variants import (
    MutableGraph,
    EditableGraph,
)
import ast

from .matrices import longest_path_in_dag, matriz_adyacencia, matriz_incidencia
from PyQt5.QtWidgets import QFileDialog

class MplCanvas(FigureCanvas):
    def __init__(self, parent=None, width=500, height=400, dpi=100):
        # Inicialización del lienzo Matplotlib
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        self.ax = self.fig.add_subplot(111)
        super(MplCanvas, self).__init__(self.fig)
        self.setParent(parent)
        self.graph = None

        # Establecer la política de enfoque para manejar eventos de teclado
        self.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.setFocus()

    def keyPressEvent(self, event):
        # Manejar eventos de teclado
        key = event.key()
        modifiers = event.modifiers() # Obtiene los modificadores del evento de tecla

        # Imprimir información adicional sobre la tecla presionada y los modificadores
        print("Pressed key:", key, "Modifiers:", modifiers)

        # Verificar si se presionó Shift junto con otras teclas
        if modifiers & QtCore.Qt.ShiftModifier:
            if key == QtCore.Qt.Key_Insert: # Detectar Shift + Insert
                self.add_node_dialog()
            elif key == QtCore.Qt.Key_Minus: # Detectar Shift + Minus
                self.delete_selected()
            elif key == QtCore.Qt.Key_At: # Detectar Shift + At (@)
                self.reverse_edges()
        else:
            super().keyPressEvent(event)

    # Función para mostrar un diálogo para agregar un nodo
    # (Actualmente no implementada completamente)
    def add_node_dialog(self):
        dialog = QtWidgets.QInputDialog(self)
        dialog.setWindowTitle("Agregar Nodo")
        dialog.setLabelText("Ingrese el valor del nodo:")
        dialog.setOkButtonText("Agregar")
        dialog.setCancelButtonText("Cancelar")
        ok = dialog.exec_()
        if ok:
            node_value = dialog.textValue()
            print(f"Agregando nodo con valor: {node_value}")

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        # Crear un lienzo Matplotlib y una barra de herramientas
        self.canvas = MplCanvas(self, width=5, height=4, dpi=100)
        self.toolbar = NavigationToolbar2QT(self.canvas, self)

        # Crear un widget central y establecer el lienzo y la barra de herramientas
        widget = QtWidgets.QWidget()
        self.setCentralWidget(widget)

        # Configurar el diseño de la ventana
        self.layout = QtWidgets.QVBoxLayout(widget)
        self.layout.addWidget(self.toolbar)
        self.layout.addWidget(self.canvas)

        # Configurar el grafo inicial
        self.setup_graph()
    
    # Función para configurar el grafo inicial
    def setup_graph(self):
        # Crear un grafo dirigido utilizando NetworkX
        g = nx.DiGraph()
        
        # Definir las aristas del grafo y sus pesos
        self.edges_list = {(0, 1): 1, (0, 3): 1.1, (1, 4): 0.5,
                        (3, 4): 1.3, (1, 2):0.8, (2,4) : 9}
        
        # Agregar las aristas al grafo
        g.add_edges_from(self.edges_list)
        
        # Asignar un color predeterminado a los nodos
        node_color = {0: 'tab:blue', 1: 'tab:blue', 2: 'tab:blue', 3: 'tab:blue', 4: 'tab:blue'}
        
        # Calcular las posiciones de los nodos automáticamente
        pos = nx.spring_layout(g) 
        original_pos = pos.copy()

        # Asignar colores a las aristas
        edge_color = {}
        for ii, (source, target) in enumerate(g.edges):
            edge_color[(source, target)] = 'tab:gray' if ii % 2 else 'tab:orange'

    # Función para mostrar la matriz de adyacencia del grafo actual
        def mostrar_matriz_adyacencia():
            edges_list = transform_edges_json(self.canvas.graph.edge_label_artists)
            edges_to_add = convert_keys_to_tuples(edges_list)
            g.add_edges_from(edges_to_add)
            matriz = matriz_adyacencia(g)

            # Crear una figura y ejes para mostrar la matriz de adyacencia
            fig, axs = plt.subplots(1, 2, figsize=(10, 5))
            axs[0].axis('off') # Desactiva los ejes
            axs[0].set_title('Matriz de Adyacencia')

            # Ajusta los límites de los ejes para que coincidan con el tamaño de la matriz
            axs[0].set_xlim(0, matriz.shape[1])
            axs[0].set_ylim(0, matriz.shape[0])

            # Desactiva la cuadrícula
            plt.grid(False)

            # Ajusta la posición y el tamaño de las celdas de la tabla
            the_table = axs[0].table(cellText=matriz, loc='center', cellLoc='center')
            table_props = the_table.properties()
            table_cells = table_props.get('children')
            if table_cells:
                for cell in table_cells: 
                    cell.set_height(1/float(matriz.shape[0]))
                    cell.set_width(1/float(matriz.shape[1]))

            plt.show()

        # Función para mostrar la matriz de incidencia del grafo actual
        def mostrar_matriz_incidencia():
                # Crear una figura y ejes para mostrar la matriz de incidencia
            fig, axs = plt.subplots(1, 2, figsize=(10, 5))
            axs[1].axis('off') # Desactiva los ejes
            axs[1].set_title('Matriz de Incidencia')
        
            # Obtener nombres de nodos
            node_names = {node: str(node) for node in g.nodes()}
        
            # Crear matriz de incidencia con nombres de nodos
            matriz = matriz_incidencia(g, node_names)
        
            # Ajusta los límites de los ejes basándote en las dimensiones de la lista
            num_rows = len(matriz)
            num_cols = len(matriz[0]) if matriz else 0
            axs[1].set_xlim(0, num_cols)
            axs[1].set_ylim(0, num_rows)
        
            # Desactiva la cuadrícula
            plt.grid(False)
        
            # Ajusta la posición y el tamaño de las celdas de la tabla
            the_table = axs[1].table(cellText=matriz, loc='center', cellLoc='center')
            table_props = the_table.properties()
            table_cells = table_props.get('children')
            if table_cells:
                for cell in table_cells: 
                    cell.set_height(1/float(num_rows))
                    cell.set_width(1/float(num_cols))
        
            plt.show()

        # Función para calcular el camino más corto entre dos nodos utilizando el algoritmo de Dijkstra
        def dijkstra(g, start, end):
            shortest_path = nx.shortest_path(g, source=start, target=end)
            return shortest_path
            # Función para aplicar el algoritmo de Dijkstra al grafo
        def aplicar_dijkstra():
            # Obtener los nodos de inicio y fin del usuario
            start_end, ok = QtWidgets.QInputDialog.getText(self, "Dijkstra", "Ingrese dos números separados por un espacio para representar el nodo de inicio y el nodode fin:")
            if ok and start_end:
                # Guardar la lista de aristas actual
                guardar_edges_list()
                # Transformar y agregar las aristas al grafo
                edges_dict = transform_edges_json(self.canvas.graph.edge_label_artists)
                edges_to_add = convert_keys_to_tuples(edges_dict)
                self.edges_list = edges_to_add
                g.add_edges_from(edges_to_add)
                # Colorear los nodos de azul
                node_color = {node: 'tab:blue' for node in g.nodes()}
                # Resetear el color de las aristas a gris
                edge_color = {edge: 'tab:gray' for edge in g.edges()}
                # Obtener los nodos de inicio y fin
                start_node, end_node = map(int, start_end.split())
                # Calcular el camino más corto con el algoritmo de Dijkstra
                shortest_path = dijkstra(g, start_node, end_node)
                # Obtener las aristas del camino más corto
                path_edges = list(zip(shortest_path, shortest_path[1:]))
                # Colorear las aristas del camino más corto de verde
                for edge in g.edges():
                    if edge in path_edges or edge[::-1] in path_edges:
                        edge_color[edge] = 'tab:green'
                # Generar posiciones de nodos
                pos = nx.spring_layout(g)
                # Actualizar el lienzo con el nuevo grafo
                self.canvas.ax.clear()
                self.canvas.graph = EditableGraph(g, edges_with_weight=self.edges_list, node_positions=pos, node_color=node_color, node_size=5, edge_labels=True,node_labels=True,
                                                 edge_layout_kwargs=dict(k=0.025), node_label_fontdict=dict(size=20), edge_width=2, 
                                                 annotation_fontdict=dict(color='blue', fontsize=15), edge_label_fontdict=dict(fontweight='bold'),
                                                 arrows=True, ax=self.canvas.ax, edge_color=edge_color)
                self.canvas.ax.set_position([0.05, 0.05, 0.75, 0.9])
                self.canvas.ax.axis('off')
                self.canvas.draw()
        # Función para guardar la lista de aristas en un archivo JSON
        def guardar_edges_list():
            edges_list = transform_edges_json(self.canvas.graph.edge_label_artists)
            edges_to_add = convert_keys_to_tuples(edges_list)
            g.add_edges_from(edges_to_add)
            with open('Parcial_xd/edge_list.json', 'w') as f:
                json.dump(edges_list, f, indent=2)
            print("Lista de aristas guardada en edge_list.json")
        # Función para transformar los datos de las aristas a un formato JSON
        def transform_edges_json(datos):
            edges_list = {}
            for tupla, texto in datos.items():
                tupla_str = str(tupla)
                try:
                    peso = float(texto.get_text())
                except ValueError:
                    peso = 0
                edges_list[tupla_str] = peso
            return edges_list
        # Función para convertir las claves del diccionario de cadenas a tuplas
        def convert_keys_to_tuples(d):
            return {ast.literal_eval(k): v for k, v in d.items()}

        def ruta_critica():
            # Creamos una ventana de tkinter para solicitar los nodos de inicio y fin
            root = tk.Tk()
            root.withdraw()  # Ocultamos la ventana principal

    # Solicitamos al usuario los nodos de inicio y fin
            start_node = simpledialog.askinteger("Nodo de inicio", "Ingrese el nodo de inicio:")
            end_node = simpledialog.askinteger("Nodo de fin", "Ingrese el nodo de fin:")

    # Llamamos a la función para encontrar la ruta crítica
            critical_path = longest_path_in_dag(g, start_node, end_node)
            if critical_path:
                print("Ruta crítica entre los nodos {} y {}: {}".format(start_node, end_node, critical_path))

        def guardar_edges_list_dialogo():
            
            guardar_edges_list()
            # Transforma los datos de las aristas a un formato JSON
            edges_list = transform_edges_json(self.canvas.graph.edge_label_artists)

            # Abre el diálogo de guardado de archivos
            options = QFileDialog.Options()
            options |= QFileDialog.DontUseNativeDialog
            fileName, _ = QFileDialog.getSaveFileName(self, "Guardar Lista de Aristas", "", "Archivos JSON (*.json);;Todos los archivos (*)", options=options)

            # Si el usuario seleccionó un archivo, guarda la lista de aristas en ese archivo
            if fileName:
                with open(fileName, 'w') as f:
                    json.dump(edges_list, f, indent=2)
                print(f"Lista de aristas guardada en {fileName}")

        # Función para abrir un archivo JSON y leer sus datos
        def abrir_y_leer_json():
            options = QFileDialog.Options()
            options |= QFileDialog.ReadOnly
            fileName, _ = QFileDialog.getOpenFileName(self, "Abrir Archivo JSON", "", "Archivos JSON (*.json);;Todos los archivos (*)", options=options)
            if fileName:
                with open(fileName, 'r') as f:
                    data = json.load(f)
                print(f"Archivo JSON abierto y leído: {fileName}")
                return data
            else:
                print("No se seleccionó ningún archivo.")
                return None
        # Función para cargar los datos de un archivo JSON y actualizar el grafo en el lienzo
        def data_abierto():
            edges_dict = abrir_y_leer_json()
            edges_to_add = convert_keys_to_tuples(edges_dict)
            g.add_edges_from(edges_to_add)
            node_color = {node: 'tab:blue' for node in g.nodes()}
            edge_color = {edge: 'tab:gray' for edge in g.edges()}
            self.canvas.ax.clear()
            self.canvas.graph = EditableGraph(g, edges_with_weight=self.edges_list, node_positions=pos, node_color=node_color, node_size=5, edge_labels=True,node_labels=True,
                                             edge_layout_kwargs=dict(k=0.025), node_label_fontdict=dict(size=20), edge_width=2, 
                                             annotation_fontdict=dict(color='blue', fontsize=15), edge_label_fontdict=dict(fontweight='bold'),
                                             arrows=True, ax=self.canvas.ax, edge_color=edge_color)
            self.canvas.ax.set_position([0.05, 0.05, 0.75, 0.9])
            self.canvas.ax.axis('off')
            self.canvas.draw()
        # Crear la instancia de EditableGraph y configurar la interfaz gráfica
        self.canvas.graph = EditableGraph(g,edges_with_weight = self.edges_list, node_positions=pos, node_color=node_color, node_size=5, edge_labels=True,node_labels=True,
                                          edge_layout_kwargs=dict(k=0.025), node_label_fontdict=dict(size=20), edge_width=2,
                                          annotation_fontdict=dict(color='blue', fontsize=15), edge_label_fontdict=dict(fontweight='bold'),
                                          arrows=True, ax=self.canvas.ax)
        self.canvas.ax.set_position([0.05, 0.05, 0.75, 0.9])
        self.canvas.ax.axis('off')
        # Crear y conectar los botones de la interfaz gráfica
        self.aplicar_dijkstra_button = QtWidgets.QPushButton('Aplicar Dijkstra', self)
        self.aplicar_dijkstra_button.clicked.connect(aplicar_dijkstra)
        self.layout.addWidget(self.aplicar_dijkstra_button)
        self.mostrar_matriz_adyacencia_button = QtWidgets.QPushButton('Mostrar Matriz de Adyacencia', self)
        self.mostrar_matriz_adyacencia_button.clicked.connect(mostrar_matriz_adyacencia)
        self.layout.addWidget(self.mostrar_matriz_adyacencia_button)

        self.mostrar_matriz_incidencia_button = QtWidgets.QPushButton('Mostrar Matriz de Incidencia', self)
        self.mostrar_matriz_incidencia_button.clicked.connect(mostrar_matriz_incidencia)
        self.layout.addWidget(self.mostrar_matriz_incidencia_button)

        self.guardar_button_dialogo = QtWidgets.QPushButton('Guardar Edges List', self)
        self.guardar_button_dialogo.clicked.connect(guardar_edges_list_dialogo)
        self.layout.addWidget(self.guardar_button_dialogo)
        self.abrir_json_button = QtWidgets.QPushButton('Abrir y Leer JSON', self)
        self.abrir_json_button.clicked.connect(lambda: data_abierto())
        self.layout.addWidget(self.abrir_json_button)

        self.ruta_button_dialogo = QtWidgets.QPushButton('Ruta Critica', self)
        self.ruta_button_dialogo.clicked.connect(ruta_critica)
        self.layout.addWidget(self.ruta_button_dialogo)


# Función principal para iniciar la aplicación
def main():
    app = QtWidgets.QApplication(sys.argv)
    w = MainWindow()
    w.show()
    sys.exit(app.exec_())

# Iniciar la aplicación si este script es el programa principal
if __name__ == "__main__":
    main()
