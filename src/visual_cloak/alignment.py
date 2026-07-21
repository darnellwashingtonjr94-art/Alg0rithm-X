import cv2
import numpy as np
from typing import Tuple, Optional

class FrameAlignmentEngine:
    """
    Matches feature points between a saved background and the current frame
    to calculate a perspective transform (Homography), stabilizing the cloak.
    """
    def __init__(self, max_features: int = 500):
        self.orb = cv2.ORB_create(nfeatures=max_features)
        self.matcher = cv2.DescriptorMatcher_create(cv2.DESCRIPTOR_MATCHER_BRUTEFORCE_HAMMING)

    def extract_features(self, frame: np.ndarray) -> Tuple[list, np.ndarray]:
        """Detects keypoints and computes descriptors using ORB."""
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        keypoints, descriptors = self.orb.detectAndCompute(gray, None)
        return keypoints, descriptors

    def align_frames(self, live_frame: np.ndarray, bg_frame: np.ndarray) -> Optional[np.ndarray]:
        """
        Warps the background frame to match the perspective of the live camera feed.
        """
        kp1, des1 = self.extract_features(bg_frame)
        kp2, des2 = self.extract_features(live_frame)

        if des1 is None or des2 is None:
            return None

        matches = self.matcher.match(des1, des2, None)
        matches = sorted(matches, key=lambda x: x.distance)

        # Keep top 15% of matches
        good_matches = int(len(matches) * 0.15)
        matches = matches[:good_matches]

        if len(matches) < 4:
            # Not enough points to calculate homography
            return None

        # Extract coordinates of matched keypoints
        points1 = np.zeros((len(matches), 2), dtype=np.float32)
        points2 = np.zeros((len(matches), 2), dtype=np.float32)

        for i, match in enumerate(matches):
            points1[i, :] = kp1[match.queryIdx].pt
            points2[i, :] = kp2[match.trainIdx].pt

        # Find homography matrix using RANSAC
        h_matrix, _ = cv2.findHomography(points1, points2, cv2.RANSAC)
        
        if h_matrix is None:
            return None

        # Warp the background frame to align with the live camera perspective
        height, width, _ = live_frame.shape
        aligned_bg = cv2.warpPerspective(bg_frame, h_matrix, (width, height))
        
        return aligned_bg
