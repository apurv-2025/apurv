import React, { useState, useMemo, useEffect, useCallback } from 'react';
import { Bell, Check, X, AlertCircle, Info, CheckCircle, XCircle, Settings, Filter, Search, RefreshCw, Loader } from 'lucide-react';

// NotificationService class - inline for demo
class NotificationService {
  constructor(baseURL = '/api') {
    this.baseURL = baseURL;
  }

  async apiCall(endpoint, options = {}) {
    const url = `${this.baseURL}${endpoint}`;
    const config = {
      headers: {
        'Content-Type': 'application/json',
        ...options.headers,
      },
      ...options,
    };

    try {
      const response = await fetch(url, config);
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      
      const data = await response.json();
      return data;
    } catch (error) {
      console.error(`API call failed for ${endpoint}:`, error);
      throw error;
    }
  }

  async getNotifications(filters = {}) {
    const queryParams = new URLSearchParams();
    
    if (filters.category && filters.category !== 'all') {
      queryParams.append('category', filters.category);
    }
    if (filters.read !== undefined) {
      queryParams.append('read', filters.read);
    }
    if (filters.search) {
      queryParams.append('search', filters.search);
    }

    const endpoint = `/notifications${queryParams.toString() ? `?${queryParams.toString()}` : ''}`;
    return this.apiCall(endpoint);
  }

  async markAsRead(notificationId) {
    return this.apiCall(`/notifications/${notificationId}/read`, {
      method: 'PATCH',
      body: JSON.stringify({ read: true }),
    });
  }

  async markAllAsRead() {
    return this.apiCall('/notifications/read-all', {
      method: 'PATCH',
    });
  }

  async deleteNotification(notificationId) {
    return this.apiCall(`/notifications/${notificationId}`, {
      method: 'DELETE',
    });
  }

  async getPreferences() {
    return this.apiCall('/notifications/preferences');
  }

  async updatePreferences(preferences) {
    return this.apiCall('/notifications/preferences', {
      method: 'PUT',
      body: JSON.stringify(preferences),
    });
  }

  async getUnreadCount() {
    return this.apiCall('/notifications/unread-count');
  }
}

const notificationService = new NotificationService();

// Custom hooks - inline for demo
const useNotifications = (initialFilters = {}) => {
  const [notifications, setNotifications] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [filters, setFilters] = useState(initialFilters);
  const [unreadCount, setUnreadCount] = useState(0);

  // Mock data for demo - replace with actual API calls
  const mockNotifications = [
    {
      id: 1,
      title: "Payment Successful",
      message: "Your subscription has been renewed for $29.99",
      type: "success",
      timestamp: new Date(Date.now() - 1000 * 60 * 5),
      read: false,
      category: "billing"
    },
    {
      id: 2,
      title: "New Team Member",
      message: "John Doe has joined your workspace",
      type: "info",
      timestamp: new Date(Date.now() - 1000 * 60 * 30),
      read: false,
      category: "team"
    },
    {
      id: 3,
      title: "Storage Limit Warning",
      message: "You're using 85% of your storage space",
      type: "warning",
      timestamp: new Date(Date.now() - 1000 * 60 * 60 * 2),
      read: true,
      category: "system"
    },
    {
      id: 4,
      title: "Security Alert",
      message: "New login from unknown device detected",
      type: "error",
      timestamp: new Date(Date.now() - 1000 * 60 * 60 * 24),
      read: false,
      category: "security"
    }
  ];

  const fetchNotifications = useCallback(async () => {
    try {
      setLoading(true);
      setError(null);
      
      // For demo purposes, use mock data
      // In real app, uncomment this:
      // const data = await notificationService.getNotifications(filters);
      // setNotifications(data.notifications || data);
      
      // Mock API delay
      await new Promise(resolve => setTimeout(resolve, 500));
      setNotifications(mockNotifications);
      setUnreadCount(mockNotifications.filter(n => !n.read).length);
    } catch (err) {
      setError(err.message);
      console.error('Failed to fetch notifications:', err);
    } finally {
      setLoading(false);
    }
  }, [filters]);

  const markAsRead = useCallback(async (notificationId) => {
    try {
      // In real app, uncomment this:
      // await notificationService.markAsRead(notificationId);
      
      setNotifications(prev => 
        prev.map(n => n.id === notificationId ? { ...n, read: true } : n)
      );
      setUnreadCount(prev => Math.max(0, prev - 1));
    } catch (err) {
      setError(err.message);
      console.error('Failed to mark notification as read:', err);
    }
  }, []);

  const markAllAsRead = useCallback(async () => {
    try {
      // In real app, uncomment this:
      // await notificationService.markAllAsRead();
      
      setNotifications(prev => prev.map(n => ({ ...n, read: true })));
      setUnreadCount(0);
    } catch (err) {
      setError(err.message);
      console.error('Failed to mark all notifications as read:', err);
    }
  }, []);

  const deleteNotification = useCallback(async (notificationId) => {
    try {
      // In real app, uncomment this:
      // await notificationService.deleteNotification(notificationId);
      
      const wasUnread = notifications.find(n => n.id === notificationId && !n.read);
      setNotifications(prev => prev.filter(n => n.id !== notificationId));
      
      if (wasUnread) {
        setUnreadCount(prev => Math.max(0, prev - 1));
      }
    } catch (err) {
      setError(err.message);
      console.error('Failed to delete notification:', err);
    }
  }, [notifications]);

  const updateFilters = useCallback((newFilters) => {
    setFilters(prev => ({ ...prev, ...newFilters }));
  }, []);

  const refresh = useCallback(() => {
    fetchNotifications();
  }, [fetchNotifications]);

  useEffect(() => {
    fetchNotifications();
  }, [fetchNotifications]);

  return {
    notifications,
    loading,
    error,
    unreadCount,
    filters,
    markAsRead,
    markAllAsRead,
    deleteNotification,
    updateFilters,
    refresh,
  };
};

