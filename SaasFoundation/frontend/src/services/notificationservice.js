// services/notificationService.js
class NotificationService {
    constructor(baseURL = '/api') {
      this.baseURL = baseURL;
    }
  
    // Helper method for making API calls
    async apiCall(endpoint, options = {}) {
      const url = `${this.baseURL}${endpoint}`;
      const config = {
        headers: {
          'Content-Type': 'application/json',
          // Add authorization header if needed
          // 'Authorization': `Bearer ${getAuthToken()}`,
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
  
    // Fetch all notifications with optional filters
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
      if (filters.limit) {
        queryParams.append('limit', filters.limit);
      }
      if (filters.offset) {
        queryParams.append('offset', filters.offset);
      }
  
      const endpoint = `/notifications${queryParams.toString() ? `?${queryParams.toString()}` : ''}`;
      return this.apiCall(endpoint);
    }
  
    // Mark a single notification as read
    async markAsRead(notificationId) {
      return this.apiCall(`/notifications/${notificationId}/read`, {
        method: 'PATCH',
        body: JSON.stringify({ read: true }),
      });
    }
  
    // Mark multiple notifications as read
    async markMultipleAsRead(notificationIds) {
      return this.apiCall('/notifications/bulk/read', {
        method: 'PATCH',
        body: JSON.stringify({ notificationIds, read: true }),
      });
    }
  
    // Mark all notifications as read
    async markAllAsRead() {
      return this.apiCall('/notifications/read-all', {
        method: 'PATCH',
      });
    }
  
    // Delete a notification
    async deleteNotification(notificationId) {
      return this.apiCall(`/notifications/${notificationId}`, {
        method: 'DELETE',
      });
    }
  
    // Delete multiple notifications
    async deleteMultipleNotifications(notificationIds) {
      return this.apiCall('/notifications/bulk/delete', {
        method: 'DELETE',
        body: JSON.stringify({ notificationIds }),
      });
    }
  
    // Get notification preferences
    async getPreferences() {
      return this.apiCall('/notifications/preferences');
    }
  
    // Update notification preferences
    async updatePreferences(preferences) {
      return this.apiCall('/notifications/preferences', {
        method: 'PUT',
        body: JSON.stringify(preferences),
      });
    }
  
    // Get unread count
    async getUnreadCount() {
      return this.apiCall('/notifications/unread-count');
    }
  
    // Create a new notification (admin/system use)
    async createNotification(notification) {
      return this.apiCall('/notifications', {
        method: 'POST',
        body: JSON.stringify(notification),
      });
    }
  }
  
  export const notificationService = new NotificationService();
  
  
 
  
  // Example backend API endpoints structure (for reference)
  /*
  Backend API Endpoints needed:
  
  GET /api/notifications
  - Query params: category, read, search, limit, offset
  - Returns: { notifications: [...], total: number }
  
  GET /api/notifications/unread-count
  - Returns: { count: number }
  
  PATCH /api/notifications/:id/read
  - Body: { read: boolean }
  - Returns: { success: boolean }
  
  PATCH /api/notifications/read-all
  - Returns: { success: boolean }
  
  PATCH /api/notifications/bulk/read
  - Body: { notificationIds: [...], read: boolean }
  - Returns: { success: boolean }
  
  DELETE /api/notifications/:id
  - Returns: { success: boolean }
  
  DELETE /api/notifications/bulk/delete
  - Body: { notificationIds: [...] }
  - Returns: { success: boolean }
  
  GET /api/notifications/preferences
  - Returns: { email: boolean, push: boolean, sms: boolean, weeklyDigest: boolean }
  
  PUT /api/notifications/preferences
  - Body: { email: boolean, push: boolean, sms: boolean, weeklyDigest: boolean }
  - Returns: { success: boolean }
  
  POST /api/notifications (for creating new notifications)
  - Body: { title, message, type, category, userId }
  - Returns: { notification: {...} }
  */