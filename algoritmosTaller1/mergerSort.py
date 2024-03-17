import time
import random

def merge_sort(arr):
    start_time = time.time()
    
    if len(arr) > 1:
        mid = len(arr) // 2
        L = arr[:mid]
        R = arr[mid:]

        merge_sort(L)
        merge_sort(R)

        i = j = k = 0

        while i < len(L) and j < len(R):
            if L[i] < R[j]:
                arr[k] = L[i]
                i += 1
            else:
                arr[k] = R[j]
                j += 1
            k += 1

        while i < len(L):
            arr[k] = L[i]
            i += 1
            k += 1

        while j < len(R):
            arr[k] = R[j]
            j += 1
            k += 1

    end_time = time.time()
    return end_time - start_time

# Solicitar al usuario la cantidad de números aleatorios en el array
num_elements = 15000

# Generar el array con números aleatorios
arr = [random.randint(0, 1000) for _ in range(num_elements)]

time_taken = merge_sort(arr)

print("Tiempo de ejecución:", time_taken, "segundos")
