"""
app/services/preprocessing.py
Advanced image preprocessing pipeline for OCR
"""

import cv2
import numpy as np
from PIL import Image
from typing import Tuple
import io


class ImagePreprocessor:
    """Advanced image preprocessing for better OCR accuracy"""
    
    @staticmethod
    def preprocess(image: np.ndarray) -> np.ndarray:
        """
        Apply full preprocessing pipeline
        Pipeline: Grayscale → Noise Reduction → Contrast Enhancement → Thresholding → Deskew
        """
        # Convert to grayscale if needed
        if len(image.shape) == 3:
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        else:
            gray = image.copy()
        
        # Apply bilateral filter for noise reduction while preserving edges
        denoised = ImagePreprocessor._denoise(gray)
        
        # Enhance contrast using CLAHE
        enhanced = ImagePreprocessor._enhance_contrast(denoised)
        
        # Apply adaptive thresholding
        thresholded = ImagePreprocessor._adaptive_threshold(enhanced)
        
        # Deskew the image
        deskewed = ImagePreprocessor._deskew(thresholded)
        
        return deskewed
    
    @staticmethod
    def _denoise(image: np.ndarray) -> np.ndarray:
        """Apply bilateral filtering for noise reduction"""
        # Bilateral filter: reduces noise while keeping edges sharp
        # Parameters: d=9 (diameter), sigmaColor=75, sigmaSpace=75
        return cv2.bilateralFilter(image, 9, 75, 75)
    
    @staticmethod
    def _enhance_contrast(image: np.ndarray) -> np.ndarray:
        """Enhance contrast using CLAHE (Contrast Limited Adaptive Histogram Equalization)"""
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
        return clahe.apply(image)
    
    @staticmethod
    def _adaptive_threshold(image: np.ndarray) -> np.ndarray:
        """Apply adaptive thresholding for better text/background separation"""
        # Gaussian adaptive thresholding works better for varying lighting
        return cv2.adaptiveThreshold(
            image,
            255,
            cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
            cv2.THRESH_BINARY,
            11,  # Block size
            2    # Constant subtracted from mean
        )
    
    @staticmethod
    def _deskew(image: np.ndarray) -> np.ndarray:
        """Detect and correct skew in the image"""
        # Find all white pixels
        coords = np.column_stack(np.where(image > 0))
        
        if len(coords) < 100:  # Not enough points to determine skew
            return image
        
        # Calculate the angle of skew
        angle = cv2.minAreaRect(coords)[-1]
        
        # Adjust angle
        if angle < -45:
            angle = 90 + angle
        elif angle > 45:
            angle = angle - 90
        
        # Only deskew if angle is significant (> 0.5 degrees)
        if abs(angle) < 0.5:
            return image
        
        # Rotate image to deskew
        (h, w) = image.shape[:2]
        center = (w // 2, h // 2)
        M = cv2.getRotationMatrix2D(center, angle, 1.0)
        rotated = cv2.warpAffine(
            image,
            M,
            (w, h),
            flags=cv2.INTER_CUBIC,
            borderMode=cv2.BORDER_REPLICATE
        )
        
        return rotated
    
    @staticmethod
    def resize_if_needed(image: np.ndarray, max_dimension: int = 3000) -> np.ndarray:
        """Resize image if it's too large"""
        height, width = image.shape[:2]
        
        if max(height, width) > max_dimension:
            scale = max_dimension / max(height, width)
            new_width = int(width * scale)
            new_height = int(height * scale)
            
            return cv2.resize(
                image,
                (new_width, new_height),
                interpolation=cv2.INTER_AREA
            )
        
        return image
    
    @staticmethod
    def pil_to_cv2(pil_image: Image.Image) -> np.ndarray:
        """Convert PIL Image to OpenCV format"""
        return cv2.cvtColor(np.array(pil_image), cv2.COLOR_RGB2BGR)
    
    @staticmethod
    def cv2_to_pil(cv2_image: np.ndarray) -> Image.Image:
        """Convert OpenCV image to PIL format"""
        if len(cv2_image.shape) == 2:  # Grayscale
            return Image.fromarray(cv2_image)
        else:  # Color
            return Image.fromarray(cv2.cvtColor(cv2_image, cv2.COLOR_BGR2RGB))
