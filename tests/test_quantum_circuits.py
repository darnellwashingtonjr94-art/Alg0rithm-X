import unittest
import numpy as np
from src.quantum_solver.hybrid_solver import HybridVQESolver
from src.quantum_solver.cluster_bridge import HPCClusterBridge

# Moved outside the class to allow multiprocessing serialization
def mock_hamiltonian_evaluator(theta: np.ndarray) -> float:
    """A simple quadratic bowl for the VQE optimizer to solve."""
    target = np.array([np.pi, np.pi])
    return float(np.sum((theta - target) ** 2))

class TestQuantumCircuits(unittest.TestCase):

    def test_vqe_convergence(self):
        """Tests if the COBYLA optimizer successfully minimizes the mock energy."""
        # Update reference to the detached function
        solver = HybridVQESolver(num_parameters=2, energy_evaluator_fn=mock_hamiltonian_evaluator)
        
        initial_params = np.array([0.0, 0.0])
        result = solver.solve(initial_theta=initial_params, max_iterations=50)
        
        self.assertLess(result['optimal_energy'], 0.1)
        self.assertAlmostEqual(result['optimal_parameters'][0], np.pi, places=1)

    def test_cluster_bridge_sorting(self):
        """Ensures the HPC bridge returns configurations sorted by lowest energy."""
        bridge = HPCClusterBridge(max_workers=2)
        
        grid = [
            np.array([0.0, 0.0]),
            np.array([np.pi, np.pi]),  # The optimal solution
            np.array([5.0, 5.0])
        ]
        
        # Update reference to the detached function
        results = bridge.parallel_energy_evaluation(mock_hamiltonian_evaluator, grid)
        
        best_energy = results[0]['energy']
        worst_energy = results[-1]['energy']
        
        self.assertLess(best_energy, worst_energy)
        self.assertAlmostEqual(best_energy, 0.0, places=5)
        
        bridge.shutdown()
