import multiprocessing
import time
from typing import Callable, Any, Dict

def _sandboxed_worker(target_func: Callable, args: tuple, return_dict: dict):
    """Isolated worker process to execute untrusted/generated code."""
    try:
        start_time = time.perf_counter()
        result = target_func(*args)
        execution_time = time.perf_counter() - start_time
        
        return_dict['result'] = result
        return_dict['time_ms'] = execution_time * 1000
        return_dict['status'] = 'success'
    except Exception as e:
        return_dict['error'] = str(e)
        return_dict['status'] = 'failed'

class AlgorithmEvaluator:
    """
    Sandboxed algorithmic execution testing framework. Prevents infinite loops 
    and memory leaks caused by mutated AST generation.
    """
    def __init__(self, timeout_seconds: float = 2.0):
        self.timeout = timeout_seconds

    def evaluate(self, generated_func: Callable, *args) -> Dict[str, Any]:
        """
        Executes the generated function in a separate process with a strict timeout limit.
        """
        manager = multiprocessing.Manager()
        return_dict = manager.dict()
        
        process = multiprocessing.Process(
            target=_sandboxed_worker, 
            args=(generated_func, args, return_dict)
        )
        
        process.start()
        process.join(self.timeout)

        if process.is_alive():
            # Terminate if the generated algorithm enters an infinite loop
            process.terminate()
            process.join()
            return {
                "status": "timeout",
                "error": f"Execution exceeded {self.timeout}s limit.",
                "time_ms": self.timeout * 1000
            }

        return dict(return_dict)
