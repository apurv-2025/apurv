// src/components/common/ErrorMessage.jsx
import React from 'react';
import { AlertCircle } from 'lucide-react';

const ErrorMessage = ({ error, onRetry }) => (
  <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded flex items-center">
    <AlertCircle className="h-4 w-4 mr-2" />
    <span className="flex-1">{error}</span>
    {onRetry && (
      <button
        onClick={onRetry}
        className="ml-2 text-red-700 hover:text-red-900 underline"
      >
        Retry
      </button>
    )}
  </div>
);

export default ErrorMessage;
