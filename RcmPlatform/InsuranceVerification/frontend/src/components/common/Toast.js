// File: src/components/common/Toast.js
import React, { useEffect } from 'react';
import { CheckCircle, XCircle, AlertTriangle, Info, X } from 'lucide-react';

const Toast = ({ message, type = 'info', onClose, duration = 5000 }) => {
  useEffect(() => {
    if (duration > 0) {
      const timer = setTimeout(onClose, duration);
      return () => clearTimeout(timer);
    }
  }, [duration, onClose]);

  const types = {
    success: {
      icon: CheckCircle,
      className: 'bg-green-500 text-white',
      iconClassName: 'text-white'
    },
    error: {
      icon: XCircle,
      className: 'bg-red-500 text-white',
      iconClassName: 'text-white'
    },
    warning: {
      icon: AlertTriangle,
      className: 'bg-yellow-500 text-white',
      iconClassName: 'text-white'
    },
    info: {
      icon: Info,
      className: 'bg-blue-500 text-white',
      iconClassName: 'text-white'
    }
  };

  const { icon: Icon, className, iconClassName } = types[type];

  return (
    <div className={`flex items-center p-4 rounded-lg shadow-lg max-w-sm ${className}`}>
      <Icon className={`h-5 w-5 mr-3 ${iconClassName}`} />
      <span className="flex-1 text-sm font-medium">{message}</span>
      <button
        onClick={onClose}
        className="ml-3 hover:opacity-75"
      >
        <X className="h-4 w-4" />
      </button>
    </div>
  );
};

export default Toast;
