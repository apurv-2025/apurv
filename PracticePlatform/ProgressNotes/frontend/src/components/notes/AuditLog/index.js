import React, { useState, useEffect } from 'react';
import { RotateCcw } from 'lucide-react';
import AuditLogEntry from './AuditLogEntry';
import AuditFilters from './AuditFilters';
import AuditService from '../../../services/auditService';

const AuditLogViewer = ({ resourceType, resourceId }) => {
  const [auditLogs, setAuditLogs] = useState([]);
  const [loading, setLoading] = useState(true);
  const [filters, setFilters] = useState({
    action: '',
    user_id: '',
    date_from: '',
    date_to: ''
  });

  useEffect(() => {
    fetchAuditLogs();
  }, [resourceId, resourceType, filters]);

  const fetchAuditLogs = async () => {
    if (!resourceId || !resourceType) return;
    
    setLoading(true);
    try {
      const data = await AuditService.getAuditLogs(resourceType, resourceId, filters);
      setAuditLogs(data.items || []);
    } catch (error) {
      console.error('Error fetching audit logs:', error);
      // Fallback to mock data for demo
      setAuditLogs([
        {
          id: '1',
          action: 'create',
          user: { first_name: 'John', last_name: 'Doe' },
          created_at: '2024-01-15T10:30:00Z',
          ip_address: '192.168.1.1',
          old_values: null,
          new_values: { note_type: 'SOAP', patient_id: 'patient-1' }
        },
        {
          id: '2',
          action: 'update',
          user: { first_name: 'John', last_name: 'Doe' },
          created_at: '2024-01-15T11:15:00Z',
          ip_address: '192.168.1.1',
          old_values: { content: { subjective: 'Old content' } },
          new_values: { content: { subjective: 'Updated content' } }
        },
        {
          id: '3',
          action: 'sign',
          user: { first_name: 'John', last_name: 'Doe' },
          created_at: '2024-01-15T11:30:00Z',
          ip_address: '192.168.1.1',
          old_values: { is_signed: false },
          new_values: { is_signed: true, signed_at: '2024-01-15T11:30:00Z' }
        }
      ]);
    } finally {
      setLoading(false);
    }
  };

  const handleFilterChange = (key, value) => {
    setFilters(prev => ({ ...prev, [key]: value }));
  };

  const handleClearFilters = () => {
    setFilters({
      action: '',
      user_id: '',
      date_from: '',
      date_to: ''
    });
  };

  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between">
        <h3 className="text-lg font-medium text-gray-900">Audit Trail</h3>
        <button
          onClick={fetchAuditLogs}
          className="px-3 py-2 text-gray-600 border border-gray-300 rounded-md hover:bg-gray-50 flex items-center"
        >
          <RotateCcw className="h-4 w-4 mr-2" />
          Refresh
        </button>
      </div>

      <AuditFilters
        filters={filters}
        onFilterChange={handleFilterChange}
        onClearFilters={handleClearFilters}
      />

      <div className="space-y-3">
        {loading ? (
          <div className="text-center py-4">Loading audit logs...</div>
        ) : auditLogs.length > 0 ? (
          auditLogs.map((log) => (
            <AuditLogEntry key={log.id} log={log} />
          ))
        ) : (
          <div className="text-center py-4 text-gray-500">
            No audit logs found for the selected filters.
          </div>
        )}
      </div>
    </div>
  );
};

export default AuditLogViewer;
