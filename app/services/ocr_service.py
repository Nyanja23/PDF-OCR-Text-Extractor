"""
app/services/ocr_service.py
OCR processing orchestration service
"""

import pytesseract
from PIL import Image
import cv2
import numpy as np
from pdf2image import convert_from_path
import time
from typing import List, Tuple
import os

from app.core.config import settings
from app.services.preprocessing import ImagePreprocessor
from app.schemas.user import OCRResult
from app.core.exceptions import OCRProcessingException


class OCRService:
    """OCR processing service using Tesseract"""
    
    def __init__(self):
        # Set Tesseract command path
        if settings.TESSERACT_CMD:
            pytesseract.pytesseract.tesseract_cmd = settings.TESSERACT_CMD
        
        self.preprocessor = ImagePreprocessor()
    
    def process_file(self, file_path: str, language: str = None) -> List[OCRResult]:
        """
        Process a file (PDF or image) and extract text
        Returns list of OCRResult for each page
        """
        if language is None:
            language = settings.DEFAULT_LANGUAGE
        
        # Determine file type
        file_ext = os.path.splitext(file_path)[1].lower()
        
        if file_ext == '.pdf':
            return self._process_pdf(file_path, language)
        else:
            return self._process_image(file_path, language)
    
    def _process_pdf(self, pdf_path: str, language: str) -> List[OCRResult]:
        """Process PDF file page by page"""
        results = []
        
        try:
            # Convert PDF to images
            images = convert_from_path(pdf_path, dpi=300)
            
            for page_num, image in enumerate(images, start=1):
                # Convert PIL image to numpy array
                cv2_image = self.preprocessor.pil_to_cv2(image)
                
                # Process the page
                result = self._process_single_image(cv2_image, page_num, language)
                results.append(result)
            
            return results
        
        except Exception as e:
            raise OCRProcessingException(f"Failed to process PDF: {str(e)}")
    
    def _process_image(self, image_path: str, language: str) -> List[OCRResult]:
        """Process single image file"""
        try:
            # Load image
            image = cv2.imread(image_path)
            
            if image is None:
                raise OCRProcessingException("Failed to load image")
            
            # Process the image
            result = self._process_single_image(image, 1, language)
            
            return [result]
        
        except Exception as e:
            raise OCRProcessingException(f"Failed to process image: {str(e)}")
    
    def _process_single_image(
        self,
        image: np.ndarray,
        page_number: int,
        language: str
    ) -> OCRResult:
        """Process a single image and extract text"""
        start_time = time.time()
        
        try:
            # Resize if too large
            image = self.preprocessor.resize_if_needed(image)
            
            # Apply preprocessing pipeline
            preprocessed = self.preprocessor.preprocess(image)
            
            # Convert back to PIL for Tesseract
            pil_image = self.preprocessor.cv2_to_pil(preprocessed)
            
            # Perform OCR with data for confidence scores
            ocr_data = pytesseract.image_to_data(
                pil_image,
                lang=language,
                output_type=pytesseract.Output.DICT,
                config='--psm 3'  # Fully automatic page segmentation
            )
            
            # Extract text
            text = pytesseract.image_to_string(
                pil_image,
                lang=language,
                config='--psm 3'
            )
            
            # Calculate average confidence
            confidences = [
                int(conf) for conf in ocr_data['conf']
                if conf != '-1'
            ]
            avg_confidence = sum(confidences) / len(confidences) if confidences else 0
            
            processing_time = time.time() - start_time
            
            # Clean up text
            text = self._clean_text(text)
            
            return OCRResult(
                page_number=page_number,
                text=text,
                confidence=avg_confidence / 100.0,  # Convert to 0-1 range
                processing_time=processing_time
            )
        
        except Exception as e:
            processing_time = time.time() - start_time
            raise OCRProcessingException(
                f"OCR failed on page {page_number}: {str(e)}"
            )
    
    def _clean_text(self, text: str) -> str:
        """Clean extracted text"""
        # Remove excessive whitespace
        lines = text.split('\n')
        cleaned_lines = []
        
        for line in lines:
            # Strip whitespace from each line
            line = line.strip()
            
            # Keep non-empty lines
            if line:
                cleaned_lines.append(line)
        
        # Join with single newlines
        cleaned_text = '\n'.join(cleaned_lines)
        
        # Remove multiple consecutive newlines
        while '\n\n\n' in cleaned_text:
            cleaned_text = cleaned_text.replace('\n\n\n', '\n\n')
        
        return cleaned_text.strip()
    
    def get_supported_languages(self) -> List[str]:
        """Get list of supported languages from Tesseract"""
        try:
            langs = pytesseract.get_languages()
            return langs
        except Exception:
            return [settings.DEFAULT_LANGUAGE]
