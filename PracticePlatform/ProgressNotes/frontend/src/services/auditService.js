// src/services/auditService.js
import APIService from './api';

class AuditService extends APIService {
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
}

export default AuditService;
