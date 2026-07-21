import numpy as np
from typing import Dict, List, Optional, Tuple

class TheoryOfMindNode:
    """
    Represents an N-Depth recursive belief node in a Theory of Mind framework.
    Level 0: Direct belief ('What I believe state X is')
    Level 1: 1st-order ToM ('What I believe Agent B believes about state X')
    Level N: Nested ToM ('What I believe Agent B believes Agent C believes... about state X')
    """
    def __init__(self, agent_id: str, depth: int, state_dim: int = 4):
        self.agent_id: str = agent_id
        self.depth: int = depth
        self.state_dim: int = state_dim
        
        # Mean belief vector and covariance matrix representing uncertainty
        self.belief_mean: np.ndarray = np.zeros(state_dim)
        self.belief_covariance: np.ndarray = np.eye(state_dim)
        self.nested_perspectives: Dict[str, 'TheoryOfMindNode'] = {}

    def add_nested_perspective(self, target_agent_id: str) -> 'TheoryOfMindNode':
        """Constructs an (N+1) depth belief projection targeting another agent."""
        if self.depth <= 0:
            raise ValueError("Cannot extend perspective beyond depth 0 limit.")
            
        child_node = TheoryOfMindNode(
            agent_id=target_agent_id,
            depth=self.depth - 1,
            state_dim=self.state_dim
        )
        self.nested_perspectives[target_agent_id] = child_node
        return child_node

    def update_belief_bayes(self, observation: np.ndarray, observation_noise: np.ndarray):
        """
        Performs a Bayesian Kalman update on the belief state vector.
        """
        obs_dim = observation.shape[0]
        H = np.eye(obs_dim, self.state_dim)  # Measurement matrix
        
        # Innovation covariance
        S = H @ self.belief_covariance @ H.T + observation_noise
        # Kalman Gain
        K = self.belief_covariance @ H.T @ np.linalg.inv(S)
        
        # State update
        y = observation - (H @ self.belief_mean)
        self.belief_mean = self.belief_mean + (K @ y)
        self.belief_covariance = (np.eye(self.state_dim) - (K @ H)) @ self.belief_covariance

    def compute_jensen_shannon_divergence(self, other_node: 'TheoryOfMindNode') -> float:
        """
        Calculates the divergence between this belief state and a target belief state.
        Serves as a metric for cognitive dissonance or misalignment.
        """
        m = 0.5 * (self.belief_mean + other_node.belief_mean)
        p_diff = self.belief_mean - m
        q_diff = other_node.belief_mean - m
        
        # Simplified Gaussian KL divergence approximation
        kl_p = 0.5 * np.sum(p_diff ** 2)
        kl_q = 0.5 * np.sum(q_diff ** 2)
        
        return float(0.5 * kl_p + 0.5 * kl_q)
