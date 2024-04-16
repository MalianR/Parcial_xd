import matplotlib.pyplot as plt

# Datos de Merge Sort
merge_sort_n = [1000, 10000, 100000, 1000000]
merge_sort_tiempo = [9.274e-4, 0.0040012, 0.0304107, 0.1387797]

# Datos de Insertion Sort
insertion_sort_n = [1000, 10000, 100000, 1000000]
insertion_sort_tiempo = [0.0018475, 0.0393592, 3.144691, 330.9564333]

# Graficar datos de Merge Sort
plt.plot(merge_sort_n, merge_sort_tiempo, marker='o', label='Merge Sort')

# Graficar datos de Insertion Sort
plt.plot(insertion_sort_n, insertion_sort_tiempo, marker='o', label='Insertion Sort')

# Configurar el gráfico
plt.title('Tiempo de ejecución de Merge Sort vs Insertion Sort en Java')
plt.xlabel('Tamaño del arreglo (n)')
plt.ylabel('Tiempo de ejecución (segundos)')
plt.xscale('log')  # Escala logarítmica en el eje x para mejor visualización
plt.yscale('log')  # Escala logarítmica en el eje y para mejor visualización
plt.grid(True)
plt.legend()

# Mostrar gráfico
plt.show()
