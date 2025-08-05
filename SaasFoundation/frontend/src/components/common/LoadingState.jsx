import React from 'react';

const LoadingState = ({ 
  message = 'Loading...', 
  size = 'medium',
  className = '',
  showMessage = true,
  variant = 'default'
}) => {
  const getContainerClasses = () => {
    const baseClasses = 'flex flex-col items-center justify-center';
    
    switch (variant) {
      case 'overlay':
        return `${baseClasses} fixed inset-0 bg-white bg-opacity-75 z-50`;
      case 'card':
        return `${baseClasses} bg-white rounded-lg shadow p-8`;
      case 'inline':
        return `${baseClasses} py-4`;
      default:
        return `${baseClasses} py-8`;
    }
  };

  const getSpinnerSize = () => {
    switch (size) {
      case 'small':
        return 'w-4 h-4';
      case 'large':
        return 'w-8 h-8';
      case 'xl':
        return 'w-12 h-12';
      default:
        return 'w-6 h-6';
    }
  };

  const getMessageClasses = () => {
    switch (size) {
      case 'small':
        return 'text-xs text-gray-500 mt-1';
      case 'large':
        return 'text-base text-gray-600 mt-3';
      case 'xl':
        return 'text-lg text-gray-600 mt-4';
      default:
        return 'text-sm text-gray-600 mt-2';
    }
  };

  return (
    <div className={`${getContainerClasses()} ${className}`}>
      {/* Custom Spinner */}
      <div className={`${getSpinnerSize()} animate-spin`}>
        <svg
          className="w-full h-full text-blue-600"
          fill="none"
          viewBox="0 0 24 24"
        >
          <circle
            className="opacity-25"
            cx="12"
            cy="12"
            r="10"
            stroke="currentColor"
            strokeWidth="4"
          />
          <path
            className="opacity-75"
            fill="currentColor"
            d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
          />
        </svg>
      </div>
      
      {showMessage && message && (
        <p className={getMessageClasses()}>
          {message}
        </p>
      )}
    </div>
  );
};

// Preset loading states for common scenarios
export const LoadingStates = {
  // Page loading
  page: {
    message: 'Loading page...',
    size: 'large',
    variant: 'default'
  },
  
  // Data fetching
  data: {
    message: 'Fetching data...',
    size: 'medium',
    variant: 'inline'
  },
  
  // Form submission
  saving: {
    message: 'Saving changes...',
    size: 'small',
    variant: 'inline'
  },
  
  // File upload
  uploading: {
    message: 'Uploading file...',
    size: 'medium',
    variant: 'card'
  },
  
  // Authentication
  authenticating: {
    message: 'Signing you in...',
    size: 'large',
    variant: 'default'
  },
  
  // Processing
  processing: {
    message: 'Processing request...',
    size: 'medium',
    variant: 'overlay'
  }
};

export default LoadingState;
