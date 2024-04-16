import time
import random

def insertion_sort(arr):
    start_time = time.time()
    
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        while j >= 0 and key < arr[j]:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key

    end_time = time.time()
    return end_time - start_time

# Solicitar al usuario la cantidad de números aleatorios en el array
num_elements = 15000

# Generar el array con números aleatorios
arr = [random.randint(0, 1000) for _ in range(num_elements)]

time_taken = insertion_sort(arr)

print("Tiempo de ejecución:", time_taken, "segundos")
