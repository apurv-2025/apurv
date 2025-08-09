# backend/utils/encryption.py
from cryptography.fernet import Fernet
from typing import Optional
import base64
import os

class EncryptionService:
    """Service for encrypting/decrypting sensitive data."""

    def __init__(self):
        # In production, store this in environment variables or key management service
        key = os.getenv('ENCRYPTION_KEY')
        if not key:
            # Generate a key for development (don't do this in production)
            key = Fernet.generate_key()
        else:
            key = key.encode()

        self.cipher_suite = Fernet(key)

    def encrypt(self, data: str) -> str:
        """Encrypt a string."""
        if not data:
            return data

        encrypted_data = self.cipher_suite.encrypt(data.encode())
        return base64.urlsafe_b64encode(encrypted_data).decode()

    def decrypt(self, encrypted_data: str) -> str:
        """Decrypt a string."""
        if not encrypted_data:
            return encrypted_data

        try:
            decoded_data = base64.urlsafe_b64decode(encrypted_data.encode())
            decrypted_data = self.cipher_suite.decrypt(decoded_data)
            return decrypted_data.decode()
        except Exception:
            # Return original data if decryption fails (for backward compatibility)
            return encrypted_data

# Global instance
encryption_service = EncryptionService()
