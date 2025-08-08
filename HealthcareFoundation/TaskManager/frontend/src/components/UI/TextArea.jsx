import React from 'react';

const TextArea = ({ 
  label, 
  error, 
  className = '', 
  ...props 
}) => {
  const textareaClasses = `form-textarea ${error ? 'border-red-300 focus:ring-red-500 focus:border-red-500' : ''} ${className}`;

  return (
    <div className="w-full">
      {label && (
        <label className="block text-sm font-medium text-gray-700 mb-1">
          {label}
        </label>
      )}
      <textarea className={textareaClasses} {...props} />
      {error && (
        <p className="mt-1 text-sm text-red-600">{error}</p>
      )}
    </div>
  );
};

export default TextArea;
