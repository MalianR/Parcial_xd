import networkx as nx

def matriz_incidencia(g, node_names):
    # Obtener nombres de nodos y pesos de las aristas
    nodes = list(g.nodes())
    edges_with_weights = nx.get_edge_attributes(g, 'weight')

    # Crear matriz de incidencia
    matriz_incidencia = []

    # Obtener las aristas ordenadas
    sorted_edges = sorted(edges_with_weights.keys())

    # Primero creamos la fila de encabezado con los nombres de los nodos
    fila_nodos = [''] + [node_names[node] for node in nodes]
    matriz_incidencia.append(fila_nodos)

    # Luego iteramos sobre las aristas
    for node in nodes:
        # Creamos una fila nueva para cada nodo
        fila = [node_names[node]]

        # Llenamos la fila con los pesos de las aristas que conectan el nodo actual con otros nodos
        for target_node in nodes:
            # Si hay una arista entre el nodo actual y el nodo de destino,
            # agregamos el peso de la arista o dejamos un espacio en blanco si no hay conexión
            weight = edges_with_weights.get((node, target_node), '')

            # Verificamos si la arista está en las conexiones del nodo actual
            if (node, target_node) in sorted_edges:
                # Si la arista está presente, agregamos el peso correspondiente
                fila.append(weight)
            else:
                # Si la arista no está presente, dejamos un espacio en blanco
                fila.append('')

        # Agregamos la fila completa a la matriz de incidencia
        matriz_incidencia.append(fila)

    return matriz_incidencia


def matriz_adyacencia(g):
    # La matriz de adyacencia se obtiene directamente de NetworkX
    matriz_adyacencia = nx.adjacency_matrix(g).toarray()
    return matriz_adyacencia


def longest_path_in_dag(g, start_node, end_node):
    try:
        longest_path = nx.dag_longest_path(g)
        if start_node in longest_path and end_node in longest_path:
            start_index = longest_path.index(start_node)
            end_index = longest_path.index(end_node)
            if start_index < end_index:
                longest_path = longest_path[start_index:end_index+1]
            else:
                longest_path = longest_path[end_index:start_index+1][::-1]
            return longest_path
        else:
            print("Los nodos de inicio y fin no están en el camino más largo.")
            return None
    except nx.NetworkXNotImplemented:
        print("El grafo no es un grafo dirigido acíclico (DAG).")
        return None