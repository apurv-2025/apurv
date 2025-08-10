// File: src/components/notifications/NotificationItem.js - Individual Notification
import React from 'react';
import { CheckCircle, XCircle, AlertTriangle, Info, X } from 'lucide-react';
import { useNotification } from '../../contexts/NotificationContext';

const NotificationItem = ({ notification }) => {
  const { removeNotification } = useNotification();

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

  const { icon: Icon, className, iconClassName } = types[notification.type];

  return (
    <div className={`flex items-center p-4 rounded-lg shadow-lg max-w-sm slide-in ${className}`}>
      <Icon className={`h-5 w-5 mr-3 ${iconClassName}`} />
      <span className="flex-1 text-sm font-medium">{notification.message}</span>
      <button
        onClick={() => removeNotification(notification.id)}
        className="ml-3 hover:opacity-75"
      >
        <X className="h-4 w-4" />
      </button>
    </div>
  );
};

export default NotificationItem;
