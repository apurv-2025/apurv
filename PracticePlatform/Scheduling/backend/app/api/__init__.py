"""
API Module
Contains all API routers for the Scheduling2.0 application
"""

from . import patients
from . import practitioners
from . import waitlist

__all__ = ["patients", "practitioners", "waitlist"] 