const useNotificationPreferences = () => {
  const [preferences, setPreferences] = useState({
    email: true,
    push: true,
    sms: false,
    weeklyDigest: true,
  });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [saving, setSaving] = useState(false);

  const fetchPreferences = useCallback(async () => {
    try {
      setLoading(true);
      setError(null);
      
      // In real app, uncomment this:
      // const data = await notificationService.getPreferences();
      // setPreferences(data);
      
      // Mock API delay
      await new Promise(resolve => setTimeout(resolve, 300));
    } catch (err) {
      setError(err.message);
      console.error('Failed to fetch preferences:', err);
    } finally {
      setLoading(false);
    }
  }, []);

  const updatePreferences = useCallback(async (newPreferences) => {
    try {
      setSaving(true);
      setError(null);
      const updatedPrefs = { ...preferences, ...newPreferences };
      
      // In real app, uncomment this:
      // await notificationService.updatePreferences(updatedPrefs);
      
      // Mock API delay
      await new Promise(resolve => setTimeout(resolve, 300));
      setPreferences(updatedPrefs);
    } catch (err) {
      setError(err.message);
      console.error('Failed to update preferences:', err);
    } finally {
      setSaving(false);
    }
  }, [preferences]);

  const togglePreference = useCallback((key) => {
    const newValue = !preferences[key];
    updatePreferences({ [key]: newValue });
  }, [preferences, updatePreferences]);

  useEffect(() => {
    fetchPreferences();
  }, [fetchPreferences]);

  return {
    preferences,
    loading,
    error,
    saving,
    updatePreferences,
    togglePreference,
    refresh: fetchPreferences,
  };
};

