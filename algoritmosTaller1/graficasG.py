import pandas as pd

# Datos de Merge Sort en diferentes lenguajes
merge_sort_data = {
    'Lenguaje': ['Java', 'C++', 'Python'],
    '1000': [9.274e-4, 0.00802206, 0.000238],
    '10000': [0.0040012, 0.0559375, 0.002341],
    '100000': [0.0304107, 0.26166868, 0.017152],
    '1000000': [0.1387797, 38.616118, 0.17814]
}

# Datos de Insertion Sort en diferentes lenguajes
insertion_sort_data = {
    'Lenguaje': ['Java', 'C++', 'Python'],
    '1000': [0.0018475, 0.0392644, 0.000231],
    '10000': [0.0393592, 3.42444, 0.020229],
    '100000': [3.144691, 325.640305, 1.98443],
    '1000000': [330.9564333, None, 206.668]
}

# Crear DataFrames para Merge Sort e Insertion Sort
merge_sort_df = pd.DataFrame(merge_sort_data)
insertion_sort_df = pd.DataFrame(insertion_sort_data)

# Mostrar los DataFrames
print("Tiempo de ejecucion de Merge Sort:")
print(merge_sort_df)
print("\nTiempo de ejecucion de Insertion Sort:")
print(insertion_sort_df)
