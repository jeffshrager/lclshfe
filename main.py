import time
import multiprocessing
from rich.progress import Progress


def do_kmeans(param1):
    time.sleep(5)    
    return param1

def call_do_kmeans(params):
    return do_kmeans(*params)

if __name__ == "__main__":
    algo_params = []
    results = []
    for x in range(100):
        algo_params.append([x])

    with Progress() as progress:
        task_id = progress.add_task("[cyan]Working...", total=len(algo_params))
        with multiprocessing.Pool(processes=5) as pool:
            for result in pool.imap(call_do_kmeans, algo_params):
                print(result)
                results.append(result)            
                progress.advance(task_id)

    print(results)