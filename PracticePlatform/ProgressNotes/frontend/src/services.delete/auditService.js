// src/services/auditService.js
import APIService from './api';

class AuditService extends APIService {
  // Get audit logs for a specific resource
  static async getAuditLogs(resourceType, resourceId, filters = {}) {
    const params = new URLSearchParams();
    params.append('resource_type', resourceType);
    params.append('resource_id', resourceId);
    
    Object.entries(filters).forEach(([key, value]) => {
      if (value !== null && value !== undefined && value !== '') {
        params.append(key, value);
      }
    });

    return this.request(`/audit-logs/?${params.toString()}`);
  }

  // Get all audit logs with filters
  static async getAllAuditLogs(filters = {}) {
    const params = new URLSearchParams();
    Object.entries(filters).forEach(([key, value]) => {
      if (value !== null && value !== undefined && value !== '') {
        params.append(key, value);
      }
    });

    return this.request(`/audit-logs/?${params.toString()}`);
  }

  // Get audit log by ID
  static async getAuditLog(logId) {
    return this.request(`/audit-logs/${logId}`);
  }

  // Create audit log entry (usually done automatically by backend)
  static async createAuditLog(logData) {
    return this.request('/audit-logs/', {
      method: 'POST',
      body: JSON.stringify(logData),
    });
  }

  // Get audit logs for current user
  static async getUserAuditLogs(userId, filters = {}) {
    const params = new URLSearchParams();
    params.append('user_id', userId);
    
    Object.entries(filters).forEach(([key, value]) => {
      if (value !== null && value !== undefined && value !== '') {
        params.append(key, value);
      }
    });

    return this.request(`/audit-logs/user/?${params.toString()}`);
  }

  // Get audit statistics
  static async getAuditStats(resourceType = null, dateFrom = null, dateTo = null) {
    const params = new URLSearchParams();
    if (resourceType) params.append('resource_type', resourceType);
    if (dateFrom) params.append('date_from', dateFrom);
    if (dateTo) params.append('date_to', dateTo);

    return this.request(`/audit-logs/stats/?${params.toString()}`);
  }

  // Export audit logs
  static async exportAuditLogs(filters = {}, format = 'csv') {
    const params = new URLSearchParams();
    params.append('format', format);
    
    Object.entries(filters).forEach(([key, value]) => {
      if (value !== null && value !== undefined && value !== '') {
        params.append(key, value);
      }
    });

    const response = await fetch(`${this.API_BASE_URL}/audit-logs/export/?${params.toString()}`, {
      headers: {
        Authorization: `Bearer ${localStorage.getItem('access_token')}`
      }
    });

    if (!response.ok) {
      throw new Error('Export failed');
    }

    return response.blob();
  }

  // Get audit logs for multiple resources
  static async getMultiResourceAuditLogs(resources, filters = {}) {
    return this.request('/audit-logs/multi-resource/', {
      method: 'POST',
      body: JSON.stringify({
        resources,
        filters
      }),
    });
  }

  // Search audit logs
  static async searchAuditLogs(searchQuery, filters = {}) {
    const params = new URLSearchParams();
    params.append('q', searchQuery);
    
    Object.entries(filters).forEach(([key, value]) => {
      if (value !== null && value !== undefined && value !== '') {
        params.append(key, value);
      }
    });

    return this.request(`/audit-logs/search/?${params.toString()}`);
  }
}

export default AuditService;
