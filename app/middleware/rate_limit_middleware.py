"""
app/middleware/rate_limit_middleware.py
Rate limiting middleware
"""

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse
from typing import Dict
from datetime import datetime, timedelta
from collections import defaultdict
import asyncio

from app.core.config import settings


class RateLimiter:
    """In-memory rate limiter"""
    
    def __init__(self, max_requests: int = 100, window_seconds: int = 900):
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self.requests: Dict[str, list] = defaultdict(list)
        self.lock = asyncio.Lock()
    
    async def is_allowed(self, key: str) -> bool:
        """Check if request is allowed"""
        async with self.lock:
            now = datetime.now()
            cutoff = now - timedelta(seconds=self.window_seconds)
            
            # Remove old requests
            self.requests[key] = [
                req_time for req_time in self.requests[key]
                if req_time > cutoff
            ]
            
            # Check if under limit
            if len(self.requests[key]) < self.max_requests:
                self.requests[key].append(now)
                return True
            
            return False
    
    async def cleanup(self):
        """Periodically cleanup old entries"""
        async with self.lock:
            now = datetime.now()
            cutoff = now - timedelta(seconds=self.window_seconds * 2)
            
            keys_to_delete = []
            for key, timestamps in self.requests.items():
                # Remove old timestamps
                self.requests[key] = [t for t in timestamps if t > cutoff]
                
                # Mark empty keys for deletion
                if not self.requests[key]:
                    keys_to_delete.append(key)
            
            # Delete empty keys
            for key in keys_to_delete:
                del self.requests[key]


# Global rate limiter instances
auth_limiter = RateLimiter(max_requests=5, window_seconds=900)  # 5 per 15 min
general_limiter = RateLimiter(max_requests=100, window_seconds=900)  # 100 per 15 min


class RateLimitMiddleware(BaseHTTPMiddleware):
    """Rate limiting middleware for FastAPI"""
    
    async def dispatch(self, request: Request, call_next):
        # Get client IP
        client_ip = request.client.host
        
        # Determine which limiter to use
        path = request.url.path
        
        # Apply stricter rate limiting to auth endpoints
        if any(path.startswith(p) for p in ['/api/auth/login', '/api/auth/register']):
            limiter = auth_limiter
            rate_limit_type = "auth"
        else:
            limiter = general_limiter
            rate_limit_type = "general"
        
        # Check rate limit
        if not await limiter.is_allowed(f"{rate_limit_type}:{client_ip}"):
            return JSONResponse(
                status_code=429,
                content={
                    "detail": "Too many requests. Please try again later.",
                    "retry_after": settings.RATE_LIMIT_WINDOW
                }
            )
        
        # Process request
        response = await call_next(request)
        return response
