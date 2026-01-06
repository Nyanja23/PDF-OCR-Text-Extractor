"""
app/utils/file_handlers.py
File handling utility functions
"""

import os
from pathlib import Path
from datetime import datetime, timedelta
from app.core.config import settings


def cleanup_old_files():
    """Cleanup old files from upload directory"""
    upload_dir = Path(settings.UPLOAD_DIR)
    cutoff_time = datetime.now() - timedelta(hours=settings.FILE_CLEANUP_HOURS)
    deleted_count = 0
    
    try:
        for file_path in upload_dir.iterdir():
            if file_path.is_file():
                file_mtime = datetime.fromtimestamp(file_path.stat().st_mtime)
                
                if file_mtime < cutoff_time:
                    file_path.unlink()
                    deleted_count += 1
        
        if deleted_count > 0:
            print(f"🗑️ Cleaned up {deleted_count} old files")
    
    except Exception as e:
        print(f"Error during file cleanup: {e}")
    
    return deleted_count


def get_file_extension(filename: str) -> str:
    """Get file extension from filename"""
    return os.path.splitext(filename)[1].lower()


def is_pdf(filename: str) -> bool:
    """Check if file is PDF"""
    return get_file_extension(filename) == '.pdf'


def is_image(filename: str) -> bool:
    """Check if file is an image"""
    return get_file_extension(filename) in ['.jpg', '.jpeg', '.png', '.tiff']


def sanitize_filename(filename: str) -> str:
    """Sanitize filename to prevent directory traversal"""
    # Remove any path components
    filename = os.path.basename(filename)
    
    # Remove any potentially dangerous characters
    dangerous_chars = ['..', '/', '\\', '\0']
    for char in dangerous_chars:
        filename = filename.replace(char, '')
    
    return filename
