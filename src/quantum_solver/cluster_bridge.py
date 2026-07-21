import concurrent.futures
import numpy as np
import logging
from typing import Callable, List, Dict

logger = logging.getLogger(__name__)

class HPCClusterBridge:
    """
    Distributes classical-quantum hybrid workloads (like VQE parameter sweeps) 
    across local cores or HPC cluster nodes.
    """
    def __init__(self, max_workers: int = None):
        # Defaults to the number of processors on the machine
        self.max_workers = max_workers
        self.executor = concurrent.futures.ProcessPoolExecutor(max_workers=self.max_workers)
        logger.info(f"Cluster Bridge initialized with up to {self.executor._max_workers} parallel workers.")

    def parallel_energy_evaluation(self, 
                                   evaluator_fn: Callable[[np.ndarray], float], 
                                   parameter_grid: List[np.ndarray]) -> List[Dict[str, float]]:
        """
        Splits a grid of VQE parameter configurations across multiple workers
        to find the optimal starting parameters concurrently.
        """
        results = []
        
        # Submit all evaluation tasks to the process pool
        future_to_params = {
            self.executor.submit(evaluator_fn, params): params 
            for params in parameter_grid
        }
        
        for future in concurrent.futures.as_completed(future_to_params):
            params = future_to_params[future]
            try:
                energy = future.result()
                results.append({"params": params, "energy": energy})
            except Exception as exc:
                logger.error(f"Cluster node generated an exception: {exc}")
                
        # Sort results by lowest energy (optimal ground state)
        results.sort(key=lambda x: x['energy'])
        return results

    def shutdown(self):
        """Safely cleans up the distributed computing pool."""
        self.executor.shutdown(wait=True)
        logger.info("Cluster Bridge offline.")
