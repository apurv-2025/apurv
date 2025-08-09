import React, { createContext, useContext } from 'react';
import { useNotifications } from '../../../hooks/useNotifications';
import NotificationContainer from './NotificationContainer';

const NotificationContext = createContext(null);

export const useNotificationContext = () => {
  const context = useContext(NotificationContext);
  if (!context) {
    throw new Error('useNotificationContext must be used within NotificationProvider');
  }
  return context;
};

export const NotificationProvider = ({ children }) => {
  const notificationMethods = useNotifications();

  return (
    <NotificationContext.Provider value={notificationMethods}>
      {children}
      <NotificationContainer
        notifications={notificationMethods.notifications}
        onRemove={notificationMethods.removeNotification}
      />
    </NotificationContext.Provider>
  );
};