const NotificationManager = () => {
  const [searchTerm, setSearchTerm] = useState('');
  const [filter, setFilter] = useState('all');
  const [showSettings, setShowSettings] = useState(false);

  // Use the custom hooks
  const {
    notifications,
    loading,
    error,
    unreadCount,
    markAsRead,
    markAllAsRead,
    deleteNotification,
    updateFilters,
    refresh
  } = useNotifications({ category: filter, search: searchTerm });

  const {
    preferences,
    loading: preferencesLoading,
    error: preferencesError,
    saving: preferencesSaving,
    togglePreference
  } = useNotificationPreferences();

  // Filter notifications locally for real-time search
  const filteredNotifications = useMemo(() => {
    return notifications.filter(notification => {
      const matchesFilter = filter === 'all' || 
        (filter === 'unread' && !notification.read) ||
        (filter === 'read' && notification.read) ||
        notification.category === filter;
      
      const matchesSearch = searchTerm === '' ||
        notification.title.toLowerCase().includes(searchTerm.toLowerCase()) ||
        notification.message.toLowerCase().includes(searchTerm.toLowerCase());
      
      return matchesFilter && matchesSearch;
    });
  }, [notifications, filter, searchTerm]);

  // Update filters when search term or filter changes
  useEffect(() => {
    const timeoutId = setTimeout(() => {
      updateFilters({ 
        category: filter === 'all' || filter === 'unread' || filter === 'read' ? undefined : filter,
        read: filter === 'unread' ? false : filter === 'read' ? true : undefined,
        search: searchTerm || undefined
      });
    }, 300); // Debounce API calls

    return () => clearTimeout(timeoutId);
  }, [searchTerm, filter, updateFilters]);

  const getTypeIcon = (type) => {
    switch (type) {
      case 'success': return <CheckCircle className="w-5 h-5 text-green-500" />;
      case 'warning': return <AlertCircle className="w-5 h-5 text-yellow-500" />;
      case 'error': return <XCircle className="w-5 h-5 text-red-500" />;
      default: return <Info className="w-5 h-5 text-blue-500" />;
    }
  };

  const formatTimeAgo = (timestamp) => {
    const now = new Date();
    const diff = now - timestamp;
    const minutes = Math.floor(diff / (1000 * 60));
    const hours = Math.floor(diff / (1000 * 60 * 60));
    const days = Math.floor(diff / (1000 * 60 * 60 * 24));

    if (days > 0) return `${days}d ago`;
    if (hours > 0) return `${hours}h ago`;
    if (minutes > 0) return `${minutes}m ago`;
    return 'Just now';
  };

  const handleMarkAsRead = async (id) => {
    try {
      await markAsRead(id);
    } catch (err) {
      // Error handling is done in the hook
    }
  };

  const handleMarkAllAsRead = async () => {
    try {
      await markAllAsRead();
    } catch (err) {
      // Error handling is done in the hook
    }
  };

  const handleDeleteNotification = async (id) => {
    try {
      await deleteNotification(id);
    } catch (err) {
      // Error handling is done in the hook
    }
  };

  if (loading) {
    return (
      <div className="max-w-4xl mx-auto p-6 bg-gray-50 min-h-screen">
        <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-8">
          <div className="flex items-center justify-center">
            <Loader className="w-8 h-8 animate-spin text-blue-500" />
            <span className="ml-2 text-gray-600">Loading notifications...</span>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="max-w-4xl mx-auto p-6 bg-gray-50 min-h-screen">
      <div className="bg-white rounded-lg shadow-sm border border-gray-200">
        {/* Error Display */}
        {error && (
          <div className="px-6 py-4 bg-red-50 border-b border-red-200">
            <div className="flex items-center">
              <XCircle className="w-5 h-5 text-red-500 mr-2" />
              <span className="text-red-700">Error loading notifications: {error}</span>
              <button
                onClick={refresh}
                className="ml-auto text-red-600 hover:text-red-800 underline"
              >
                Retry
              </button>
            </div>
          </div>
        )}

        {/* Header */}
        <div className="px-6 py-4 border-b border-gray-200 bg-gray-50 rounded-t-lg">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-3">
              <div className="relative">
                <Bell className="w-6 h-6 text-gray-700" />
                {unreadCount > 0 && (
                  <span className="absolute -top-2 -right-2 bg-red-500 text-white text-xs rounded-full w-5 h-5 flex items-center justify-center">
                    {unreadCount}
                  </span>
                )}
              </div>
              <h1 className="text-xl font-semibold text-gray-900">Notifications</h1>
              {unreadCount > 0 && (
                <span className="bg-blue-100 text-blue-800 text-sm font-medium px-2.5 py-0.5 rounded">
                  {unreadCount} new
                </span>
              )}
            </div>
            <div className="flex items-center space-x-2">
              <button
                onClick={refresh}
                className="p-2 text-gray-500 hover:text-gray-700 hover:bg-gray-100 rounded-lg"
                title="Refresh notifications"
              >
                <RefreshCw className="w-5 h-5" />
              </button>
              {unreadCount > 0 && (
                <button
                  onClick={handleMarkAllAsRead}
                  className="text-sm text-blue-600 hover:text-blue-800 font-medium"
                >
                  Mark all as read
                </button>
              )}
              <button
                onClick={() => setShowSettings(!showSettings)}
                className="p-2 text-gray-500 hover:text-gray-700 hover:bg-gray-100 rounded-lg"
              >
                <Settings className="w-5 h-5" />
              </button>
            </div>
          </div>
        </div>

        {/* Filters and Search */}
        <div className="px-6 py-4 border-b border-gray-200 space-y-4">
          <div className="flex items-center space-x-4">
            <div className="relative flex-1 max-w-md">
              <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-4 h-4" />
              <input
                type="text"
                placeholder="Search notifications..."
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                className="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              />
            </div>
            <div className="flex items-center space-x-2">
              <Filter className="w-4 h-4 text-gray-500" />
              <select
                value={filter}
                onChange={(e) => setFilter(e.target.value)}
                className="border border-gray-300 rounded-lg px-3 py-2 focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              >
                <option value="all">All</option>
                <option value="unread">Unread</option>
                <option value="read">Read</option>
                <option value="billing">Billing</option>
                <option value="team">Team</option>
                <option value="system">System</option>
                <option value="security">Security</option>
              </select>
            </div>
          </div>
        </div>

        {/* Settings Panel */}
        {showSettings && (
          <div className="px-6 py-4 border-b border-gray-200 bg-gray-50">
            <h3 className="text-sm font-medium text-gray-900 mb-3">Notification Preferences</h3>
            {preferencesError && (
              <div className="mb-3 text-sm text-red-600">
                Error loading preferences: {preferencesError}
              </div>
            )}
            <div className="space-y-2">
              {[
                { key: 'email', label: 'Email notifications' },
                { key: 'push', label: 'Push notifications' },
                { key: 'sms', label: 'SMS notifications' },
                { key: 'weeklyDigest', label: 'Weekly digest' }
              ].map(({ key, label }) => (
                <label key={key} className="flex items-center">
                  <input
                    type="checkbox"
                    checked={preferences[key]}
                    onChange={() => togglePreference(key)}
                    disabled={preferencesLoading || preferencesSaving}
                    className="rounded border-gray-300 text-blue-600 focus:ring-blue-500 disabled:opacity-50"
                  />
                  <span className="ml-2 text-sm text-gray-700">{label}</span>
                  {preferencesSaving && (
                    <Loader className="ml-2 w-3 h-3 animate-spin text-blue-500" />
                  )}
                </label>
              ))}
            </div>
          </div>
        )}

        {/* Notifications List */}
        <div className="divide-y divide-gray-200">
          {filteredNotifications.length === 0 ? (
            <div className="px-6 py-12 text-center">
              <Bell className="w-12 h-12 text-gray-300 mx-auto mb-4" />
              <p className="text-gray-500">
                {searchTerm || filter !== 'all' ? 'No notifications match your criteria' : 'No notifications found'}
              </p>
              {searchTerm && (
                <button
                  onClick={() => setSearchTerm('')}
                  className="mt-2 text-blue-600 hover:text-blue-800 text-sm underline"
                >
                  Clear search
                </button>
              )}
            </div>
          ) : (
            filteredNotifications.map((notification) => (
              <div
                key={notification.id}
                className={`px-6 py-4 hover:bg-gray-50 transition-colors ${
                  !notification.read ? 'bg-blue-50 border-l-4 border-l-blue-500' : ''
                }`}
              >
                <div className="flex items-start space-x-3">
                  <div className="flex-shrink-0 mt-1">
                    {getTypeIcon(notification.type)}
                  </div>
                  <div className="flex-1 min-w-0">
                    <div className="flex items-start justify-between">
                      <div className="flex-1">
                        <p className={`text-sm font-medium ${
                          !notification.read ? 'text-gray-900' : 'text-gray-700'
                        }`}>
                          {notification.title}
                        </p>
                        <p className="text-sm text-gray-600 mt-1">
                          {notification.message}
                        </p>
                        <div className="flex items-center space-x-3 mt-2">
                          <span className="text-xs text-gray-500">
                            {formatTimeAgo(notification.timestamp)}
                          </span>
                          <span className={`text-xs px-2 py-1 rounded-full ${
                            notification.category === 'billing' ? 'bg-green-100 text-green-800' :
                            notification.category === 'team' ? 'bg-blue-100 text-blue-800' :
                            notification.category === 'system' ? 'bg-yellow-100 text-yellow-800' :
                            'bg-red-100 text-red-800'
                          }`}>
                            {notification.category}
                          </span>
                        </div>
                      </div>
                      <div className="flex items-center space-x-2 ml-4">
                        {!notification.read && (
                          <button
                            onClick={() => handleMarkAsRead(notification.id)}
                            className="p-1 text-gray-400 hover:text-green-600 hover:bg-green-50 rounded"
                            title="Mark as read"
                          >
                            <Check className="w-4 h-4" />
                          </button>
                        )}
                        <button
                          onClick={() => handleDeleteNotification(notification.id)}
                          className="p-1 text-gray-400 hover:text-red-600 hover:bg-red-50 rounded"
                          title="Delete notification"
                        >
                          <X className="w-4 h-4" />
                        </button>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            ))
          )}
        </div>

        {/* Footer */}
        <div className="px-6 py-3 bg-gray-50 rounded-b-lg border-t border-gray-200">
          <p className="text-xs text-gray-500 text-center">
            Showing {filteredNotifications.length} of {notifications.length} notifications
          </p>
        </div>
      </div>
    </div>
  );
};

export default NotificationManager;