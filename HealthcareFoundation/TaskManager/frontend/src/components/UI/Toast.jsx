// src/components/UI/Toast.jsx
import React, { useEffect } from 'react';
import { X, CheckCircle, AlertCircle, Info, AlertTriangle } from 'lucide-react';

const Toast = ({ toasts = [], onRemove }) => {
  const getToastIcon = (type) => {
    switch (type) {
      case 'success':
        return <CheckCircle className="w-5 h-5 text-green-500" />;
      case 'error':
        return <AlertCircle className="w-5 h-5 text-red-500" />;
      case 'warning':
        return <AlertTriangle className="w-5 h-5 text-yellow-500" />;
      default:
        return <Info className="w-5 h-5 text-blue-500" />;
    }
  };

  const getToastClasses = (type) => {
    const baseClasses = 'flex items-center p-4 rounded-lg shadow-lg border';
    switch (type) {
      case 'success':
        return `${baseClasses} bg-green-50 border-green-200`;
      case 'error':
        return `${baseClasses} bg-red-50 border-red-200`;
      case 'warning':
        return `${baseClasses} bg-yellow-50 border-yellow-200`;
      default:
        return `${baseClasses} bg-blue-50 border-blue-200`;
    }
  };

  if (toasts.length === 0) return null;

  return (
    <div className="fixed top-4 right-4 z-50 space-y-2">
      {toasts.map((toast) => (
        <div key={toast.id} className={getToastClasses(toast.type)}>
          <div className="flex items-center space-x-3">
            {getToastIcon(toast.type)}
            <p className="text-sm font-medium text-gray-900">{toast.message}</p>
            <button
              onClick={() => onRemove(toast.id)}
              className="ml-4 flex-shrink-0 hover:bg-gray-100 rounded p-1"
            >
              <X className="w-4 h-4 text-gray-500" />
            </button>
          </div>
        </div>
      ))}
    </div>
  );
};

export default Toast;
