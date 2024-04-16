import matplotlib.pyplot as plt

# Datos de Merge Sort
merge_sort_n = [1000, 10000, 100000, 1000000]
merge_sort_tiempo = [0.00802206, 0.0559375, 0.26166868, 38.616118]

# Datos de Insertion Sort
insertion_sort_n = [1000, 10000, 100000, 1000000]
insertion_sort_tiempo = [0.0392644, 3.42444, 325.640305, None]

# Graficar datos de Merge Sort
plt.plot(merge_sort_n, merge_sort_tiempo, marker='o', label='Merge Sort')

# Graficar datos de Insertion Sort
plt.plot(insertion_sort_n, insertion_sort_tiempo, marker='o', label='Insertion Sort')

# Configurar el gráfico
plt.title('Tiempo de ejecución de Merge Sort vs Insertion Sort en Python')
plt.xlabel('Tamaño del arreglo (n)')
plt.ylabel('Tiempo de ejecución (segundos)')
plt.xscale('log')  # Escala logarítmica en el eje x para mejor visualización
plt.yscale('log')  # Escala logarítmica en el eje y para mejor visualización
plt.grid(True)
plt.legend()

# Mostrar gráfico
plt.show()
