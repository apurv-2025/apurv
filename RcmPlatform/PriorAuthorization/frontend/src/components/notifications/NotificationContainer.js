// File: src/components/notifications/NotificationContainer.js - Notification System
import React from 'react';
import { useNotification } from '../../contexts/NotificationContext';
import NotificationItem from './NotificationItem';

const NotificationContainer = () => {
  const { notifications } = useNotification();

  if (notifications.length === 0) return null;

  return (
    <div className="fixed top-4 right-4 z-50 space-y-2">
      {notifications.map(notification => (
        <NotificationItem
          key={notification.id}
          notification={notification}
        />
      ))}
    </div>
  );
};

export default NotificationContainer;
