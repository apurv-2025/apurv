// frontend/src/components/InvitationAccept.js
import React, { useState, useEffect } from 'react';
import { useSearchParams, useNavigate, Link } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';
import api from '../services/api';

function InvitationAccept() {
  const [searchParams] = useSearchParams();
  const navigate = useNavigate();
  const { user, login } = useAuth();
  const [status, setStatus] = useState('loading'); // loading, valid, invalid, accepted, error
  const [invitation, setInvitation] = useState(null);
  const [message, setMessage] = useState('');
  const [showSignup, setShowSignup] = useState(false);
  
  // Signup form for new users
  const [signupForm, setSignupForm] = useState({
    first_name: '',
    last_name: '',
    password: '',
    confirm_password: ''
  });

  useEffect(() => {
    const token = searchParams.get('token');
    
    if (!token) {
      setStatus('invalid');
      setMessage('Invalid invitation link. Please check your email for the correct link.');
      return;
    }

    fetchInvitationDetails(token);
  }, [searchParams]);

  const fetchInvitationDetails = async (token) => {
    try {
      const response = await api.get(`/api/invitations/${token}`);
      setInvitation(response.data);
      setStatus('valid');
      
      // If user is not logged in and doesn't exist, show signup form
      if (!user && !response.data.user_exists) {
        setShowSignup(true);
      }
    } catch (error) {
      setStatus('invalid');
      setMessage(error.response?.data?.detail || 'Invalid or expired invitation');
    }
  };

  const handleAcceptInvitation = async () => {
    if (!user) {
      setMessage('Please log in or create an account to accept this invitation');
      return;
    }

    try {
      const token = searchParams.get('token');
      await api.post(`/api/invitations/${token}/accept`);
      setStatus('accepted');
      setMessage('Invitation accepted successfully! You are now a member of the organization.');
      
      // Redirect to dashboard after a delay
      setTimeout(() => {
        navigate('/dashboard');
      }, 2000);
    } catch (error) {
      setStatus('error');
      setMessage(error.response?.data?.detail || 'Failed to accept invitation');
    }
  };

  const handleSignupAndAccept = async (e) => {
    e.preventDefault();
    
    if (signupForm.password !== signupForm.confirm_password) {
      setMessage('Passwords do not match');
      return;
    }

    try {
      // Create account
      const signupData = {
        email: invitation.email,
        password: signupForm.password,
        first_name: signupForm.first_name,
        last_name: signupForm.last_name
      };
      
      await api.post('/api/auth/register', signupData);
      
      // Login with new account
      const loginResult = await login(invitation.email, signupForm.password);
      
      if (loginResult.success) {
        // Accept invitation
        const token = searchParams.get('token');
        await api.post(`/api/invitations/${token}/accept`);
        
        setStatus('accepted');
        setMessage('Account created and invitation accepted! Welcome to the team!');
        
        // Redirect to dashboard
        setTimeout(() => {
          navigate('/dashboard');
        }, 2000);
      }
    } catch (error) {
      setMessage(error.response?.data?.detail || 'Failed to create account and accept invitation');
    }
  };

  const formatDate = (dateString) => {
    return new Date(dateString).toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'long',
      day: 'numeric'
    });
  };

  return (
    <div className="invitation-container">
      <div className="invitation-card">
        {status === 'loading' && (
          <>
            <div className="invitation-icon loading">
              <div className="spinner"></div>
            </div>
            <h2>Loading Invitation</h2>
            <p>Please wait while we verify your invitation...</p>
          </>
        )}
        
        {status === 'valid' && invitation && (
          <>
            <div className="invitation-icon valid">
              <svg width="64" height="64" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                <path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"/>
                <circle cx="9" cy="7" r="4"/>
                <path d="M22 21v-2a4 4 0 0 0-3-3.87"/>
                <path d="M16 3.13a4 4 0 0 1 0 7.75"/>
              </svg>
            </div>
            <h2>You're Invited!</h2>
            <div className="invitation-details">
              <p>
                <strong>{invitation.invited_by.first_name} {invitation.invited_by.last_name}</strong> 
                {' '}has invited you to join
              </p>
              <h3>{invitation.organization.name}</h3>
              <div className="invitation-meta">
                <div className="meta-item">
                  <span className="meta-label">Role:</span>
                  <span className={`role-badge role-${invitation.role}`}>
                    {invitation.role.toUpperCase()}
                  </span>
                </div>
                <div className="meta-item">
                  <span className="meta-label">Invited:</span>
                  <span>{formatDate(invitation.created_at)}</span>
                </div>
                <div className="meta-item">
                  <span className="meta-label">Expires:</span>
                  <span>{formatDate(invitation.expires_at)}</span>
                </div>
              </div>
            </div>

            {message && (
              <div className="invitation-message">
                {message}
              </div>
            )}

            {!user && showSignup ? (
              <div className="signup-section">
                <h4>Create Your Account</h4>
                <p>Complete your profile to join {invitation.organization.name}</p>
                
                <form onSubmit={handleSignupAndAccept} className="signup-form">
                  <div className="form-row">
                    <div className="form-group">
                      <label>First Name</label>
                      <input
                        type="text"
                        value={signupForm.first_name}
                        onChange={(e) => setSignupForm(prev => ({
                          ...prev,
                          first_name: e.target.value
                        }))}
                        className="form-input"
                        required
                      />
                    </div>
                    <div className="form-group">
                      <label>Last Name</label>
                      <input
                        type="text"
                        value={signupForm.last_name}
                        onChange={(e) => setSignupForm(prev => ({
                          ...prev,
                          last_name: e.target.value
                        }))}
                        className="form-input"
                        required
                      />
                    </div>
                  </div>
                  
                  <div className="form-group">
                    <label>Email</label>
                    <input
                      type="email"
                      value={invitation.email}
                      className="form-input"
                      disabled
                    />
                  </div>
                  
                  <div className="form-group">
                    <label>Password</label>
                    <input
                      type="password"
                      value={signupForm.password}
                      onChange={(e) => setSignupForm(prev => ({
                        ...prev,
                        password: e.target.value
                      }))}
                      className="form-input"
                      required
                      minLength="8"
                    />
                  </div>
                  
                  <div className="form-group">
                    <label>Confirm Password</label>
                    <input
                      type="password"
                      value={signupForm.confirm_password}
                      onChange={(e) => setSignupForm(prev => ({
                        ...prev,
                        confirm_password: e.target.value
                      }))}
                      className="form-input"
                      required
                    />
                  </div>
                  
                  <button type="submit" className="btn-primary btn-full">
                    Create Account & Join Team
                  </button>
                </form>
              </div>
            ) : !user ? (
              <div className="login-section">
                <p>You already have an account with this email.</p>
                <div className="invitation-actions">
                  <Link to="/login" className="btn-primary">
                    Log In to Accept
                  </Link>
                  <Link to="/register" className="btn-secondary">
                    Create New Account
                  </Link>
                </div>
              </div>
            ) : (
              <div className="accept-section">
                <p>Ready to join {invitation.organization.name}?</p>
                <button 
                  onClick={handleAcceptInvitation}
                  className="btn-primary btn-full"
                >
                  Accept Invitation
                </button>
              </div>
            )}
          </>
        )}
        
        {status === 'accepted' && (
          <>
            <div className="invitation-icon success">
              <svg width="64" height="64" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                <path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/>
                <polyline points="22,4 12,14.01 9,11.01"/>
              </svg>
            </div>
            <h2>Welcome to the Team!</h2>
            <p>{message}</p>
            <div className="invitation-actions">
              <Link to="/dashboard" className="btn-primary">
                Go to Dashboard
              </Link>
            </div>
          </>
        )}
        
        {(status === 'invalid' || status === 'error') && (
          <>
            <div className="invitation-icon error">
              <svg width="64" height="64" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                <circle cx="12" cy="12" r="10"/>
                <line x1="15" y1="9" x2="9" y2="15"/>
                <line x1="9" y1="9" x2="15" y2="15"/>
              </svg>
            </div>
            <h2>Invitation Invalid</h2>
            <p>{message}</p>
            <div className="invitation-actions">
              <Link to="/login" className="btn-primary">
                Go to Login
              </Link>
              <Link to="/register" className="btn-secondary">
                Create Account
              </Link>
            </div>
          </>
        )}
      </div>
    </div>
  );
}

export default InvitationAccept;
