import matplotlib.pyplot as plt

# Datos de Merge Sort
merge_sort_n = [1000, 10000, 100000, 1000000]
merge_sort_tiempo = [0.000238, 0.002341, 0.017152, 0.17814]

# Datos de Insertion Sort
insertion_sort_n = [1000, 10000, 100000, 1000000]
insertion_sort_tiempo = [0.000231, 0.020229, 1.98443, 206.668]

# Graficar datos de Merge Sort
plt.plot(merge_sort_n, merge_sort_tiempo, marker='o', label='Merge Sort')

# Graficar datos de Insertion Sort
plt.plot(insertion_sort_n, insertion_sort_tiempo, marker='o', label='Insertion Sort')

# Configurar el gráfico
plt.title('Tiempo de ejecución de Merge Sort vs Insertion Sort en C++')
plt.xlabel('Tamaño del arreglo (n)')
plt.ylabel('Tiempo de ejecución (segundos)')
plt.xscale('log')  # Escala logarítmica en el eje x para mejor visualización
plt.yscale('log')  # Escala logarítmica en el eje y para mejor visualización
plt.grid(True)
plt.legend()

# Mostrar gráfico
plt.show()
