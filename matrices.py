import networkx as nx

def matriz_incidencia(g):
        # La matriz de incidencia se construye a partir de la matriz de adyacencia
        # y la lista de aristas, ya que NetworkX no proporciona una función directa
        # para obtener la matriz de incidencia.
        matriz_adyacencia = nx.adjacency_matrix(g).toarray()
        matriz_incidencia = []
        for i in range(len(matriz_adyacencia)):
            fila = []
            for j in range(len(matriz_adyacencia[i])):
                if matriz_adyacencia[i][j] == 1:
                    fila.append(1)
                else:
                    fila.append(-1)
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