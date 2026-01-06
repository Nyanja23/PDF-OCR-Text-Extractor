"""
app/routers/ocr.py
OCR processing API endpoints
"""

from fastapi import APIRouter, Depends, UploadFile, File, Form, BackgroundTasks
from fastapi.responses import FileResponse, PlainTextResponse
from sqlalchemy.orm import Session
from typing import Optional
import uuid
import time
from datetime import datetime

from app.core.database import get_db
from app.core.dependencies import get_verified_user
from app.models.user import User
from app.schemas.ocr import OCRResponse, OCRResult
from app.services.ocr_service import OCRService
from app.services.file_service import FileService
from app.core.exceptions import BadRequestException, OCRProcessingException


router = APIRouter()


# In-memory storage for OCR jobs (in production, use Redis or database)
ocr_jobs = {}


@router.post("/upload", response_model=OCRResponse)
async def upload_and_process(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...),
    language: Optional[str] = Form(None),
    current_user: User = Depends(get_verified_user),
    db: Session = Depends(get_db)
):
    """
    Upload and process a document
    This is a synchronous endpoint - file is processed immediately
    """
    start_time = time.time()
    
    # Initialize services
    file_service = FileService()
    ocr_service = OCRService()
    
    # Save uploaded file
    file_path = file_service.save_upload(file)
    
    # Schedule cleanup
    background_tasks.add_task(file_service.delete_file, file_path)
    
    try:
        # Process file
        results = ocr_service.process_file(file_path, language)
        
        total_time = time.time() - start_time
        job_id = str(uuid.uuid4())
        
        # Create response
        response = OCRResponse(
            job_id=job_id,
            filename=file.filename,
            total_pages=len(results),
            results=results,
            total_processing_time=total_time,
            created_at=datetime.utcnow()
        )
        
        # Store result for later retrieval
        ocr_jobs[job_id] = {
            "user_id": current_user.id,
            "response": response,
            "created_at": datetime.utcnow()
        }
        
        return response
    
    except Exception as e:
        # Cleanup on error
        file_service.delete_file(file_path)
        raise OCRProcessingException(f"Failed to process document: {str(e)}")


@router.get("/result/{job_id}", response_model=OCRResponse)
async def get_result(
    job_id: str,
    current_user: User = Depends(get_verified_user)
):
    """Get OCR result by job ID"""
    job = ocr_jobs.get(job_id)
    
    if not job:
        raise BadRequestException("Job not found")
    
    # Verify ownership
    if job["user_id"] != current_user.id:
        raise BadRequestException("Unauthorized access to job")
    
    return job["response"]


@router.post("/export/{job_id}")
async def export_text(
    job_id: str,
    format: str = "txt",  # Future: support docx, pdf
    current_user: User = Depends(get_verified_user)
):
    """Export OCR result as downloadable file"""
    job = ocr_jobs.get(job_id)
    
    if not job:
        raise BadRequestException("Job not found")
    
    if job["user_id"] != current_user.id:
        raise BadRequestException("Unauthorized access to job")
    
    response_data: OCRResponse = job["response"]
    
    # Combine all page texts
    full_text = "\n\n".join([
        f"--- Page {result.page_number} ---\n{result.text}"
        for result in response_data.results
    ])
    
    if format == "txt":
        return PlainTextResponse(
            content=full_text,
            headers={
                "Content-Disposition": f"attachment; filename={response_data.filename}_extracted.txt"
            }
        )
    else:
        raise BadRequestException("Unsupported export format")


@router.get("/languages")
async def get_supported_languages():
    """Get list of supported OCR languages"""
    ocr_service = OCRService()
    languages = ocr_service.get_supported_languages()
    
    return {
        "languages": languages,
        "default": "eng"
    }


@router.delete("/cleanup-jobs")
async def cleanup_old_jobs(
    current_user: User = Depends(get_verified_user)
):
    """Cleanup old OCR jobs (admin only in production)"""
    cutoff_time = datetime.utcnow()
    
    jobs_to_delete = []
    for job_id, job_data in ocr_jobs.items():
        # Delete jobs older than 1 hour
        if (cutoff_time - job_data["created_at"]).total_seconds() > 3600:
            jobs_to_delete.append(job_id)
    
    for job_id in jobs_to_delete:
        del ocr_jobs[job_id]
    
    return {
        "message": f"Cleaned up {len(jobs_to_delete)} old jobs"
    }