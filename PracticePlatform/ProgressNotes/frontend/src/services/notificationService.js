class NotificationService {
  static notifications = [];
  static listeners = [];

  static addNotification(message, type = 'info', duration = 5000, options = {}) {
    const id = Math.random().toString(36).substr(2, 9);
    const notification = {
      id,
      message,
      type,
      duration,
      timestamp: new Date(),
      persistent: options.persistent || false,
      action: options.action || null,
      autoClose: duration > 0 && !options.persistent
    };

    this.notifications = [...this.notifications, notification];
    this.notifyListeners();

    // Auto-remove notification if not persistent
    if (notification.autoClose) {
      setTimeout(() => {
        this.removeNotification(id);
      }, duration);
    }

    return id;
  }

  static removeNotification(id) {
    this.notifications = this.notifications.filter(n => n.id !== id);
    this.notifyListeners();
  }

  static clearAll() {
    this.notifications = [];
    this.notifyListeners();
  }

  static subscribe(listener) {
    this.listeners.push(listener);
    
    // Return unsubscribe function
    return () => {
      this.listeners = this.listeners.filter(l => l !== listener);
    };
  }

  static notifyListeners() {
    this.listeners.forEach(listener => {
      listener(this.notifications);
    });
  }

  static getNotifications() {
    return this.notifications;
  }

  // Convenience methods for different notification types
  static success(message, options = {}) {
    return this.addNotification(message, 'success', 5000, options);
  }

  static error(message, options = {}) {
    return this.addNotification(message, 'error', 8000, {
      ...options,
      persistent: options.persistent !== false // Default to persistent for errors
    });
  }

  static warning(message, options = {}) {
    return this.addNotification(message, 'warning', 6000, options);
  }

  static info(message, options = {}) {
    return this.addNotification(message, 'info', 5000, options);
  }

  // Specific notification methods for common operations
  static noteSaved(noteName) {
    return this.success(`Note "${noteName}" saved successfully`);
  }

  static noteDeleted(noteName) {
    return this.success(`Note "${noteName}" deleted successfully`);
  }

  static noteSigned(noteName) {
    return this.success(`Note "${noteName}" signed successfully`);
  }

  static fileUploaded(fileName) {
    return this.success(`File "${fileName}" uploaded successfully`);
  }

  static fileDeleted(fileName) {
    return this.success(`File "${fileName}" deleted successfully`);
  }

  static operationFailed(operation, reason) {
    return this.error(`${operation} failed: ${reason}`);
  }

  static validationError(message) {
    return this.warning(`Validation Error: ${message}`);
  }

  static networkError() {
    return this.error('Network error. Please check your connection and try again.', {
      action: {
        label: 'Retry',
        handler: () => window.location.reload()
      }
    });
  }

  static permissionDenied(action) {
    return this.error(`Permission denied: You don't have permission to ${action}`);
  }

  static bulkOperationComplete(operation, count) {
    return this.success(`${operation} completed for ${count} item${count !== 1 ? 's' : ''}`);
  }

  static confirmAction(message, onConfirm, onCancel = null) {
    return this.addNotification(message, 'warning', 0, {
      persistent: true,
      action: {
        confirm: {
          label: 'Confirm',
          handler: () => {
            onConfirm();
            this.removeNotification(id);
          }
        },
        cancel: {
          label: 'Cancel',
          handler: () => {
            if (onCancel) onCancel();
            this.removeNotification(id);
          }
        }
      }
    });
  }

  // Progress notifications for long-running operations
  static startProgress(operation) {
    const id = this.addNotification(`${operation} in progress...`, 'info', 0, {
      persistent: true,
      progress: true
    });
    
    return {
      update: (message) => {
        const notification = this.notifications.find(n => n.id === id);
        if (notification) {
          notification.message = message;
          this.notifyListeners();
        }
      },
      complete: (message = null) => {
        this.removeNotification(id);
        if (message) {
          this.success(message);
        }
      },
      error: (message) => {
        this.removeNotification(id);
        this.error(message);
      }
    };
  }

  // System notifications
  static systemMaintenance(message, scheduledTime) {
    return this.warning(`System Maintenance: ${message} scheduled for ${scheduledTime}`, {
      persistent: true,
      action: {
        label: 'Acknowledge',
        handler: (id) => this.removeNotification(id)
      }
    });
  }

  static sessionExpiring(timeLeft) {
    return this.warning(`Your session will expire in ${timeLeft} minutes`, {
      action: {
        label: 'Extend Session',
        handler: () => {
          // Handle session extension
          window.location.reload();
        }
      }
    });
  }

  static sessionExpired() {
    return this.error('Your session has expired. Please log in again.', {
      persistent: true,
      action: {
        label: 'Login',
        handler: () => {
          window.location.href = '/login';
        }
      }
    });
  }
}

export default NotificationService;
