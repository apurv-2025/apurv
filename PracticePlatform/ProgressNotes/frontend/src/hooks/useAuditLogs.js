// src/hooks/useAuditLogs.js
import { useState, useEffect, useCallback } from 'react';
import AuditService from '../services/auditService';

export const useAuditLogs = (resourceType, resourceId, initialFilters = {}) => {
  const [auditLogs, setAuditLogs] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [totalPages, setTotalPages] = useState(1);
  const [filters, setFilters] = useState({
    action: '',
    user_id: '',
    date_from: '',
    date_to: '',
    page: 1,
    page_size: 20,
    ...initialFilters
  });

  const fetchAuditLogs = useCallback(async () => {
    if (!resourceType || !resourceId) return;

    setLoading(true);
    setError(null);

    try {
      const data = await AuditService.getAuditLogs(resourceType, resourceId, filters);
      setAuditLogs(data.items || []);
      setTotalPages(data.total_pages || 1);
    } catch (err) {
      setError(err.message);
      console.error('Error fetching audit logs:', err);
    } finally {
      setLoading(false);
    }
  }, [resourceType, resourceId, filters]);

  useEffect(() => {
    fetchAuditLogs();
  }, [fetchAuditLogs]);

  const updateFilter = useCallback((key, value) => {
    setFilters(prev => ({ 
      ...prev, 
      [key]: value,
      page: 1 // Reset to first page when filtering
    }));
  }, []);

  const clearFilters = useCallback(() => {
    setFilters({
      action: '',
      user_id: '',
      date_from: '',
      date_to: '',
      page: 1,
      page_size: 20
    });
  }, []);

  const exportLogs = useCallback(async (format = 'csv') => {
    try {
      const blob = await AuditService.exportAuditLogs(filters, format);
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `audit_logs_${resourceType}_${resourceId}.${format}`;
      document.body.appendChild(a);
      a.click();
      window.URL.revokeObjectURL(url);
      document.body.removeChild(a);
      return true;
    } catch (err) {
      setError(`Export failed: ${err.message}`);
      return false;
    }
  }, [resourceType, resourceId, filters]);

  return {
    auditLogs,
    loading,
    error,
    totalPages,
    filters,
    updateFilter,
    clearFilters,
    exportLogs,
    refetch: fetchAuditLogs
  };
};

// Hook for getting audit statistics
export const useAuditStats = (resourceType = null, dateFrom = null, dateTo = null) => {
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchStats = async () => {
      setLoading(true);
      setError(null);

      try {
        const data = await AuditService.getAuditStats(resourceType, dateFrom, dateTo);
        setStats(data);
      } catch (err) {
        setError(err.message);
        console.error('Error fetching audit stats:', err);
      } finally {
        setLoading(false);
      }
    };

    fetchStats();
  }, [resourceType, dateFrom, dateTo]);

  return { stats, loading, error };
};
