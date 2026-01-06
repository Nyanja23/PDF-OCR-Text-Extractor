"""
app/services/file_service.py
File upload and management service
"""

import os
import uuid
import shutil
from pathlib import Path
from typing import Optional
from datetime import datetime, timedelta

from fastapi import UploadFile
from app.core.config import settings
from app.core.exceptions import BadRequestException


class FileService:
    """File management service"""
    
    def __init__(self):
        self.upload_dir = Path(settings.UPLOAD_DIR)
        self.upload_dir.mkdir(exist_ok=True)
    
    def save_upload(self, file: UploadFile) -> str:
        """
        Save uploaded file and return file path
        Returns: absolute path to saved file
        """
        # Validate file
        self._validate_file(file)
        
        # Generate unique filename
        file_ext = os.path.splitext(file.filename)[1].lower()
        unique_filename = f"{uuid.uuid4()}{file_ext}"
        file_path = self.upload_dir / unique_filename
        
        # Save file
        try:
            with open(file_path, "wb") as buffer:
                shutil.copyfileobj(file.file, buffer)
        except Exception as e:
            raise BadRequestException(f"Failed to save file: {str(e)}")
        
        return str(file_path)
    
    def delete_file(self, file_path: str) -> bool:
        """Delete a file"""
        try:
            if os.path.exists(file_path):
                os.remove(file_path)
                return True
            return False
        except Exception as e:
            print(f"Error deleting file {file_path}: {e}")
            return False
    
    def _validate_file(self, file: UploadFile):
        """Validate uploaded file"""
        # Check file extension
        file_ext = os.path.splitext(file.filename)[1].lower()
        if file_ext not in settings.ALLOWED_EXTENSIONS:
            raise BadRequestException(
                f"File type not allowed. Supported: {', '.join(settings.ALLOWED_EXTENSIONS)}"
            )
        
        # Check file size (read content to get actual size)
        file.file.seek(0, 2)  # Seek to end
        file_size = file.file.tell()
        file.file.seek(0)  # Seek back to start
        
        max_size = settings.MAX_FILE_SIZE_MB * 1024 * 1024
        if file_size > max_size:
            raise BadRequestException(
                f"File too large. Maximum size: {settings.MAX_FILE_SIZE_MB}MB"
            )
        
        # Validate content type
        content_type = file.content_type or ""
        valid_types = [
            "application/pdf",
            "image/jpeg",
            "image/jpg",
            "image/png",
            "image/tiff"
        ]
        
        if not any(ct in content_type for ct in valid_types):
            # Additional check based on extension
            if file_ext not in settings.ALLOWED_EXTENSIONS:
                raise BadRequestException("Invalid file type")
    
    def cleanup_old_files(self):
        """Delete files older than FILE_CLEANUP_HOURS"""
        cutoff_time = datetime.now() - timedelta(hours=settings.FILE_CLEANUP_HOURS)
        deleted_count = 0
        
        try:
            for file_path in self.upload_dir.iterdir():
                if file_path.is_file():
                    # Get file modification time
                    file_mtime = datetime.fromtimestamp(file_path.stat().st_mtime)
                    
                    if file_mtime < cutoff_time:
                        file_path.unlink()
                        deleted_count += 1
            
            if deleted_count > 0:
                print(f"🗑️ Cleaned up {deleted_count} old files")
        
        except Exception as e:
            print(f"Error during file cleanup: {e}")
        
        return deleted_count
