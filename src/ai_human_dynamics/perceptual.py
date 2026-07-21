import numpy as np
from typing import Dict, List

class PerceptualIngest:
    """
    Ingests and normalizes raw environmental inputs into structured sensory vectors.
    Acts as the sensory gateway for the AI human dynamics model.
    """
    def __init__(self, buffer_size: int = 100):
        self.buffer_size = buffer_size
        self.sensory_history = []

    def _calculate_volatility(self) -> float:
        """
        Calculates environmental volatility based on the standard deviation 
        of recent sensory magnitudes.
        """
        if len(self.sensory_history) < 2:
            return 0.0
            
        magnitudes = [np.linalg.norm(vec) for vec in self.sensory_history]
        return float(np.std(magnitudes))

    def ingest_signal(self, raw_signal: List[float], signal_weights: List[float] = None) -> Dict[str, float]:
        """
        Takes raw multi-modal input (e.g., text sentiment, audio pitch, visual chaos)
        and normalizes it into a standardized perceptual vector.
        """
        signal_array = np.array(raw_signal)
        
        if signal_weights is not None:
            if len(signal_weights) != len(raw_signal):
                raise ValueError("Weights array must match signal array dimensions.")
            signal_array = signal_array * np.array(signal_weights)

        # L2 Normalization to keep vectors within the unit hypersphere
        norm = np.linalg.norm(signal_array)
        if norm > 0:
            normalized_signal = signal_array / norm
        else:
            normalized_signal = signal_array

        # Update rolling buffer
        self.sensory_history.append(normalized_signal)
        if len(self.sensory_history) > self.buffer_size:
            self.sensory_history.pop(0)

        # Map to cognitive dimensions
        perceptual_state = {
            "valence": float(np.mean(normalized_signal)),        # Overall positivity/negativity
            "arousal": float(norm),                              # Intensity of the stimulus
            "volatility": self._calculate_volatility()           # Unpredictability of the environment
        }
        
        return perceptual_state
