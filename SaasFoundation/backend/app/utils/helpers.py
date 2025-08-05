import re
from typing import Optional

def generate_slug(text: str, max_length: int = 50) -> str:
    """Generate a URL-friendly slug from text"""
    # Convert to lowercase and replace non-alphanumeric chars with hyphens
    slug = re.sub(r'[^a-zA-Z0-9-]', '-', text.lower())
    
    # Remove multiple consecutive hyphens
    slug = re.sub(r'-+', '-', slug)
    
    # Remove leading/trailing hyphens
    slug = slug.strip('-')
    
    # Truncate if too long
    if len(slug) > max_length:
        slug = slug[:max_length].rstrip('-')
    
    return slug

def validate_email_domain(email: str, allowed_domains: Optional[list] = None) -> bool:
    """Validate email domain against allowed list"""
    if not allowed_domains:
        return True
    
    domain = email.split('@')[1].lower()
    return domain in [d.lower() for d in allowed_domains]

def format_currency(amount: float, currency: str = "USD") -> str:
    """Format currency amount"""
    if currency == "USD":
        return f"${amount:,.2f}"
    return f"{amount:,.2f} {currency}"
