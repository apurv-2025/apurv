"""
Encryption Manager for Healthcare Data Security
"""

import hashlib
import hmac
import secrets
import logging
import base64
from datetime import datetime
from typing import Dict, List, Any, Optional
from enum import Enum
import os

from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

logger = logging.getLogger(__name__)

class DataClassification(Enum):
    """Data classification levels"""
    PUBLIC = "public"
    INTERNAL = "internal"
    CONFIDENTIAL = "confidential"
    PHI = "phi"  # Protected Health Information

class EncryptionManager:
    """Handles all encryption/decryption operations"""
    
    def __init__(self, master_key: Optional[str] = None):
        if master_key:
            self.master_key = master_key.encode()
        else:
            self.master_key = os.environ.get('ENCRYPTION_MASTER_KEY', '').encode()
        
        if not self.master_key:
            # Generate a new key for development
            self.master_key = Fernet.generate_key()
            logger.warning("No master key provided, generated new key for development")
        
        # Derive encryption key from master key
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=b'healthcare_ml_salt',  # In production, use random salt per deployment
            iterations=100000,
        )
        key = base64.urlsafe_b64encode(kdf.derive(self.master_key))
        self.fernet = Fernet(key)
        
        # Generate RSA key pair for asymmetric encryption
        self.private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048,
        )
        self.public_key = self.private_key.public_key()
    
    def encrypt_data(self, data: str, classification: DataClassification = DataClassification.CONFIDENTIAL) -> str:
        """Encrypt sensitive data based on classification"""
        if classification == DataClassification.PUBLIC:
            return data  # No encryption needed
        
        if classification == DataClassification.PHI:
            # Use strongest encryption for PHI
            return self._encrypt_phi(data)
        
        # Standard encryption for confidential data
        return self.fernet.encrypt(data.encode()).decode()
    
    def decrypt_data(self, encrypted_data: str, classification: DataClassification = DataClassification.CONFIDENTIAL) -> str:
        """Decrypt data based on classification"""
        if classification == DataClassification.PUBLIC:
            return encrypted_data  # No decryption needed
        
        if classification == DataClassification.PHI:
            return self._decrypt_phi(encrypted_data)
        
        # Standard decryption for confidential data
        return self.fernet.decrypt(encrypted_data.encode()).decode()
    
    def _encrypt_phi(self, data: str) -> str:
        """Encrypt PHI with additional security measures"""
        # First encrypt with symmetric key
        symmetric_encrypted = self.fernet.encrypt(data.encode())
        
        # Then encrypt the symmetric key with RSA
        encrypted_key = self.public_key.encrypt(
            self.master_key,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        
        # Combine encrypted data and key
        combined = base64.b64encode(encrypted_key + symmetric_encrypted).decode()
        return combined
    
    def _decrypt_phi(self, encrypted_data: str) -> str:
        """Decrypt PHI data"""
        try:
            # Decode combined data
            combined = base64.b64decode(encrypted_data.encode())
            
            # Extract encrypted key and data
            key_size = 256  # RSA 2048 bit key size
            encrypted_key = combined[:key_size]
            symmetric_encrypted = combined[key_size:]
            
            # Decrypt the symmetric key
            decrypted_key = self.private_key.decrypt(
                encrypted_key,
                padding.OAEP(
                    mgf=padding.MGF1(algorithm=hashes.SHA256()),
                    algorithm=hashes.SHA256(),
                    label=None
                )
            )
            
            # Decrypt the data
            temp_fernet = Fernet(decrypted_key)
            return temp_fernet.decrypt(symmetric_encrypted).decode()
            
        except Exception as e:
            logger.error(f"Error decrypting PHI data: {e}")
            raise ValueError("Failed to decrypt PHI data")
    
    def hash_identifier(self, identifier: str, salt: str = None) -> str:
        """Hash sensitive identifiers"""
        if not salt:
            salt = secrets.token_hex(16)
        
        hashed = hashlib.pbkdf2_hmac('sha256', identifier.encode(), salt.encode(), 100000)
        return f"{salt}:{hashed.hex()}"
    
    def generate_api_key(self, user_id: str, permissions: List[str]) -> str:
        """Generate secure API key"""
        # Create payload
        payload = {
            'user_id': user_id,
            'permissions': permissions,
            'created_at': datetime.utcnow().isoformat(),
            'nonce': secrets.token_hex(16)
        }
        
        # Sign with HMAC
        message = f"{user_id}:{','.join(permissions)}:{payload['created_at']}:{payload['nonce']}"
        signature = hmac.new(self.master_key, message.encode(), hashlib.sha256).hexdigest()
        
        # Combine into API key
        api_key = base64.urlsafe_b64encode(f"{message}:{signature}".encode()).decode()
        return api_key
    
    def verify_api_key(self, api_key: str) -> Dict[str, Any]:
        """Verify and decode API key"""
        try:
            # Decode API key
            decoded = base64.urlsafe_b64decode(api_key.encode()).decode()
            parts = decoded.split(':')
            
            if len(parts) != 5:
                raise ValueError("Invalid API key format")
            
            user_id, permissions_str, created_at, nonce, signature = parts
            permissions = permissions_str.split(',') if permissions_str else []
            
            # Recreate message and verify signature
            message = f"{user_id}:{permissions_str}:{created_at}:{nonce}"
            expected_signature = hmac.new(self.master_key, message.encode(), hashlib.sha256).hexdigest()
            
            if not hmac.compare_digest(signature, expected_signature):
                raise ValueError("Invalid API key signature")
            
            return {
                'user_id': user_id,
                'permissions': permissions,
                'created_at': created_at,
                'valid': True
            }
            
        except Exception as e:
            logger.warning(f"API key verification failed: {e}")
            return {'valid': False, 'error': str(e)}
    
    def rotate_keys(self) -> Dict[str, str]:
        """Rotate encryption keys"""
        # Generate new keys
        new_master_key = Fernet.generate_key()
        new_private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048,
        )
        new_public_key = new_private_key.public_key()
        
        # Store old keys for re-encryption
        old_keys = {
            'master_key': self.master_key,
            'private_key': self.private_key,
            'public_key': self.public_key
        }
        
        # Update current keys
        self.master_key = new_master_key
        self.private_key = new_private_key
        self.public_key = new_public_key
        
        # Re-derive symmetric key
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=b'healthcare_ml_salt',
            iterations=100000,
        )
        key = base64.urlsafe_b64encode(kdf.derive(self.master_key))
        self.fernet = Fernet(key)
        
        logger.info("Encryption keys rotated successfully")
        
        return {
            'old_keys': old_keys,
            'new_master_key': new_master_key.hex(),
            'rotation_time': datetime.utcnow().isoformat()
        } 