from datetime import datetime, timezone
import sys

def utcnow():
    """
    Get current UTC datetime that works across Python versions
    """
    if sys.version_info >= (3, 11):
        try:
            return datetime.now(datetime.UTC)
        except AttributeError:
            # Fallback if datetime.UTC is not available
            return datetime.now(timezone.utc)
    else:
        return datetime.now(timezone.utc)

def utc_timezone():
    """
    Get UTC timezone object that works across Python versions
    """
    if sys.version_info >= (3, 11):
        try:
            return datetime.UTC
        except AttributeError:
            return timezone.utc
    else:
        return timezone.utc
