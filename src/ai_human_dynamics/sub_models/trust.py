import math

class AsymmetricTrustModel:
    """
    Simulates human trust dynamics where confidence is built logarithmically (slowly) 
    but decays exponentially (rapidly) upon betrayal or failure.
    """
    def __init__(self, initial_trust: float = 0.5):
        # Trust bounded between 0.0 (complete distrust) and 1.0 (absolute faith)
        self.trust_level = max(0.0, min(1.0, initial_trust))
        
        # Tuning parameters for the asymmetry
        self.growth_factor = 0.02
        self.decay_factor = 0.15

    def process_interaction(self, reliability_score: float) -> float:
        """
        reliability_score: Evaluated outcome of an interaction (-1.0 to 1.0)
        """
        if reliability_score > 0:
            # Positive interaction: Logarithmic growth (diminishing returns as trust nears 1.0)
            available_growth_space = 1.0 - self.trust_level
            growth = self.growth_factor * reliability_score * available_growth_space
            self.trust_level += growth
        elif reliability_score < 0:
            # Negative interaction: Exponential decay (damage is worse when trust is high)
            damage_multiplier = 1.0 + self.trust_level
            decay = self.decay_factor * abs(reliability_score) * damage_multiplier
            self.trust_level = max(0.0, self.trust_level - decay)
            
        return self.trust_level

    def requires_verification(self) -> bool:
        """
        Threshold check: If trust drops below 0.4, the system should trigger 
        secondary verification routines.
        """
        return self.trust_level < 0.4
