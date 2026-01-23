"""
app/services/ocr_service.py
OCR processing orchestration service - FAST & ACCURATE VERSION
"""

import pytesseract
from PIL import Image
import cv2
import numpy as np
from pdf2image import convert_from_path
import time
from typing import List
import os
import re
import subprocess

from app.core.config import settings
from app.services.preprocessing import ImagePreprocessor
from app.schemas.ocr import OCRResult
from app.core.exceptions import OCRProcessingException


def check_tesseract_available() -> bool:
    """Check if Tesseract is installed and available"""
    try:
        subprocess.run(['tesseract', '--version'], capture_output=True, check=True, timeout=5)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError, OSError):
        return False


class OCRService:
    """OCR processing service using Tesseract - optimized for speed & readability"""

    # Modern LSTM + single block of text (best for most scanned docs)
    TESSERACT_CONFIG = '--oem 1 --psm 6'

    def __init__(self):
        if settings.TESSERACT_CMD:
            pytesseract.pytesseract.tesseract_cmd = settings.TESSERACT_CMD
        self.preprocessor = ImagePreprocessor()
        self.tesseract_available = check_tesseract_available()

    def process_file(self, file_path: str, language: str = None) -> List[OCRResult]:
        if not self.tesseract_available:
            error_msg = (
                "Tesseract OCR is not installed on the server. "
                "The app is running in native Python mode instead of Docker. "
                "To fix this: go to Render dashboard → Settings → Change Environment to 'Docker' → Redeploy. "
                "Your Dockerfile has Tesseract configured. "
            )
            raise OCRProcessingException(error_msg)
            
        if language is None:
            language = settings.DEFAULT_LANGUAGE
        
        file_ext = os.path.splitext(file_path)[1].lower()
        
        if file_ext == '.pdf':
            return self._process_pdf(file_path, language)
        else:
            return self._process_image(file_path, language)

    def _process_pdf(self, pdf_path: str, language: str) -> List[OCRResult]:
        results = []
        try:
            # Lower DPI = much faster, still excellent quality
            images = convert_from_path(pdf_path, dpi=250)
            
            for page_num, image in enumerate(images, start=1):
                cv2_image = self.preprocessor.pil_to_cv2(image)
                result = self._process_single_image(cv2_image, page_num, language)
                results.append(result)
            return results
        except Exception as e:
            raise OCRProcessingException(f"Failed to process PDF: {str(e)}")

    def _process_image(self, image_path: str, language: str) -> List[OCRResult]:
        try:
            image = cv2.imread(image_path)
            if image is None:
                raise OCRProcessingException("Failed to load image")
            result = self._process_single_image(image, 1, language)
            return [result]
        except Exception as e:
            raise OCRProcessingException(f"Failed to process image: {str(e)}")

    def _process_single_image(
        self, image: np.ndarray, page_number: int, language: str
    ) -> OCRResult:
        start_time = time.time()
        try:
            # Resize if huge
            image = self.preprocessor.resize_if_needed(image, max_dimension=2200)

            # === OPTIMIZED PREPROCESSING ===
            processed = self._optimized_preprocess(image)

            # Convert to PIL
            pil_image = self.preprocessor.cv2_to_pil(processed)

            # OCR
            ocr_data = pytesseract.image_to_data(
                pil_image, lang=language,
                output_type=pytesseract.Output.DICT,
                config=self.TESSERACT_CONFIG
            )

            text = pytesseract.image_to_string(
                pil_image, lang=language, config=self.TESSERACT_CONFIG
            )

            # Handle empty cases
            text = text or ""

            # Confidence
            confidences = [int(c) for c in ocr_data['conf'] if c != '-1']
            avg_confidence = sum(confidences) / len(confidences) if confidences else 0

            processing_time = time.time() - start_time

            text = self._clean_text(text)

            return OCRResult(
                page_number=page_number,
                text=text,
                confidence=avg_confidence / 100.0,
                processing_time=processing_time
            )

        except Exception as e:
            processing_time = time.time() - start_time
            raise OCRProcessingException(f"OCR failed on page {page_number}: {str(e)}")

    # ──── OPTIMIZED PREPROCESSING ───────────────────────────────────────
    def _optimized_preprocess(self, image: np.ndarray) -> np.ndarray:
        """Faster & better for Tesseract: grayscale → denoise → CLAHE → light sharpen"""
        if len(image.shape) == 3:
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        else:
            gray = image.copy()

        # Denoise (keep it light)
        denoised = cv2.bilateralFilter(gray, d=7, sigmaColor=50, sigmaSpace=50)

        # Contrast enhancement
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
        enhanced = clahe.apply(denoised)

        # Light sharpening (helps Tesseract a lot!)
        kernel = np.array([[-1,-1,-1], [-1,9,-1], [-1,-1,-1]])
        sharpened = cv2.filter2D(enhanced, -1, kernel)

        # Return grayscale enhanced image (NO binarization!)
        return sharpened

    def _clean_text(self, text: str) -> str:
        if not text:
            return ""
        
        # Split lines and clean each
        lines = [line.strip() for line in text.split('\n') if line.strip()]
        
        # Join and normalize spaces
        result = '\n'.join(lines)
        result = re.sub(r'  +', ' ', result)        # multiple spaces → one
        result = re.sub(r'\n{3,}', '\n\n', result)  # multiple newlines → two
        
        return result.strip()

    def get_supported_languages(self) -> List[str]:
        return ['eng', 'fra', 'deu', 'spa', 'ita', 'por', 'rus', 'jpn', 'kor', 'chi_sim', 'chi_tra']