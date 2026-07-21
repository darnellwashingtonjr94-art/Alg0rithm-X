import numpy as np
from scipy.optimize import minimize
from typing import Callable, Dict, List, Tuple

class HybridVQESolver:
    """
    Variational Quantum Eigensolver (VQE) hybrid classical-quantum optimization engine.
    Iteratively adjusts parameter vectors theta to minimize Hamiltonian energy expectation values.
    """
    def __init__(self, num_parameters: int, energy_evaluator_fn: Callable[[np.ndarray], float]):
        self.num_parameters = num_parameters
        self.evaluator = energy_evaluator_fn
        self.history: List[float] = []

    def _cost_function(self, theta: np.ndarray) -> float:
        """Evaluates ground state energy expectation value for parameter set theta."""
        energy = self.evaluator(theta)
        self.history.append(energy)
        return energy

    def solve(self, initial_theta: Optional[np.ndarray] = None, max_iterations: int = 100) -> Dict[str, Union[float, np.ndarray, int]]:
        """
        Executes the optimization routine using COBYLA (Constrained Optimization By Linear Approximation).
        """
        if initial_theta is None:
            initial_theta = np.random.uniform(0, 2 * np.pi, self.num_parameters)

        result = minimize(
            fun=self._cost_function,
            x0=initial_theta,
            method='COBYLA',
            options={'maxiter': max_iterations, 'disp': False}
        )

        return {
            "optimal_energy": float(result.fun),
            "optimal_parameters": result.x,
            "iterations": result.nfev,
            "convergence_history": self.history
        }
