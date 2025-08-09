import React from 'react';
import { AUDIT_ACTIONS } from '../../../utils/constants';

const AuditFilters = ({ filters, onFilterChange, onClearFilters }) => {
  return (
    <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
      <select
        value={filters.action}
        onChange={(e) => onFilterChange('action', e.target.value)}
        className="px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
      >
        <option value="">All Actions</option>
        {Object.values(AUDIT_ACTIONS).map(action => (
          <option key={action} value={action}>
            {action.charAt(0).toUpperCase() + action.slice(1)}
          </option>
        ))}
      </select>

      <input
        type="date"
        value={filters.date_from}
        onChange={(e) => onFilterChange('date_from', e.target.value)}
        className="px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
        placeholder="From Date"
      />

      <input
        type="date"
        value={filters.date_to}
        onChange={(e) => onFilterChange('date_to', e.target.value)}
        className="px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
        placeholder="To Date"
      />

      <button
        onClick={onClearFilters}
        className="px-3 py-2 text-gray-600 border border-gray-300 rounded-md hover:bg-gray-50"
      >
        Clear Filters
      </button>
    </div>
  );
};

export default AuditFilters;
