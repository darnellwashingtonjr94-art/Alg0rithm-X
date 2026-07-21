import unittest
import time
import numpy as np
from src.ai_human_dynamics.affective import AffectiveEngine
from src.ai_human_dynamics.sub_models.happiness import HedonicAdaptationModel
from src.ai_human_dynamics.sub_models.trust import AsymmetricTrustModel
from src.ai_human_dynamics.cognitive import TheoryOfMindNode

class TestDynamicsMath(unittest.TestCase):
    
    def test_affective_bound_saturation(self):
        """Ensures stress levels cannot exceed 1.0 or drop below baseline."""
        engine = AffectiveEngine(baseline_stress=0.2)
        # Apply massive, chaotic stimulus
        extreme_stimulus = [5.0, 5.0, 5.0]
        state = engine.update_state(extreme_stimulus)
        
        self.assertLessEqual(state['current_stress'], 1.0)
        self.assertGreaterEqual(state['current_stress'], 0.2)

    def test_hedonic_adaptation_decay(self):
        """Validates that happiness decays back toward the set point."""
        model = HedonicAdaptationModel(set_point=0.5, adaptation_rate=1.0)
        model.apply_stimulus(valence=1.0, intensity=1.0) # Massive positive spike
        
        peak_happiness = model.current_happiness
        self.assertGreater(peak_happiness, 0.5)
        
        # Manually advance the internal clock by 1 second
        model.last_update_time -= 1.0 
        decayed_happiness = model.step_adaptation()
        
        self.assertLess(decayed_happiness, peak_happiness)
        self.assertGreaterEqual(decayed_happiness, 0.5)

    def test_asymmetric_trust(self):
        """Validates that trust falls faster than it rises."""
        trust = AsymmetricTrustModel(initial_trust=0.5)
        
        # +0.8 positive interaction
        trust.process_interaction(0.8)
        positive_delta = trust.trust_level - 0.5
        
        # Reset and apply -0.8 negative interaction
        trust.trust_level = 0.5
        trust.process_interaction(-0.8)
        negative_delta = 0.5 - trust.trust_level
        
        # The drop should be significantly larger than the gain
        self.assertGreater(negative_delta, positive_delta)

    def test_tom_divergence(self):
        """Tests the Jensen-Shannon divergence math for belief misalignment."""
        node_a = TheoryOfMindNode("AgentA", depth=0, state_dim=2)
        node_b = TheoryOfMindNode("AgentB", depth=0, state_dim=2)
        
        node_a.belief_mean = np.array([1.0, 0.0])
        node_b.belief_mean = np.array([0.0, 1.0])
        
        divergence = node_a.compute_jensen_shannon_divergence(node_b)
        self.assertGreater(divergence, 0.0)
