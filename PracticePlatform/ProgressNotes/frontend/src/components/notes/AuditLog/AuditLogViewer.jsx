import React from 'react';
import { RotateCcw, Download } from 'lucide-react';
import { useAuditLogs } from '../../../hooks/useAuditLogs';
import { useNotificationContext } from '../../common/Notification/NotificationProvider';
import AuditLogEntry from './AuditLogEntry';
import AuditFilters from './AuditFilters';
import Pagination from '../../common/Pagination/Pagination';
import ErrorMessage from '../../common/ErrorMessage';

const EnhancedAuditLogViewer = ({ resourceType, resourceId }) => {
  const { showSuccess, showError } = useNotificationContext();
  
  const {
    auditLogs,
    loading,
    error,
    totalPages,
    filters,
    updateFilter,
    clearFilters,
    exportLogs,
    refetch
  } = useAuditLogs(resourceType, resourceId);

  const handleExport = async (format) => {
    const success = await exportLogs(format);
    if (success) {
      showSuccess(`Audit logs exported successfully as ${format.toUpperCase()}`);
    } else {
      showError('Failed to export audit logs');
    }
  };

  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between">
        <h3 className="text-lg font-medium text-gray-900">Audit Trail</h3>
        <div className="flex items-center space-x-2">
          <div className="relative">
            <button className="px-3 py-2 text-gray-600 border border-gray-300 rounded-md hover:bg-gray-50 flex items-center">
              <Download className="h-4 w-4 mr-2" />
              Export
            </button>
            {/* Dropdown menu for export options could go here */}
          </div>
          <button
            onClick={refetch}
            className="px-3 py-2 text-gray-600 border border-gray-300 rounded-md hover:bg-gray-50 flex items-center"
          >
            <RotateCcw className="h-4 w-4 mr-2" />
            Refresh
          </button>
        </div>
      </div>

      <AuditFilters
        filters={filters}
        onFilterChange={updateFilter}
        onClearFilters={clearFilters}
      />

      {error && <ErrorMessage error={error} onRetry={refetch} />}

      <div className="space-y-3">
        {loading ? (
          <div className="text-center py-4">Loading audit logs...</div>
        ) : auditLogs.length > 0 ? (
          <>
            {auditLogs.map((log) => (
              <AuditLogEntry key={log.id} log={log} />
            ))}
            
            {totalPages > 1 && (
              <div className="mt-6">
                <Pagination
                  currentPage={filters.page}
                  totalPages={totalPages}
                  onPageChange={(page) => updateFilter('page', page)}
                />
              </div>
            )}
          </>
        ) : (
          <div className="text-center py-4 text-gray-500">
            No audit logs found for the selected filters.
          </div>
        )}
      </div>
    </div>
  );
};

export default EnhancedAuditLogViewer;
