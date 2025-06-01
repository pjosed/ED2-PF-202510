import threading
import time
from load_ventas import cargar_ventas_desde_csv
from algorithms.sorting_algorithms import quicksort, mergesort, heapsort, radixsort

ventas = cargar_ventas_desde_csv()

def key_function(cantidad):
    return cantidad["CANTIDAD"] 

class SortingThread(threading.Thread):
    def __init__(self, name, sort_function, data, key):
        super().__init__()
        self.name = name
        self.sort_function = sort_function
        self.data = data
        self.key = key
        self.sorted_data = None
        self.execution_time = None

    def run(self):
        start = time.time()
        self.sorted_data = self.sort_function(self.data.copy(), key=self.key)
        end = time.time()
        self.execution_time = end - start
        print(f"{self.name} tardó {self.execution_time:.4f} s")
        with open(f"{self.name}_ordenado.txt", "w", encoding="utf-8") as f:
            for item in self.sorted_data:
                f.write(str(item) + "\n")

if __name__ == '__main__':
    algos = {
        "quicksort": quicksort,
        "mergesort": mergesort,
        "heapsort": heapsort,
        "radixsort": radixsort
    }

    threads = []
    for name, func in algos.items():
        thread = SortingThread(name, func, ventas, key=key_function)
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

