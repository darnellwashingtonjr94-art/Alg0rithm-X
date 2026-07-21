import unittest
import numpy as np
from src.visual_cloak.segmentation import SegmentationEngine
from src.visual_cloak.alignment import FrameAlignmentEngine

class TestCloakPipeline(unittest.TestCase):
    
    def setUp(self):
        # Create a mock 480x640 BGR frame (solid black)
        self.blank_frame = np.zeros((480, 640, 3), dtype=np.uint8)
        
        # Create a noisy frame to simulate movement
        self.noise_frame = np.random.randint(0, 255, (480, 640, 3), dtype=np.uint8)

    def test_optical_flow_initialization(self):
        """Ensures the first frame initializes a zero-vector flow matrix."""
        engine = SegmentationEngine()
        flow = engine.calculate_optical_flow(self.blank_frame)
        
        self.assertEqual(flow.shape, (480, 640, 2))
        self.assertTrue(np.all(flow == 0))

    def test_alignment_rejection(self):
        """Ensures homography fails safely if frames have no matching features."""
        engine = FrameAlignmentEngine(max_features=50)
        
        # Attempt to align a solid black frame with random static noise
        # This should fail to find RANSAC matches and return None
        result = engine.align_frames(self.noise_frame, self.blank_frame)
        self.assertIsNone(result)
