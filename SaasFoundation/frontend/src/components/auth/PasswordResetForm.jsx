import React, { useState,useEffect } from 'react';
import { Eye, EyeOff } from 'lucide-react';
import { useAuth } from '../../hooks/useAuth';

function PasswordResetForm() {
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [showPassword, setShowPassword] = useState(false);
  const [showConfirmPassword, setShowConfirmPassword] = useState(false);
  const [securityCodeMethod, setSecurityCodeMethod] = useState('call');
  const [token, setToken] = useState('');

  const [isLoading, setIsLoading] = useState(false);
  const [isSubmitted, setIsSubmitted] = useState(false);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');

  const { resetPassword } = useAuth();

  // Password validation checks
  const hasLowercase = /[a-z]/.test(password);
  const hasUppercase = /[A-Z]/.test(password);
  const hasNumber = /\d/.test(password);
  const hasMinLength = password.length >= 8;

  const requirements = [
    { text: '1 lowercase letter', met: hasLowercase },
    { text: '1 uppercase letter', met: hasUppercase },
    { text: '1 number', met: hasNumber },
    { text: '8 characters minimum', met: hasMinLength }
  ];

  useEffect(() => {
    // Get URL parameters
    const urlParams = new URLSearchParams(window.location.search);
    const tokenFromUrl = urlParams.get('token');
    
    if (tokenFromUrl) {
      setToken(tokenFromUrl);
    }
  }, []);

  const handleSubmit = async () => {
    setError('');

    if (!password.trim()) {
      setError('Password is required');
      return;
    }
    setIsLoading(true);

    try {
      // Simulate API call
      await new Promise(resolve => setTimeout(resolve, 2000));

      const result = await resetPassword(token, password);
      
      if (result.success) {
        setSuccess(result.message);
      } else {
        setError(result.error);
      }
      
      setIsSubmitted(true);
    } catch (err) {
      setError('Something went wrong. Please try again.');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="max-w-md mx-auto p-8 bg-white">
      {/* Header */}
      <div className="text-center mb-8">
        <h1 className="text-3xl font-semibold text-gray-900 mb-4">
          Create a new password
        </h1>
        <p className="text-gray-600 text-lg">
          Enter your new password, then choose how to get your security code.
        </p>
      </div>

      {/* Password Field */}
      <div className="mb-6">
        <label className="block text-gray-700 text-lg font-medium mb-3">
          Password
        </label>
        <div className="relative">
          <input
            type={showPassword ? 'text' : 'password'}
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            className="w-full px-4 py-3 border border-gray-300 rounded-lg text-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent pr-12"
            placeholder=""
          />
          <button
            type="button"
            onClick={() => setShowPassword(!showPassword)}
            className="absolute right-3 top-1/2 transform -translate-y-1/2 text-gray-500 hover:text-gray-700"
          >
            {showPassword ? (
              <EyeOff className="w-5 h-5" />
            ) : (
              <Eye className="w-5 h-5" />
            )}
            <span className="ml-2 text-sm">Show</span>
          </button>
        </div>

        {/* Password Requirements */}
        <div className="mt-4 grid grid-cols-2 gap-3">
          {requirements.map((req, index) => (
            <div key={index} className="flex items-center">
              <div className={`w-2 h-2 rounded-full mr-3 ${
                req.met ? 'bg-blue-500' : 'bg-blue-500'
              }`} />
              <span className={`text-sm ${
                req.met ? 'text-gray-900' : 'text-gray-600'
              }`}>
                {req.text}
              </span>
            </div>
          ))}
        </div>
      </div>

      {/* Confirm Password Field */}
      <div className="mb-8">
        <label className="block text-gray-700 text-lg font-medium mb-3">
          Confirm password
        </label>
        <div className="relative">
          <input
            type={showConfirmPassword ? 'text' : 'password'}
            value={confirmPassword}
            onChange={(e) => setConfirmPassword(e.target.value)}
            className="w-full px-4 py-3 border border-gray-300 rounded-lg text-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent pr-12"
            placeholder=""
          />
          <button
            type="button"
            onClick={() => setShowConfirmPassword(!showConfirmPassword)}
            className="absolute right-3 top-1/2 transform -translate-y-1/2 text-gray-500 hover:text-gray-700"
          >
            {showConfirmPassword ? (
              <EyeOff className="w-5 h-5" />
            ) : (
              <Eye className="w-5 h-5" />
            )}
            <span className="ml-2 text-sm">Show</span>
          </button>
        </div>
      </div>

      <div>
        <button
            type="button"
            onClick={handleSubmit}
            disabled={isLoading}
            className="w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 disabled:opacity-50 disabled:cursor-not-allowed"
              >
                {isLoading ? (
                  <div className="flex items-center">
                    <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white mr-2"></div>
                    Sending reset link...
                  </div>
                ) : (
                  'Reset Password'
            )}
            </button>
        </div>

      {/* Security Code Options */}
      <div className="mb-8 space-y-4">
        <div className="flex items-center">
          <input
            type="radio"
            id="call"
            name="securityCode"
            value="call"
            checked={securityCodeMethod === 'call'}
            onChange={(e) => setSecurityCodeMethod(e.target.value)}
            className="w-4 h-4 text-blue-600 border-gray-300 focus:ring-blue-500"
          />
          <label htmlFor="call" className="ml-3 text-gray-600 text-lg">
            Call (***) ***-1212
          </label>
        </div>
        
        <div className="flex items-center">
          <input
            type="radio"
            id="text"
            name="securityCode"
            value="text"
            checked={securityCodeMethod === 'text'}
            onChange={(e) => setSecurityCodeMethod(e.target.value)}
            className="w-4 h-4 text-blue-600 border-gray-300 focus:ring-blue-500"
          />
          <label htmlFor="text" className="ml-3 text-gray-600 text-lg">
            Text (***) ***-1212
          </label>
        </div>
      </div>

      {/* Help Link */}
      <div className="text-center">
        <span className="text-gray-600">Having trouble? </span>
        <a href="#" className="text-blue-600 hover:text-blue-800 underline">
          Get help
        </a>
      </div>
    </div>
  );
}

export default PasswordResetForm;