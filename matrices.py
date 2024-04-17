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