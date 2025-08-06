import React from 'react';

const LoadingSpinner = ({ size = 'medium', text = null, fullPage = false }) => {
  const sizeClasses = {
    small: 'h-4 w-4',
    medium: 'h-8 w-8',
    large: 'h-12 w-12'
  };

  const containerClasses = fullPage 
    ? 'flex items-center justify-center h-64'
    : 'flex items-center justify-center p-4';

  return (
    <div className={containerClasses}>
      <div className="text-center">
        <div 
          className={`animate-spin rounded-full border-b-2 border-blue-500 ${sizeClasses[size]} mx-auto`}
        />
        {text && (
          <p className="mt-2 text-sm text-gray-600">{text}</p>
        )}
      </div>
    </div>
  );
};

export default LoadingSpinner;
