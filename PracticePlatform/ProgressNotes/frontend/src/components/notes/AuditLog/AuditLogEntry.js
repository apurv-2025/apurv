import React from 'react';
import { Plus, Edit, Trash2, Lock, Unlock, Eye, History } from 'lucide-react';
import { AUDIT_ACTIONS } from '../../../utils/constants';

const AuditLogEntry = ({ log }) => {
  const getActionIcon = (action) => {
    switch (action) {
      case AUDIT_ACTIONS.CREATE: 
        return <Plus className="h-4 w-4 text-green-600" />;
      case AUDIT_ACTIONS.UPDATE: 
        return <Edit className="h-4 w-4 text-blue-600" />;
      case AUDIT_ACTIONS.DELETE: 
        return <Trash2 className="h-4 w-4 text-red-600" />;
      case AUDIT_ACTIONS.SIGN: 
        return <Lock className="h-4 w-4 text-green-600" />;
      case AUDIT_ACTIONS.UNLOCK: 
        return <Unlock className="h-4 w-4 text-orange-600" />;
      case AUDIT_ACTIONS.READ: 
        return <Eye className="h-4 w-4 text-gray-600" />;
      default: 
        return <History className="h-4 w-4 text-gray-600" />;
    }
  };

  const getActionLabel = (action) => {
    return action.charAt(0).toUpperCase() + action.slice(1);
  };

  const formatChanges = (oldValues, newValues) => {
    if (!oldValues && !newValues) return null;
    
    if (!oldValues) {
      return (
        <div className="text-sm text-green-700 bg-green-50 p-2 rounded">
          <strong>Created:</strong>
          <pre className="mt-1 text-xs overflow-x-auto">
            {JSON.stringify(newValues, null, 2)}
          </pre>
        </div>
      );
    }

    return (
      <div className="space-y-2">
        {oldValues && (
          <div className="text-sm text-red-700 bg-red-50 p-2 rounded">
            <strong>Before:</strong>
            <pre className="mt-1 text-xs overflow-x-auto">
              {JSON.stringify(oldValues, null, 2)}
            </pre>
          </div>
        )}
        {newValues && (
          <div className="text-sm text-green-700 bg-green-50 p-2 rounded">
            <strong>After:</strong>
            <pre className="mt-1 text-xs overflow-x-auto">
              {JSON.stringify(newValues, null, 2)}
            </pre>
          </div>
        )}
      </div>
    );
  };

  return (
    <div className="bg-white border border-gray-200 rounded-lg p-4">
      <div className="flex items-start justify-between">
        <div className="flex items-start space-x-3">
          <div className="mt-1">
            {getActionIcon(log.action)}
          </div>
          <div className="flex-1">
            <div className="flex items-center space-x-2">
              <span className="font-medium text-gray-900">
                {getActionLabel(log.action)}
              </span>
              <span className="text-gray-600">by</span>
              <span className="font-medium text-gray-900">
                {log.user.first_name} {log.user.last_name}
              </span>
            </div>
            <div className="text-sm text-gray-600 mt-1">
              {new Date(log.created_at).toLocaleString()} • IP: {log.ip_address}
            </div>
            {(log.old_values || log.new_values) && (
              <div className="mt-3">
                {formatChanges(log.old_values, log.new_values)}
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default AuditLogEntry;
