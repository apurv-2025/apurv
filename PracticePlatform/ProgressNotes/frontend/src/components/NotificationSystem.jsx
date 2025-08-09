import React from 'react';
import { 
  CheckCircle, 
  XCircle, 
  AlertTriangle, 
  Info, 
  X,
  Clock
} from 'lucide-react';

const NotificationSystem = ({ notifications = [] }) => {
  const getNotificationIcon = (type) => {
    switch (type) {
      case 'success':
        return <CheckCircle className="h-5 w-5 text-green-600" />;
      case 'error':
        return <XCircle className="h-5 w-5 text-red-600" />;
      case 'warning':
        return <AlertTriangle className="h-5 w-5 text-yellow-600" />;
      case 'info':
      default:
        return <Info className="h-5 w-5 text-blue-600" />;
    }
  };

  const getNotificationStyles = (type) => {
    switch (type) {
      case 'success':
        return 'bg-green-50 border-green-200 text-green-800';
      case 'error':
        return 'bg-red-50 border-red-200 text-red-800';
      case 'warning':
        return 'bg-yellow-50 border-yellow-200 text-yellow-800';
      case 'info':
      default:
        return 'bg-blue-50 border-blue-200 text-blue-800';
    }
  };

  const getActionButtonStyles = (type) => {
    switch (type) {
      case 'success':
        return 'bg-green-600 hover:bg-green-700 text-white';
      case 'error':
        return 'bg-red-600 hover:bg-red-700 text-white';
      case 'warning':
        return 'bg-yellow-600 hover:bg-yellow-700 text-white';
      case 'info':
      default:
        return 'bg-blue-600 hover:bg-blue-700 text-white';
    }
  };

  const removeNotification = (id) => {
    // This would typically call the notification service
    console.log('Remove notification:', id);
  };

  if (notifications.length === 0) {
    return null;
  }

  return (
    <div className="fixed top-4 right-4 z-50 space-y-3 max-w-sm w-full">
      {notifications.map((notification) => (
        <div
          key={notification.id}
          className={`flex items-start p-4 border rounded-lg shadow-lg transition-all duration-300 transform ${getNotificationStyles(notification.type)}`}
          style={{
            animation: 'slideInRight 0.3s ease-out'
          }}
        >
          <div className="flex-shrink-0">
            {getNotificationIcon(notification.type)}
          </div>
          
          <div className="ml-3 flex-1">
            <div className="text-sm font-medium">
              {notification.message}
            </div>
            
            {notification.timestamp && (
              <div className="mt-1 flex items-center text-xs opacity-75">
                <Clock className="h-3 w-3 mr-1" />
                {new Date(notification.timestamp).toLocaleTimeString()}
              </div>
            )}
            
            {/* Progress indicator for progress notifications */}
            {notification.progress && (
              <div className="mt-2">
                <div className="w-full bg-gray-200 rounded-full h-2">
                  <div 
                    className="bg-current h-2 rounded-full transition-all duration-300"
                    style={{ width: '100%' }}
                  >
                    <div className="h-full bg-current rounded-full animate-pulse"></div>
                  </div>
                </div>
              </div>
            )}
            
            {/* Action buttons */}
            {notification.action && (
              <div className="mt-3 flex space-x-2">
                {notification.action.confirm && (
                  <button
                    onClick={() => notification.action.confirm.handler(notification.id)}
                    className={`px-3 py-1 text-xs font-medium rounded transition-colors ${getActionButtonStyles(notification.type)}`}
                  >
                    {notification.action.confirm.label}
                  </button>
                )}
                
                {notification.action.cancel && (
                  <button
                    onClick={() => notification.action.cancel.handler(notification.id)}
                    className="px-3 py-1 text-xs font-medium text-gray-600 bg-gray-100 hover:bg-gray-200 rounded transition-colors"
                  >
                    {notification.action.cancel.label}
                  </button>
                )}
                
                {notification.action.label && notification.action.handler && (
                  <button
                    onClick={() => notification.action.handler(notification.id)}
                    className={`px-3 py-1 text-xs font-medium rounded transition-colors ${getActionButtonStyles(notification.type)}`}
                  >
                    {notification.action.label}
                  </button>
                )}
              </div>
            )}
          </div>
          
          {/* Close button */}
          <button
            onClick={() => removeNotification(notification.id)}
            className="ml-4 flex-shrink-0 text-gray-400 hover:text-gray-600 transition-colors"
          >
            <X className="h-4 w-4" />
          </button>
        </div>
      ))}
      
      <style jsx>{`
        @keyframes slideInRight {
          from {
            transform: translateX(100%);
            opacity: 0;
          }
          to {
            transform: translateX(0);
            opacity: 1;
          }
        }
      `}</style>
    </div>
  );
};

export default NotificationSystem;
