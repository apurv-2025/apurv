// frontend/src/components/EmailVerification.js
import React, { useState, useEffect } from 'react';
import { useSearchParams, Link } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';

function EmailVerification() {
  const [searchParams] = useSearchParams();
  const [status, setStatus] = useState('verifying'); // verifying, success, error
  const [message, setMessage] = useState('');
  const { verifyEmail } = useAuth();

  useEffect(() => {
    const token = searchParams.get('token');
    
    if (!token) {
      setStatus('error');
      setMessage('Invalid verification link. Please check your email for the correct link.');
      return;
    }

    const handleVerification = async () => {
      const result = await verifyEmail(token);
      
      if (result.success) {
        setStatus('success');
        setMessage(result.message);
      } else {
        setStatus('error');
        setMessage(result.error);
      }
    };

    handleVerification();
  }, [searchParams, verifyEmail]);

  return (
    <div className="verification-container">
      <div className="verification-card">
        {status === 'verifying' && (
          <>
            <div className="verification-icon loading">
              <div className="spinner"></div>
            </div>
            <h2>Verifying Your Email</h2>
            <p>Please wait while we verify your email address...</p>
          </>
        )}
        
        {status === 'success' && (
          <>
            <div className="verification-icon success">
              <svg width="64" height="64" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                <path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/>
                <polyline points="22,4 12,14.01 9,11.01"/>
              </svg>
            </div>
            <h2>Email Verified Successfully!</h2>
            <p>{message}</p>
            <p>Your account is now fully activated and you can access all features.</p>
            <div className="verification-actions">
              <Link to="/dashboard" className="btn-primary">
                Go to Dashboard
              </Link>
            </div>
          </>
        )}
        
        {status === 'error' && (
          <>
            <div className="verification-icon error">
              <svg width="64" height="64" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                <circle cx="12" cy="12" r="10"/>
                <line x1="15" y1="9" x2="9" y2="15"/>
                <line x1="9" y1="9" x2="15" y2="15"/>
              </svg>
            </div>
            <h2>Verification Failed</h2>
            <p>{message}</p>
            <div className="verification-actions">
              <Link to="/login" className="btn-primary">
                Go to Login
              </Link>
              <Link to="/register" className="btn-secondary">
                Create New Account
              </Link>
            </div>
          </>
        )}
      </div>
    </div>
  );
}

export default EmailVerification;
