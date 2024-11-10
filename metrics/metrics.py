import time
import psutil
import threading

start_time = 0  # Variável global para armazenar o tempo de início
memory_start = 0  # Variável global para armazenar o uso de memória no início
max_memory_used = 0
stop_thread = False  # Controle para parar a thread

def _get_memory_usage():
    process = psutil.Process()
    memory_info = process.memory_info()
    return memory_info.rss / (1024 ** 2)  # Converte para MB


def _print_metrics_periodically():
    global stop_thread
    while not stop_thread:
        time.sleep(0.5)
        if not stop_thread:
            _print_metrics()

def _print_metrics():
    global start_time, memory_start, max_memory_used
    
    elapsed_time = time.time() - start_time 
    current_memory = _get_memory_usage() - memory_start 

    if current_memory > max_memory_used:
        max_memory_used = current_memory

    print(f"\nTempo desde o início: {elapsed_time:.2f} Segundos")
    print(f"Máximo de Memória Utilizada: {max_memory_used:.2f} MB")

def start_metrics():
    global start_time, memory_start, stop_thread
    start_time = time.time()
    memory_start = _get_memory_usage()  
    stop_thread = False

    threading.Thread(target=_print_metrics_periodically, daemon=True).start()

def stop_metrics():
    global start_time, memory_start, stop_thread
    stop_thread = True
    _print_metrics()
