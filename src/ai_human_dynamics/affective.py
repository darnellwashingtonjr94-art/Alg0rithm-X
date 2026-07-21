import numpy as np
import time

class AffectiveEngine:
    def __init__(self, baseline_stress: float = 0.1, decay_rate: float = 0.05):
        self.stress_level = baseline_stress
        self.baseline = baseline_stress
        self.decay_rate = decay_rate
        self.last_update = time.time()
        
    def _apply_homeostatic_decay(self, delta_time: float):
        """Pulls the system back to baseline using a simple exponential decay model."""
        if self.stress_level > self.baseline:
            self.stress_level -= self.decay_rate * (self.stress_level - self.baseline) * delta_time
            self.stress_level = max(self.baseline, self.stress_level)

    def update_state(self, stimulus_vector: list) -> dict:
        """
        Processes incoming perceptual vectors to update the affective state.
        stimulus_vector: List of floats [-1.0, 1.0] representing valence/arousal.
        """
        current_time = time.time()
        dt = current_time - self.last_update
        self._apply_homeostatic_decay(dt)
        
        # Calculate volatility based on L2 norm of the stimulus
        volatility = np.linalg.norm(stimulus_vector)
        
        # Non-linear stress spike (logistic growth curve stub)
        stress_spike = 1 / (1 + np.exp(-10 * (volatility - 0.5)))
        self.stress_level = min(1.0, self.stress_level + (stress_spike * 0.1))
        
        self.last_update = current_time
        
        return {
            "timestamp": current_time,
            "current_stress": round(self.stress_level, 4),
            "homeostatic_delta": round(self.stress_level - self.baseline, 4)
        }
