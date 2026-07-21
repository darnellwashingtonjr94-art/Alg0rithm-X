import cv2
import numpy as np

class SegmentationEngine:
    """
    Isolates moving foreground entities from static backgrounds using MOG2
    and calculates dense optical flow for predictive tracking.
    """
    def __init__(self, history: int = 500, var_threshold: float = 16.0):
        # MOG2 Background Subtractor
        self.bg_subtractor = cv2.createBackgroundSubtractorMOG2(
            history=history, 
            varThreshold=var_threshold, 
            detectShadows=True
        )
        self.previous_gray = None

    def generate_mask(self, frame: np.ndarray) -> np.ndarray:
        """Generates a binary mask of the foreground subject."""
        fg_mask = self.bg_subtractor.apply(frame)
        
        # Remove noise and shadows (Shadows are marked as 127 in MOG2)
        _, fg_mask = cv2.threshold(fg_mask, 254, 255, cv2.THRESH_BINARY)
        
        # Morphological operations to clean up the mask
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
        fg_mask = cv2.morphologyEx(fg_mask, cv2.MORPH_OPEN, kernel)
        fg_mask = cv2.morphologyEx(fg_mask, cv2.MORPH_CLOSE, kernel)
        
        return fg_mask

    def calculate_optical_flow(self, frame: np.ndarray) -> np.ndarray:
        """Computes dense optical flow (Farneback) to track movement vectors."""
        current_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        if self.previous_gray is None:
            self.previous_gray = current_gray
            # Return an empty flow matrix of the same dimensions
            return np.zeros((frame.shape[0], frame.shape[1], 2), dtype=np.float32)
            
        flow = cv2.calcOpticalFlowFarneback(
            self.previous_gray, current_gray, None, 
            pyr_scale=0.5, levels=3, winsize=15, 
            iterations=3, poly_n=5, poly_sigma=1.2, flags=0
        )
        
        self.previous_gray = current_gray
        return flow
