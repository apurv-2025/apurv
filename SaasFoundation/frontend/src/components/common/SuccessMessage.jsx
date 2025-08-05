import React from 'react';
import { CheckCircleIcon, XMarkIcon } from '@heroicons/react/24/outline';

const SuccessMessage = ({ 
  message, 
  onClose, 
  className = '',
  closable = true,
  icon = true 
}) => {
  if (!message) return null;

  return (
    <div className={`rounded-md bg-green-50 p-4 ${className}`}>
      <div className="flex">
        {icon && (
          <div className="flex-shrink-0">
            <CheckCircleIcon className="h-5 w-5 text-green-400" aria-hidden="true" />
          </div>
        )}
        
        <div className={`${icon ? 'ml-3' : ''} flex-1`}>
          <p className="text-sm font-medium text-green-800">
            {message}
          </p>
        </div>
        
        {closable && onClose && (
          <div className="ml-auto pl-3">
            <div className="-mx-1.5 -my-1.5">
              <button
                type="button"
                onClick={onClose}
                className="inline-flex rounded-md bg-green-50 p-1.5 text-green-500 hover:bg-green-100 focus:outline-none focus:ring-2 focus:ring-green-600 focus:ring-offset-2 focus:ring-offset-green-50"
                aria-label="Dismiss"
              >
                <XMarkIcon className="h-5 w-5" aria-hidden="true" />
              </button>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default SuccessMessage;
