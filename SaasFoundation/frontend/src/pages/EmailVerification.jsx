import React, { useState, useEffect } from 'react';
import { useNavigate, useSearchParams } from 'react-router-dom';
import { Card, Button } from '../components/ui';
import { SuccessMessage, ErrorMessage, LoadingState } from '../components/common';
import { useAuth } from '../hooks/useAuth';

const EmailVerification = () => {
  const navigate = useNavigate();
  const [searchParams] = useSearchParams();
  const { verifyEmail, resendVerificationEmail, user } = useAuth();
  
  const [status, setStatus] = useState('loading'); // loading, success, error, expired
  const [message, setMessage] = useState('');
  const [resending, setResending] = useState(false);
  const [timeLeft, setTimeLeft] = useState(60);
  const [canResend, setCanResend] = useState(false);

  const token = searchParams.get('token');
  const email = searchParams.get('email') || user?.email;

  useEffect(() => {
    if (token) {
      handleVerification();
    } else {
      setStatus('waiting');
    }
  }, [token]);

  // Countdown timer for resend button
  useEffect(() => {
    let interval = null;
    
    if (!canResend && timeLeft > 0) {
      interval = setInterval(() => {
        setTimeLeft(timeLeft => timeLeft - 1);
      }, 1000);
    } else if (timeLeft === 0) {
      setCanResend(true);
    }

    return () => clearInterval(interval);
  }, [canResend, timeLeft]);

  const handleVerification = async () => {
    try {
      setStatus('loading');
      await verifyEmail(token);
      setStatus('success');
      setMessage('Your email has been verified successfully!');
      
      // Redirect to login after 3 seconds
      setTimeout(() => {
        navigate('/login');
      }, 3000);
    } catch (error) {
      setStatus('error');
      if (error.message.includes('expired')) {
        setMessage('This verification link has expired. Please request a new one.');
        setStatus('expired');
      } else if (error.message.includes('invalid')) {
        setMessage('This verification link is invalid. Please request a new one.');
        setStatus('expired');
      } else {
        setMessage('Failed to verify email. Please try again or contact support.');
      }
    }
  };

  const handleResendEmail = async () => {
    try {
      setResending(true);
      await resendVerificationEmail(email);
      setMessage('Verification email sent! Please check your inbox.');
      setCanResend(false);
      setTimeLeft(60);
    } catch (error) {
      setMessage('Failed to resend verification email. Please try again.');
    } finally {
      setResending(false);
    }
  };

  const renderContent = () => {
    switch (status) {
      case 'loading':
        return (
          <div className="text-center">
            <LoadingState />
            <h2 className="text-xl font-semibold text-gray-900 mt-4">
              Verifying your email...
            </h2>
            <p className="text-gray-600 mt-2">
              Please wait while we verify your email address.
            </p>
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
              Email Verified Successfully!
            </h2>
            <p className="text-gray-600 mb-6">
              Your email address has been verified. You'll be redirected to the login page shortly.
            </p>
            <Button onClick={() => navigate('/login')}>
              Go to Login
            </Button>
          </div>
        );

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
              Verification Failed
            </h2>
            <p className="text-gray-600 mb-6">
              We couldn't verify your email address. Please try again.
            </p>
            <div className="space-y-3">
              <Button
                onClick={handleVerification}
                variant="primary"
                className="w-full"
              >
                Try Again
              </Button>
              <Button
                onClick={() => navigate('/login')}
                variant="outline"
                className="w-full"
              >
                Back to Login
              </Button>
            </div>
          </div>
        );

      case 'expired':
        return (
          <div className="text-center">
            <div className="mx-auto flex items-center justify-center h-12 w-12 rounded-full bg-orange-100 mb-4">
              <svg
                className="h-6 w-6 text-orange-600"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth="2"
                  d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"
                />
              </svg>
            </div>
            <h2 className="text-xl font-semibold text-gray-900 mb-2">
              Verification Link Expired
            </h2>
            <p className="text-gray-600 mb-6">
              This verification link has expired or is invalid. Request a new verification email.
            </p>
            <ResendSection
              email={email}
              onResend={handleResendEmail}
              resending={resending}
              canResend={canResend}
              timeLeft={timeLeft}
            />
          </div>
        );

      case 'waiting':
      default:
        return (
          <div className="text-center">
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
                  d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z"
                />
              </svg>
            </div>
            <h2 className="text-xl font-semibold text-gray-900 mb-2">
              Check Your Email
            </h2>
            <p className="text-gray-600 mb-6">
              We've sent a verification link to <strong>{email}</strong>. 
              Click the link in the email to verify your account.
            </p>
            <ResendSection
              email={email}
              onResend={handleResendEmail}
              resending={resending}
              canResend={canResend}
              timeLeft={timeLeft}
            />
          </div>
        );
    }
  };

  return (
    <div className="min-h-screen bg-gray-50 flex flex-col justify-center py-12 sm:px-6 lg:px-8">
      <div className="sm:mx-auto sm:w-full sm:max-w-md">
        <div className="text-center">
          <h1 className="text-3xl font-bold text-gray-900">Email Verification</h1>
        </div>
      </div>

      <div className="mt-8 sm:mx-auto sm:w-full sm:max-w-md">
        <Card className="py-8 px-6">
          {message && (
            <div className="mb-6">
              {status === 'success' ? (
                <SuccessMessage message={message} />
              ) : (
                <ErrorMessage message={message} />
              )}
            </div>
          )}
          
          {renderContent()}
        </Card>

        {/* Help Text */}
        <div className="mt-6 text-center">
          <p className="text-sm text-gray-600">
            Didn't receive the email? Check your spam folder or{' '}
            <button
              onClick={() => navigate('/contact')}
              className="text-blue-600 hover:text-blue-500 underline"
            >
              contact support
            </button>
          </p>
        </div>
      </div>
    </div>
  );
};

// Resend verification email component
const ResendSection = ({ email, onResend, resending, canResend, timeLeft }) => {
  return (
    <div className="space-y-4">
      <div className="text-sm text-gray-600">
        <p>Didn't receive the email?</p>
        {!canResend && (
          <p className="mt-1">
            You can request a new email in {timeLeft} seconds
          </p>
        )}
      </div>
      
      <Button
        onClick={onResend}
        disabled={!canResend || resending}
        loading={resending}
        variant="outline"
        className="w-full"
      >
        {resending ? 'Sending...' : 'Resend Verification Email'}
      </Button>
      
      <div className="text-xs text-gray-500">
        Email will be sent to: {email}
      </div>
    </div>
  );
};

export default EmailVerification;
