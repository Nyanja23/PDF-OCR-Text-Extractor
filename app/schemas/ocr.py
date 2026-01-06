"""
app/schemas/ocr.py
OCR-related Pydantic schemas
"""

from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


class OCRResult(BaseModel):
    page_number: int
    text: str
    confidence: Optional[float] = None
    processing_time: float


class OCRResponse(BaseModel):
    job_id: str
    filename: str
    total_pages: int
    results: List[OCRResult]
    total_processing_time: float
    created_at: datetime


class OCRStatus(BaseModel):
    job_id: str
    status: str  # 'processing', 'completed', 'failed'
    progress: int  # 0-100
    message: Optional[str] = None