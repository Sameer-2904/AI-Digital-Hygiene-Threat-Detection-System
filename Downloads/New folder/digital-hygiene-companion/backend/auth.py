"""API Key authentication and rate limiting module"""

import os
import logging
from typing import Optional, Dict
from datetime import datetime, timedelta
from fastapi import Header, HTTPException, status
from functools import lru_cache

logger = logging.getLogger(__name__)


class RateLimiter:
    """Simple in-memory rate limiter with per-API-key tracking"""
    
    def __init__(self, requests_per_minute: int = 60):
        self.requests_per_minute = requests_per_minute
        self.requests: Dict[str, list] = {}  # key -> list of timestamps
    
    def is_allowed(self, api_key: str) -> bool:
        """Check if a request from api_key is allowed (returns False if rate limited)"""
        now = datetime.utcnow()
        cutoff = now - timedelta(minutes=1)
        
        if api_key not in self.requests:
            self.requests[api_key] = []
        
        # Remove old requests outside the 1-minute window
        self.requests[api_key] = [ts for ts in self.requests[api_key] if ts > cutoff]
        
        # Check if limit exceeded
        if len(self.requests[api_key]) >= self.requests_per_minute:
            return False
        
        # Record this request
        self.requests[api_key].append(now)
        return True
    
    def get_remaining(self, api_key: str) -> int:
        """Get remaining requests for this API key in current minute"""
        now = datetime.utcnow()
        cutoff = now - timedelta(minutes=1)
        
        if api_key not in self.requests:
            return self.requests_per_minute
        
        active = [ts for ts in self.requests[api_key] if ts > cutoff]
        return max(0, self.requests_per_minute - len(active))


# Initialize rate limiter (60 requests per minute by default)
rate_limiter = RateLimiter(requests_per_minute=60)


@lru_cache(maxsize=10)
def get_valid_api_keys() -> list:
    """
    Load valid API keys from environment variables.
    Format: API_KEYS env var should contain comma-separated keys
    Example: API_KEYS="key1,key2,key3"
    
    If no API_KEYS env var is set, returns empty list (auth is optional).
    """
    keys_env = os.getenv("API_KEYS", "")
    if not keys_env:
        logger.warning("No API_KEYS environment variable set. API key auth is disabled.")
        return []
    
    return [key.strip() for key in keys_env.split(",") if key.strip()]


def validate_api_key(
    authorization: Optional[str] = Header(None),
    api_key: Optional[str] = Header(None)
) -> str:
    """
    Validate API key from either Authorization header or api-key header.
    
    Accepts:
    - Header: Authorization: Bearer <api_key>
    - Header: api-key: <api_key>
    
    Returns the API key if valid or "public" if no auth is configured.
    Raises HTTPException if auth is required but missing or invalid.
    """
    valid_keys = get_valid_api_keys()
    
    # If no API keys configured, allow public access
    if not valid_keys:
        return "public"
    
    # Extract key from Authorization header (Bearer <key>)
    provided_key = None
    if authorization:
        parts = authorization.split()
        if len(parts) == 2 and parts[0].lower() == "bearer":
            provided_key = parts[1]
    
    # Or extract from api-key header
    if not provided_key and api_key:
        provided_key = api_key
    
    # Validate
    if not provided_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="API key required. Use 'Authorization: Bearer <key>' or 'api-key: <key>' header."
        )
    
    if provided_key not in valid_keys:
        logger.warning(f"Invalid API key attempt: {provided_key[:8]}...")
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid API key"
        )
    
    return provided_key


def check_rate_limit(api_key: str):
    """
    Check if API key has exceeded rate limit.
    Raises HTTPException if rate limit exceeded.
    """
    if not rate_limiter.is_allowed(api_key):
        remaining = rate_limiter.get_remaining(api_key)
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail=f"Rate limit exceeded. Max 60 requests per minute. Retrying in 1 minute."
        )
