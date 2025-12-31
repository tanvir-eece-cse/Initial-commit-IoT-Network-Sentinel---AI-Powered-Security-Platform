"""
Rate Limiting Middleware
Implements request rate limiting per client IP
"""
import time
from collections import defaultdict
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse

from app.core.config import settings


class RateLimitMiddleware(BaseHTTPMiddleware):
    """Middleware to implement rate limiting"""
    
    def __init__(self, app):
        super().__init__(app)
        self.rate_limit = settings.RATE_LIMIT_PER_MINUTE
        self.window_size = 60  # 1 minute window
        self.requests = defaultdict(list)
    
    async def dispatch(self, request: Request, call_next):
        # Get client IP
        client_ip = request.client.host if request.client else "unknown"
        forwarded_for = request.headers.get("X-Forwarded-For")
        if forwarded_for:
            client_ip = forwarded_for.split(",")[0].strip()
        
        # Skip rate limiting for health checks
        if request.url.path in ["/health", "/metrics"]:
            return await call_next(request)
        
        current_time = time.time()
        
        # Clean old requests
        self.requests[client_ip] = [
            req_time for req_time in self.requests[client_ip]
            if current_time - req_time < self.window_size
        ]
        
        # Check rate limit
        if len(self.requests[client_ip]) >= self.rate_limit:
            return JSONResponse(
                status_code=429,
                content={
                    "detail": "Too many requests. Please try again later.",
                    "retry_after": self.window_size
                },
                headers={"Retry-After": str(self.window_size)}
            )
        
        # Record this request
        self.requests[client_ip].append(current_time)
        
        # Add rate limit headers
        response = await call_next(request)
        remaining = self.rate_limit - len(self.requests[client_ip])
        response.headers["X-RateLimit-Limit"] = str(self.rate_limit)
        response.headers["X-RateLimit-Remaining"] = str(remaining)
        response.headers["X-RateLimit-Reset"] = str(int(current_time + self.window_size))
        
        return response
