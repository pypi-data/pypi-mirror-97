import multiprocessing
from concurrent.futures  import ProcessPoolExecutor

def get_cpu_count():
    return multiprocessing.cpu_count()

def parallel_run(func, *iterables, max_workers):

    with ProcessPoolExecutor(max_workers) as executor:
        result = executor.map(func, *iterables)

    return [i for i in result]