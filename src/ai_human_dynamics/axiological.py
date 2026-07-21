import numpy as np
from typing import Callable, List, Dict, Tuple

class AxiologicalEngine:
    """
    Evaluates proposed actions or state changes based on Deontological (rule-based)
    and Teleological (goal-oriented) frameworks.
    """
    def __init__(self, target_state: np.ndarray):
        self.teleological_anchor = target_state
        self.deontological_filters: List[Callable[[np.ndarray], bool]] = []

    def add_hard_boundary(self, rule_function: Callable[[np.ndarray], bool]):
        """
        Adds a strict rule that an action/state must pass. 
        Example rule: lambda state: state[0] > -1.0 (Never allow parameter 0 to drop below -1.0)
        """
        self.deontological_filters.append(rule_function)

    def evaluate_proposal(self, current_state: np.ndarray, proposed_action_delta: np.ndarray) -> Tuple[bool, float]:
        """
        Tests if an action is permissible, and scores how well it aligns with the ultimate goal.
        Returns: (Is_Permissible, Teleological_Score)
        """
        projected_state = current_state + proposed_action_delta

        # 1. Deontological Pass (Hard Filters)
        for rule in self.deontological_filters:
            if not rule(projected_state):
                # Fails a hard ethical or systemic boundary
                return False, 0.0

        # 2. Teleological Pass (Distance to Goal)
        # Calculate Euclidean distance to the anchor before and after
        current_distance = np.linalg.norm(self.teleological_anchor - current_state)
        projected_distance = np.linalg.norm(self.teleological_anchor - projected_state)
        
        # Positive score means the action moves us closer to the goal
        progress_score = float(current_distance - projected_distance)

        return True, progress_score
