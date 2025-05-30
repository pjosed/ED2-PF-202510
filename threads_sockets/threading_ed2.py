import random
import threading
import time
import time
from threads_sockets.load_ventas import cargar_ventas_desde_csv
from algorithms.sorting_algorithms import quicksort, mergesort, heapsort, bubblesort

ventas = cargar_ventas_desde_csv()

class SortingThread(threading.Thread):
    def __init__(self, name, sort_function, data):
        super().__init__()
        self.name = name
        self.sort_function = sort_function
        self.data = data
        self.sorted_data = None
        self.execution_time = None

    def run(self):
        start = time.time()
        self.sorted_data = self.sort_function(self.data.copy())
        end = time.time()
        self.execution_time = end - start
        print(f"{self.name} tardó {self.execution_time:.4f} s")
        with open(f"{self.name}_ordenado.txt", "w") as f:
            f.write(str(self.sorted_data))

if __name__ == '__main__':
    algos = {
        "quicksort": quicksort,
        "mergesort": mergesort,
        "heapsort": heapsort,
        "bubblesort": bubblesort
    }

    threads = []
    for name, func in algos.items():
        thread = SortingThread(name, func, ventas)
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()


'''
class Working_Thread(threading.Thread):
    def __init__(self, name):
        threading.Thread.__init__(self)
        self.name = name
        self.id = id(self)

    def run(self):
        """
        Run the thread
        """
        worker(self.name, self.id)


def worker(name: str, instance_id: int) -> None:
    print(f'Started worker {name} - {instance_id}')
    worker_time = random.choice(range(1, 10))
    time.sleep(worker_time)
    print("the result is", instance_id*2)
    print(f'{name} - {instance_id} worker finished in '
          f'{worker_time} seconds')


if __name__ == '__main__':
    for i in range(1000):
        thread = Working_Thread(name=f'computer_{i}')
        thread.start()
    thread.join()

    '''
