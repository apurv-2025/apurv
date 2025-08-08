from typing import Optional
from datetime import date, time, datetime


def format_date(dt: Optional[date]) -> Optional[str]:
    """Format date for API response"""
    if dt is None:
        return None
    return dt.isoformat()


def format_time(tm: Optional[time]) -> Optional[str]:
    """Format time for API response"""
    if tm is None:
        return None
    return tm.strftime("%H:%M")


def format_datetime(dt: Optional[datetime]) -> Optional[str]:
    """Format datetime for API response"""
    if dt is None:
        return None
    return dt.isoformat()


def format_file_size(size_bytes: int) -> str:
    """Format file size in human readable format"""
    if size_bytes == 0:
        return "0 B"
    
    size_names = ["B", "KB", "MB", "GB"]
    i = 0
    while size_bytes >= 1024 and i < len(size_names) - 1:
        size_bytes /= 1024.0
        i += 1
    
    return f"{size_bytes:.1f} {size_names[i]}"


def truncate_string(text: str, max_length: int = 100) -> str:
    """Truncate string to specified length"""
    if len(text) <= max_length:
        return text
    return text[:max_length - 3] + "..."
