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
from itertools import cycle


from .matrices import longest_path_in_dag, matriz_adyacencia, matriz_incidencia
from PyQt5.QtWidgets import QFileDialog, QApplication, QWidget, QLabel, QVBoxLayout

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

        self.current_color = 'tab:blue'
        self.arc = 'circular'
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
        self.edges_list = {(0, 1): 0.1, (0, 3): 1.1, (1, 4): 0.5,
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
            g = nx.DiGraph()
            g.add_edges_from(edges_to_add)
            adjacency_matrix = nx.to_pandas_adjacency(g)
            
            plt.figure(figsize=(8, 8))  # Tamaño del gráfico
            
            # Dibuja la matriz de adyacencia
            plt.imshow(adjacency_matrix, cmap='viridis', interpolation='none')
            plt.title('Matriz de Adyacencia')
            plt.colorbar()  # Añade una barra de color para la escala
            
            # Ajusta los ticks del eje x e y
            plt.xticks(range(len(adjacency_matrix.columns)), adjacency_matrix.columns)
            plt.yticks(range(len(adjacency_matrix.index)), adjacency_matrix.index)
            
            # Rotación de los ticks del eje x
            plt.xticks(rotation=90)
            
            plt.show()

        # Función para mostrar la matriz de incidencia del grafo actual
        def mostrar_matriz_incidencia():
            edges_list = transform_edges_json(self.canvas.graph.edge_label_artists)
            edges_to_add = convert_keys_to_tuples(edges_list)
            g = nx.DiGraph()
            g.add_edges_from(edges_to_add)

            # Nodos y aristas
            nodes = list(g.nodes)
            edges = list(g.edges)
            # Crear diccionario para mapear nombres de nodos a índices
            node_indices = {node: i for i, node in enumerate(nodes)}

            # Crear la matriz de incidencia
            num_nodes = len(nodes)
            num_edges = len(edges)
            incidence_matrix = np.zeros((num_nodes, num_edges))

            for i, edge in enumerate(edges):
                u, v = edge
                incidence_matrix[node_indices[u], i] = 1
                incidence_matrix[node_indices[v], i] = 1

            print(incidence_matrix)
            # Plotear la matriz de incidencia
            plt.figure(figsize=(10, 6))
            plt.imshow(incidence_matrix, cmap='binary', aspect='auto')

            # Configurar etiquetas de los ejes
            plt.xticks(np.arange(num_edges), [f'{edges_to_add[edge]}' for edge in edges])
            plt.yticks(np.arange(num_nodes), nodes)

            # Configurar los límites de los ejes
            plt.xlim(-0.5, num_edges - 0.5)
            plt.ylim(num_nodes - 0.5, -0.5)

            # Añadir etiquetas
            plt.xlabel('Etiquetas de aristas (nodos)')
            plt.ylabel('Etiquetas de nodos')

            # Añadir barra de color
            plt.colorbar(label='Incidencia')

            plt.title('Matriz de Incidencia')

            plt.show()

        # Función para calcular el camino más corto entre dos nodos utilizando el algoritmo de Dijkstra

        def bidirectional_dijk(G, source, target, edges):
            def weight(u, v, d):
                return edges.get((u, v), None) if (u, v) in edges else edges.get((v, u), None)

            return nx.bidirectional_dijkstra(G, source, target, weight=weight)

        def aplicar_dijkstra():
            try:
                # Obtener los nodos de inicio y fin del usuario
                start_end, ok = QtWidgets.QInputDialog.getText(self, "Dijkstra", "Ingrese dos números separados por un espacio para representar el nodo de inicio y el nodode fin:")
                if ok and start_end:
                    # Guardar la lista de aristas actual
                    # Transformar y agregar las aristas al grafo
                    edges_dict = transform_edges_json(self.canvas.graph.edge_label_artists)
                    edges_to_add = convert_keys_to_tuples(edges_dict)
                    self.edges_list = edges_to_add
                    g = nx.DiGraph()
                    g.add_edges_from(edges_to_add)
                    print("edges_to_add", self.edges_list)

                    # Colorear los nodos de azul
                    color = self.current_color
                    node_color = {node: color for node in g.nodes()}
                    # Resetear el color de las aristas a gris
                    edge_color = {edge: 'tab:gray' for edge in g.edges()}
                    # Obtener los nodos de inicio y fin
                    start_node, end_node = map(int, start_end.split())
                    # Calcular el camino más corto con el algoritmo de Dijkstra
                    shortest_path = bidirectional_dijk(g, start_node, end_node, edges_to_add)
                    shortest_path = shortest_path[1]
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
                                                    arrows=True, ax=self.canvas.ax, edge_color=edge_color,
                                                    node_layout = self.arc)
                    self.canvas.ax.set_position([0.05, 0.05, 0.75, 0.9])
                    self.canvas.ax.axis('off')
                    self.canvas.draw()
            except nx.NetworkXNoPath as e:
                # Si no hay un camino entre los nodos de inicio y fin, mostrar un mensaje al usuario
                QtWidgets.QMessageBox.information(self, "Sin camino", "No hay un camino entre los nodos de inicio y fin.")

        
        # Función para guardar la lista de aristas en un archivo JSON
        def guardar_edges_list():
            edges_list = transform_edges_json(self.canvas.graph.edge_label_artists)
            edges_to_add = convert_keys_to_tuples(edges_list)
            g = nx.DiGraph()
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
            edges_dict = transform_edges_json(self.canvas.graph.edge_label_artists)
            edges_to_add = convert_keys_to_tuples(edges_dict)
            self.edges_list = edges_to_add
            g = nx.DiGraph()
            g.add_edges_from(edges_to_add)
            critical_path = longest_path_in_dag(g, start_node, end_node)
            path_edges = list(zip(critical_path, critical_path[1:]))
            if critical_path:
                # Colorear los nodos de azul
                #color = next(color_gen)
                color = self.current_color
                node_color = {node: color for node in g.nodes()}
                # Resetear el color de las aristas a gris
                edge_color = {edge: 'tab:gray' for edge in g.edges()}

                # Colorear las aristas de la ruta crítica de rojo
                for edge in path_edges:
                    edge_color[edge] = 'tab:red'

                # Generar posiciones de nodos
                pos = nx.spring_layout(g)

                # Actualizar el lienzo con el nuevo grafo
                self.canvas.ax.clear()
                self.canvas.graph = EditableGraph(g, edges_with_weight=self.edges_list, node_positions=pos, node_color=node_color, node_size=5, edge_labels=True,node_labels=True,
                                                edge_layout_kwargs=dict(k=0.025), node_label_fontdict=dict(size=20), edge_width=2, 
                                                annotation_fontdict=dict(color='blue', fontsize=15), edge_label_fontdict=dict(fontweight='bold'),
                                                arrows=True, ax=self.canvas.ax, edge_color=edge_color,
                                                node_layout = self.arc)
                self.canvas.ax.set_position([0.05, 0.05, 0.75, 0.9])
                self.canvas.ax.axis('off')
                self.canvas.draw()

            

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
            g = nx.DiGraph()
            g.add_edges_from(edges_to_add)
            color = self.current_color
            node_color = {node: color for node in g.nodes()}
            edge_color = {edge: 'tab:gray' for edge in g.edges()}
            self.canvas.ax.clear()
            self.canvas.graph = EditableGraph(g, edges_with_weight=self.edges_list, node_positions=pos, node_color=node_color, node_size=5, edge_labels=True,node_labels=True,
                                             edge_layout_kwargs=dict(k=0.025), node_label_fontdict=dict(size=20), edge_width=2, 
                                             annotation_fontdict=dict(color='blue', fontsize=15), edge_label_fontdict=dict(fontweight='bold'),
                                             arrows=True, ax=self.canvas.ax, edge_color=edge_color,
                                             node_layout = self.arc)
            self.canvas.ax.set_position([0.05, 0.05, 0.75, 0.9])
            self.canvas.ax.axis('off')
            self.canvas.draw()


        def mostrar_instrucciones():
            # Crear la ventana principal
            ventana = tk.Tk()
            ventana.title("Instrucciones")
            ventana.geometry("500x300+100+100") # Ajusta el tamaño y la posición de la ventana

            # Definir el texto de las instrucciones
            texto_instrucciones = """
            Presionar insertar - añadirá un nuevo nodo al grafo.
            Hacer doble clic en dos nodos sucesivamente creará una arista entre ellos.
            Presionar borrar o - eliminará los nodos y aristas seleccionados.
            Presionar @ invertirá la dirección de las aristas seleccionadas.
            Para crear o editar una etiqueta de nodo o arista, selecciona el nodo (o arista), presiona la tecla Enter y escribe.
            Para crear o editar una anotación, selecciona el nodo (o arista), presiona Alt + Enter y escribe.
            Termina cualquiera de estas acciones presionando Enter o Alt + Enter una segunda vez.
            """

            # Crear un widget Label para mostrar el texto de las instrucciones
            etiqueta_instrucciones = tk.Label(ventana, text=texto_instrucciones, justify='left', wraplength=450)
            etiqueta_instrucciones.pack(padx=10, pady=10)

            # Iniciar el bucle principal de la ventana
            ventana.mainloop()

        def update_color(color): 
            self.current_color = color
            #self.current_color = next(self.color_gen)
            g = update_g()
            edge_color = {edge: 'tab:gray' for edge in g.edges()}
            node_color = {node: color for node in g.nodes()}
            pos = nx.spring_layout(g)
                    # Actualizar el lienzo con el nuevo grafo
            self.canvas.ax.clear()
            self.canvas.graph = EditableGraph(g, edges_with_weight=self.edges_list, node_positions=pos, node_color=node_color, node_size=5, edge_labels=True,node_labels=True,
                                                    edge_layout_kwargs=dict(k=0.025), node_label_fontdict=dict(size=20), edge_width=2, 
                                                    annotation_fontdict=dict(color='blue', fontsize=15), edge_label_fontdict=dict(fontweight='bold'),
                                                    arrows=True, ax=self.canvas.ax, edge_color=edge_color,
                                                    node_layout = self.arc)
            self.canvas.ax.set_position([0.05, 0.05, 0.75, 0.9])
            self.canvas.ax.axis('off')
            self.canvas.draw()

        

        def update_arc(arc): 
            self.arc = arc
            #self.current_color = next(self.color_gen)
            g = update_g()
            color = self.current_color
            edge_color = {edge: 'tab:gray' for edge in g.edges()}
            node_color = {node: color for node in g.nodes()}
            pos = nx.spring_layout(g)
                    # Actualizar el lienzo con el nuevo grafo
            self.canvas.ax.clear()
            self.canvas.graph = EditableGraph(g, edges_with_weight=self.edges_list, node_positions=pos, node_color=node_color, node_size=5, edge_labels=True,node_labels=True,
                                                    edge_layout_kwargs=dict(k=0.025), node_label_fontdict=dict(size=20), edge_width=2, 
                                                    annotation_fontdict=dict(color='blue', fontsize=15), edge_label_fontdict=dict(fontweight='bold'),
                                                    arrows=True, ax=self.canvas.ax, edge_color=edge_color,
                                                    node_layout = self.arc)
            self.canvas.ax.set_position([0.05, 0.05, 0.75, 0.9])
            self.canvas.ax.axis('off')
            self.canvas.draw()
        




        def update_g():
            edges_dict = transform_edges_json(self.canvas.graph.edge_label_artists)
            edges_to_add = convert_keys_to_tuples(edges_dict)
            self.edges_list = edges_to_add
            g = nx.DiGraph()
            g.add_edges_from(edges_to_add)
            return g



        def boton_de_prueba():
            print("Hi")


            #print(nx.incidence_matrix(g, g.node))
            

        # Crear la instancia de EditableGraph y configurar la interfaz gráfica
        self.canvas.graph = EditableGraph(g,edges_with_weight = self.edges_list, node_positions=pos, node_color=node_color, node_size=5, edge_labels=True,node_labels=True,
                                          edge_layout_kwargs=dict(k=0.025), node_label_fontdict=dict(size=20), edge_width=2,
                                          annotation_fontdict=dict(color='blue', fontsize=15), edge_label_fontdict=dict(fontweight='bold'),
                                          arrows=True, ax=self.canvas.ax,
                                          node_layout = self.arc)
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




        # Crear un layout horizontal para contener los botones adicionales
        additional_buttons_layout = QtWidgets.QHBoxLayout()

        # Crear y añadir los botones adicionales al layout
        button1 = QtWidgets.QPushButton('Instrucciones', self)
        button1.clicked.connect(lambda: mostrar_instrucciones())

        button2 = QtWidgets.QPushButton('Rojo', self)
        button2.clicked.connect(lambda: update_color('tab:red'))

        button3 = QtWidgets.QPushButton('Verde', self)
        button3.clicked.connect(lambda: update_color('tab:green'))

        button4 = QtWidgets.QPushButton('Cyan', self)
        button4.clicked.connect(lambda: update_color('tab:cyan'))

        additional_buttons_layout.addWidget(button1)
        additional_buttons_layout.addWidget(button2)
        additional_buttons_layout.addWidget(button3)
        additional_buttons_layout.addWidget(button4)

        self.layout.addLayout(additional_buttons_layout)

        # Eliminar y liberar recursos del botón original
        if hasattr(self, 'boton_button_dialogo'):
            self.layout.removeWidget(self.boton_button_dialogo)
            self.boton_button_dialogo.deleteLater()

# Función principal para iniciar la aplicación
        additional_buttons2_layout = QtWidgets.QHBoxLayout()

        # Crear y añadir los botones adicionales al layout
        buttona1 = QtWidgets.QPushButton('Radial', self)
        buttona1.clicked.connect(lambda: update_arc('radial'))

        buttona2 = QtWidgets.QPushButton('Spring', self)
        buttona2.clicked.connect(lambda: update_arc('spring'))

        buttona3 = QtWidgets.QPushButton('Dot', self)
        buttona3.clicked.connect(lambda: update_arc('dot'))

        buttona4 = QtWidgets.QPushButton('Circular', self)
        buttona4.clicked.connect(lambda: update_arc('circular'))

        additional_buttons2_layout.addWidget(buttona1)
        additional_buttons2_layout.addWidget(buttona2)
        additional_buttons2_layout.addWidget(buttona3)
        additional_buttons2_layout.addWidget(buttona4)

        self.layout.addLayout(additional_buttons2_layout)
# Función principal para iniciar la aplicación
def main():
    app = QtWidgets.QApplication(sys.argv)
    w = MainWindow()
    w.show()
    sys.exit(app.exec_())

# Iniciar la aplicación si este script es el programa principal
if __name__ == "__main__":
    main()
