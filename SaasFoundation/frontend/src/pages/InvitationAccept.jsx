import React, { useState, useEffect } from 'react';
import { useNavigate, useSearchParams, Link } from 'react-router-dom';
import { Card, Button, Input, Badge } from '../components/ui';
import { SuccessMessage, ErrorMessage, LoadingState } from '../components/common';
import { useAuth } from '../hooks/useAuth';
import { API_ENDPOINTS } from '../utils/constants';

const InvitationAccept = () => {
  const navigate = useNavigate();
  const [searchParams] = useSearchParams();
  const { user, acceptInvitation, register } = useAuth();
  
  const [invitation, setInvitation] = useState(null);
  const [status, setStatus] = useState('loading'); // loading, valid, expired, invalid, accepted, error
  const [accepting, setAccepting] = useState(false);
  const [message, setMessage] = useState('');
  const [showRegistration, setShowRegistration] = useState(false);

  // Registration form state
  const [registrationData, setRegistrationData] = useState({
    firstName: '',
    lastName: '',
    password: '',
    confirmPassword: ''
  });

  const token = searchParams.get('token');
  const inviteId = searchParams.get('invite');

  useEffect(() => {
    if (token || inviteId) {
      validateInvitation();
    } else {
      setStatus('invalid');
      setMessage('Invalid invitation link. Please check the URL.');
    }
  }, [token, inviteId]);

  const validateInvitation = async () => {
    try {
      setStatus('loading');
      
      // Mock API call to validate invitation
      const response = await fetch(`/api/v1/invitations/validate`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ token, inviteId })
      });
      
      if (!response.ok) {
        throw new Error('Failed to validate invitation');
      }
      
      const invitationData = await response.json();
      setInvitation(invitationData);
      
      if (invitationData.expired) {
        setStatus('expired');
        setMessage('This invitation has expired. Please contact the team administrator for a new invitation.');
      } else if (invitationData.accepted) {
        setStatus('accepted');
        setMessage('This invitation has already been accepted.');
      } else {
        setStatus('valid');
        
        // Check if user exists or needs to register
        if (!user && !invitationData.userExists) {
          setShowRegistration(true);
          setRegistrationData(prev => ({
            ...prev,
            email: invitationData.email
          }));
        }
      }
    } catch (error) {
      setStatus('error');
      setMessage('Failed to validate invitation. Please try again or contact support.');
    }
  };

  const handleAcceptInvitation = async () => {
    try {
      setAccepting(true);
      setMessage('');
      
      await acceptInvitation({ token, inviteId });
      
      setStatus('success');
      setMessage('Successfully joined the team! Redirecting to dashboard...');
      
      setTimeout(() => {
        navigate('/dashboard');
      }, 2000);
    } catch (error) {
      setMessage('Failed to accept invitation. Please try again.');
    } finally {
      setAccepting(false);
    }
  };

  const handleRegistrationAndAccept = async (e) => {
    e.preventDefault();
    
    if (registrationData.password !== registrationData.confirmPassword) {
      setMessage('Passwords do not match.');
      return;
    }

    try {
      setAccepting(true);
      setMessage('');
      
      // Register user and accept invitation in one step
      await register({
        ...registrationData,
        email: invitation.email,
        acceptInvitation: { token, inviteId }
      });
      
      setStatus('success');
      setMessage('Account created and team invitation accepted! Redirecting to dashboard...');
      
      setTimeout(() => {
        navigate('/dashboard');
      }, 2000);
    } catch (error) {
      setMessage('Failed to create account or accept invitation. Please try again.');
    } finally {
      setAccepting(false);
    }
  };

  const getRoleColor = (role) => {
    switch (role) {
      case 'admin':
        return 'bg-purple-100 text-purple-800';
      case 'member':
        return 'bg-blue-100 text-blue-800';
      case 'viewer':
        return 'bg-gray-100 text-gray-800';
      default:
        return 'bg-gray-100 text-gray-800';
    }
  };

  const renderContent = () => {
    switch (status) {
      case 'loading':
        return (
          <div className="text-center">
            <LoadingState />
            <h2 className="text-xl font-semibold text-gray-900 mt-4">
              Validating invitation...
            </h2>
            <p className="text-gray-600 mt-2">
              Please wait while we verify your invitation.
            </p>
          </div>
        );

      case 'valid':
        return (
          <div>
            {/* Invitation Details */}
            <div className="text-center mb-8">
              <div className="mx-auto flex items-center justify-center h-12 w-12 rounded-full bg-blue-100 mb-4">
                <svg
                  className="h-6 w-6 text-blue-600"
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth="2"
                    d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z"
                  />
                </svg>
              </div>
              
              <h2 className="text-xl font-semibold text-gray-900 mb-2">
                You're invited to join a team!
              </h2>
              
              <div className="bg-gray-50 rounded-lg p-4 mt-4">
                <div className="space-y-2">
                  <div className="flex justify-between items-center">
                    <span className="text-sm text-gray-600">Team:</span>
                    <span className="font-medium">{invitation?.teamName}</span>
                  </div>
                  <div className="flex justify-between items-center">
                    <span className="text-sm text-gray-600">Invited by:</span>
                    <span className="font-medium">{invitation?.inviterName}</span>
                  </div>
                  <div className="flex justify-between items-center">
                    <span className="text-sm text-gray-600">Role:</span>
                    <Badge className={getRoleColor(invitation?.role)}>
                      {invitation?.role}
                    </Badge>
                  </div>
                  <div className="flex justify-between items-center">
                    <span className="text-sm text-gray-600">Email:</span>
                    <span className="font-medium">{invitation?.email}</span>
                  </div>
                </div>
              </div>
            </div>

            {/* Registration Form or Accept Button */}
            {showRegistration ? (
              <form onSubmit={handleRegistrationAndAccept} className="space-y-4">
                <div className="text-center mb-6">
                  <h3 className="text-lg font-medium text-gray-900">
                    Create your account to join the team
                  </h3>
                  <p className="text-sm text-gray-600 mt-1">
                    You'll need to create an account to accept this invitation
                  </p>
                </div>
                
                <div className="grid grid-cols-2 gap-4">
                  <Input
                    label="First Name"
                    value={registrationData.firstName}
                    onChange={(e) => setRegistrationData(prev => ({
                      ...prev,
                      firstName: e.target.value
                    }))}
                    required
                  />
                  <Input
                    label="Last Name"
                    value={registrationData.lastName}
                    onChange={(e) => setRegistrationData(prev => ({
                      ...prev,
                      lastName: e.target.value
                    }))}
                    required
                  />
                </div>
                
                <Input
                  label="Email"
                  type="email"
                  value={invitation?.email}
                  disabled
                  className="bg-gray-50"
                />
                
                <Input
                  label="Password"
                  type="password"
                  value={registrationData.password}
                  onChange={(e) => setRegistrationData(prev => ({
                    ...prev,
                    password: e.target.value
                  }))}
                  required
                />
                
                <Input
                  label="Confirm Password"
                  type="password"
                  value={registrationData.confirmPassword}
                  onChange={(e) => setRegistrationData(prev => ({
                    ...prev,
                    confirmPassword: e.target.value
                  }))}
                  required
                />
                
                <Button
                  type="submit"
                  loading={accepting}
                  className="w-full"
                >
                  Create Account & Join Team
                </Button>
              </form>
            ) : (
              <div className="space-y-4">
                {user ? (
                  <div className="bg-green-50 p-4 rounded-lg mb-4">
                    <p className="text-sm text-green-800">
                      You're signed in as <strong>{user.email}</strong>
                    </p>
                  </div>
                ) : (
                  <div className="bg-blue-50 p-4 rounded-lg mb-4">
                    <p className="text-sm text-blue-800">
                      You'll need to sign in to accept this invitation.
                    </p>
                  </div>
                )}
                
                <Button
                  onClick={user ? handleAcceptInvitation : () => navigate(`/login?redirect=${encodeURIComponent(window.location.pathname + window.location.search)}`)}
                  loading={accepting}
                  className="w-full"
                >
                  {user ? 'Accept Invitation' : 'Sign In to Accept'}
                </Button>
                
                {!user && (
                  <div className="text-center">
                    <p className="text-sm text-gray-600">
                      Don't have an account?{' '}
                      <button
                        onClick={() => setShowRegistration(true)}
                        className="text-blue-600 hover:text-blue-500 underline"
                      >
                        Create one now
                      </button>
                    </p>
                  </div>
                )}
              </div>
            )}
          </div>
        );

      case 'expired':
      case 'accepted':
      case 'invalid':
      case 'error':
        return (
          <div className="text-center">
            <div className="mx-auto flex items-center justify-center h-12 w-12 rounded-full bg-red-100 mb-4">
              <svg
                className="h-6 w-6 text-red-600"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth="2"
                  d="M6 18L18 6M6 6l12 12"
                />
              </svg>
            </div>
            
            <h2 className="text-xl font-semibold text-gray-900 mb-2">
              {status === 'expired' && 'Invitation Expired'}
              {status === 'accepted' && 'Invitation Already Used'}
              {status === 'invalid' && 'Invalid Invitation'}
              {status === 'error' && 'Something Went Wrong'}
            </h2>
            
            <p className="text-gray-600 mb-6">
              {message}
            </p>
            
            <div className="space-y-3">
              <Button
                onClick={() => navigate('/login')}
                className="w-full"
              >
                Go to Login
              </Button>
              <Link
                to="/contact"
                className="block text-sm text-blue-600 hover:text-blue-500 underline"
              >
                Contact Support
              </Link>
            </div>
          </div>
        );

      case 'success':
        return (
          <div className="text-center">
            <div className="mx-auto flex items-center justify-center h-12 w-12 rounded-full bg-green-100 mb-4">
              <svg
                className="h-6 w-6 text-green-600"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth="2"
                  d="M5 13l4 4L19 7"
                />
              </svg>
            </div>
            
            <h2 className="text-xl font-semibold text-gray-900 mb-2">
              Welcome to the Team!
            </h2>
            
            <p className="text-gray-600 mb-6">
              You've successfully joined <strong>{invitation?.teamName}</strong>. 
              You'll be redirected to your dashboard shortly.
            </p>
            
            <Button onClick={() => navigate('/dashboard')}>
              Go to Dashboard
            </Button>
          </div>
        );

      default:
        return null;
    }
  };

  return (
    <div className="min-h-screen bg-gray-50 flex flex-col justify-center py-12 sm:px-6 lg:px-8">
      <div className="sm:mx-auto sm:w-full sm:max-w-md">
        <div className="text-center">
          <h1 className="text-3xl font-bold text-gray-900">Team Invitation</h1>
        </div>
      </div>

      <div className="mt-8 sm:mx-auto sm:w-full sm:max-w-md">
        <Card className="py-8 px-6">
          {message && status !== 'success' && (
            <div className="mb-6">
              <ErrorMessage message={message} />
            </div>
          )}
          
          {message && status === 'success' && (
            <div className="mb-6">
              <SuccessMessage message={message} />
            </div>
          )}
          
          {renderContent()}
        </Card>

        {/* Help Text */}
        <div className="mt-6 text-center">
          <p className="text-sm text-gray-600">
            Having trouble?{' '}
            <Link
              to="/contact"
              className="text-blue-600 hover:text-blue-500 underline"
            >
              Contact support
            </Link>
          </p>
        </div>
      </div>
    </div>
  );
};

export default InvitationAccept;
