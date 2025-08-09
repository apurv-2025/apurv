import React from 'react';
import { CheckCircle, XCircle, AlertTriangle, Info, X } from 'lucide-react';
import { NOTIFICATION_TYPES } from '../../../utils/constants';

const NotificationItem = ({ notification, onRemove }) => {
  const getIcon = () => {
    switch (notification.type) {
      case NOTIFICATION_TYPES.SUCCESS:
        return <CheckCircle className="h-5 w-5 text-green-600" />;
      case NOTIFICATION_TYPES.ERROR:
        return <XCircle className="h-5 w-5 text-red-600" />;
      case NOTIFICATION_TYPES.WARNING:
        return <AlertTriangle className="h-5 w-5 text-yellow-600" />;
      default:
        return <Info className="h-5 w-5 text-blue-600" />;
    }
  };

  const getStyles = () => {
    switch (notification.type) {
      case NOTIFICATION_TYPES.SUCCESS:
        return 'bg-green-50 border-green-200 text-green-800';
      case NOTIFICATION_TYPES.ERROR:
        return 'bg-red-50 border-red-200 text-red-800';
      case NOTIFICATION_TYPES.WARNING:
        return 'bg-yellow-50 border-yellow-200 text-yellow-800';
      default:
        return 'bg-blue-50 border-blue-200 text-blue-800';
    }
  };

  return (
    <div className={`flex items-center p-4 border rounded-lg shadow-lg transition-all ${getStyles()}`}>
      {getIcon()}
      <span className="ml-3 text-sm font-medium flex-1">{notification.message}</span>
      <button
        onClick={() => onRemove(notification.id)}
        className="ml-4 text-gray-400 hover:text-gray-600"
      >
        <X className="h-4 w-4" />
      </button>
    </div>
  );
};

export default NotificationItem;
