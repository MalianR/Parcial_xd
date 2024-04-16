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
from netgraph import EditableGraph

class MplCanvas(FigureCanvas):
    def __init__(self, parent=None, width=500, height=400, dpi=100):
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        self.ax = self.fig.add_subplot(111)
        super(MplCanvas, self).__init__(self.fig)
        self.setParent(parent)
        self.graph = None

        self.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.setFocus()

    def keyPressEvent(self, event):
        key = event.key()
        modifiers = event.modifiers() # Obtiene los modificadores del evento de tecla
        print("Pressed key:", key, "Modifiers:", modifiers) # Print additional info

        if modifiers & QtCore.Qt.ShiftModifier:
            if key == QtCore.Qt.Key_Insert: # Detectar Shift + Insert
                self.add_node_dialog()
                print("sads")
            elif key == QtCore.Qt.Key_Minus: # Detectar Shift + Minus
                self.delete_selected()
                print("sads")
            elif key == QtCore.Qt.Key_At: # Detectar Shift + At (@)
                self.reverse_edges()
                print("sads")
        else:
            super().keyPressEvent(event)
            #print("sads")

        print("End of keyPressEvent") # Debug print


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

        self.canvas = MplCanvas(self, width=5, height=4, dpi=100)
        self.toolbar = NavigationToolbar2QT(self.canvas, self)

        widget = QtWidgets.QWidget()
        self.setCentralWidget(widget)

        self.layout = QtWidgets.QVBoxLayout(widget)
        self.layout.addWidget(self.toolbar)
        self.layout.addWidget(self.canvas)

        self.setup_graph()

    def setup_graph(self):
        g = nx.DiGraph()
        self.edges_list = [(1, 2, {'weight': 1}), (1, 4, {'weight': 1.1}), (2, 5, {'weight': 0.5}),
                      (4, 5, {'weight': 1.3}), (2, 3, {'weight': 0.8})]
        g.add_edges_from(self.edges_list)

        node_color = {1: 'tab:red', 2: 'tab:blue', 3: 'tab:red', 4: 'tab:blue', 5: 'tab:red'}

        pos = nx.spring_layout(g) # Genera posiciones de nodos automáticamente
        original_pos = pos.copy()

        edge_color = {}
        for ii, (source, target) in enumerate(g.edges):
            edge_color[(source, target)] = 'tab:gray' if ii % 2 else 'tab:orange'

        def dijkstra(g, start, end):
            shortest_path = nx.shortest_path(g, source=start, target=end)
            return shortest_path

        def aplicar_dijkstra():
            start_end, ok = QtWidgets.QInputDialog.getText(self, "Dijkstra", "Ingrese dos números separados por un espacio para representar el nodo de inicio y el nodo de fin:")
            if ok and start_end:
                start_node, end_node = map(int, start_end.split())

                shortest_path = dijkstra(g, start_node, end_node)

                path_edges = list(zip(shortest_path, shortest_path[1:]))
                for edge in g.edges():
                    if edge in path_edges or edge[::-1] in path_edges:
                        edge_color[edge] = 'tab:green'
                    else:
                        edge_color[edge] = 'tab:gray'

                pos = original_pos.copy()

                self.canvas.ax.clear()

                self.canvas.graph = EditableGraph(g, node_positions=pos, node_color=node_color, node_size=5, edge_labels=True, node_labels=True,
                                                 edge_layout_kwargs=dict(k=0.025), node_label_fontdict=dict(size=20), edge_width=2, 
                                                 annotation_fontdict=dict(color='blue', fontsize=15), edge_label_fontdict=dict(fontweight='bold'),
                                                 arrows=True, ax=self.canvas.ax, edge_color=edge_color)

                self.canvas.ax.set_position([0.05, 0.05, 0.75, 0.9])
                self.canvas.ax.axis('off')
                self.canvas.draw()

        def guardar_edges_list():
            edges_list = list(g.edges(data=True))
            with open('edge_list.json', 'w') as f:
                json.dump(edges_list, f, indent=2)
            print("Lista de aristas guardada en edge_list.json")

        self.canvas.graph = EditableGraph(g, node_positions=pos, node_color=node_color, node_size=5, edge_labels=True, node_labels=True,
                                          edge_layout_kwargs=dict(k=0.025), node_label_fontdict=dict(size=20), edge_width=2,
                                          annotation_fontdict=dict(color='blue', fontsize=15), edge_label_fontdict=dict(fontweight='bold'),
                                          arrows=True, ax=self.canvas.ax)

        self.canvas.ax.set_position([0.05, 0.05, 0.75, 0.9])
        self.canvas.ax.axis('off')

        self.aplicar_dijkstra_button = QtWidgets.QPushButton('Aplicar Dijkstra', self)
        self.aplicar_dijkstra_button.clicked.connect(aplicar_dijkstra)
        self.layout.addWidget(self.aplicar_dijkstra_button)

        self.guardar_button = QtWidgets.QPushButton('Guardar Edges List', self)
        self.guardar_button.clicked.connect(guardar_edges_list)
        self.layout.addWidget(self.guardar_button)

def main():
    app = QtWidgets.QApplication(sys.argv)
    w = MainWindow()
    w.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
