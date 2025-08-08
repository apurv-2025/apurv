import time
from typing import Dict, Tuple
from fastapi import Request, HTTPException, status
from starlette.middleware.base import BaseHTTPMiddleware


class RateLimitMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, calls: int = 100, period: int = 60):
        super().__init__(app)
        self.calls = calls
        self.period = period
        self.clients: Dict[str, Tuple[int, float]] = {}

    async def dispatch(self, request: Request, call_next):
        client_ip = request.client.host
        current_time = time.time()
        
        # Clean old entries
        self.clients = {
            ip: (count, timestamp) 
            for ip, (count, timestamp) in self.clients.items()
            if current_time - timestamp < self.period
        }
        
        # Check rate limit
        if client_ip in self.clients:
            count, timestamp = self.clients[client_ip]
            if current_time - timestamp < self.period:
                if count >= self.calls:
                    raise HTTPException(
                        status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                        detail="Rate limit exceeded"
                    )
                self.clients[client_ip] = (count + 1, timestamp)
            else:
                self.clients[client_ip] = (1, current_time)
        else:
            self.clients[client_ip] = (1, current_time)
        
        response = await call_next(request)
        return response
