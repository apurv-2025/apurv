// src/hooks/useNotifications.js
import { useState, useEffect } from 'react';
import NotificationService from '../services/notificationService';

export const useNotifications = () => {
  const [notifications, setNotifications] = useState([]);

  useEffect(() => {
    // Subscribe to notification updates
    const unsubscribe = NotificationService.subscribe((updatedNotifications) => {
      setNotifications(updatedNotifications);
    });

    // Get initial notifications
    setNotifications(NotificationService.getNotifications());

    // Cleanup subscription on unmount
    return unsubscribe;
  }, []);

  const addNotification = (message, type = 'info', duration = 5000, options = {}) => {
    return NotificationService.addNotification(message, type, duration, options);
  };

  const removeNotification = (id) => {
    NotificationService.removeNotification(id);
  };

  const clearAllNotifications = () => {
    NotificationService.clearAll();
  };

  // Convenience methods
  const showSuccess = (message, options = {}) => {
    return NotificationService.success(message, options);
  };

  const showError = (message, options = {}) => {
    return NotificationService.error(message, options);
  };

  const showWarning = (message, options = {}) => {
    return NotificationService.warning(message, options);
  };

  const showInfo = (message, options = {}) => {
    return NotificationService.info(message, options);
  };

  const showProgress = (operation) => {
    return NotificationService.startProgress(operation);
  };

  const confirmAction = (message, onConfirm, onCancel) => {
    return NotificationService.confirmAction(message, onConfirm, onCancel);
  };

  return {
    notifications,
    addNotification,
    removeNotification,
    clearAllNotifications,
    showSuccess,
    showError,
    showWarning,
    showInfo,
    showProgress,
    confirmAction
  };
};

export default useNotifications;
