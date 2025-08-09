import React from 'react';
import { Search, Filter } from 'lucide-react';
import { NOTE_TYPES, NOTE_FILTERS } from '../../../utils/constants';

const BasicFilters = ({ filters, onFilterChange, onShowAdvanced }) => {
  return (
    <div className="bg-white p-4 rounded-lg shadow mb-6">
      <div className="flex items-center space-x-4 mb-4">
        <div className="flex-1 relative">
          <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 h-4 w-4" />
          <input
            type="text"
            placeholder="Search notes..."
            value={filters[NOTE_FILTERS.SEARCH_QUERY]}
            onChange={(e) => onFilterChange(NOTE_FILTERS.SEARCH_QUERY, e.target.value)}
            className="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
        </div>
        <button
          onClick={onShowAdvanced}
          className="px-4 py-2 text-gray-600 border border-gray-300 rounded-md hover:bg-gray-50"
        >
          <Filter className="h-4 w-4 mr-2 inline" />
          Advanced
        </button>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <select
          value={filters[NOTE_FILTERS.NOTE_TYPE]}
          onChange={(e) => onFilterChange(NOTE_FILTERS.NOTE_TYPE, e.target.value)}
          className="px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
        >
          <option value="">All Types</option>
          {Object.values(NOTE_TYPES).map(type => (
            <option key={type} value={type}>{type}</option>
          ))}
        </select>

        <select
          value={filters[NOTE_FILTERS.IS_DRAFT]}
          onChange={(e) => onFilterChange(NOTE_FILTERS.IS_DRAFT, e.target.value)}
          className="px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
        >
          <option value="">All Notes</option>
          <option value="true">Drafts Only</option>
          <option value="false">Final Notes</option>
        </select>

        <input
          type="date"
          value={filters[NOTE_FILTERS.DATE_FROM]}
          onChange={(e) => onFilterChange(NOTE_FILTERS.DATE_FROM, e.target.value)}
          className="px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
          placeholder="From Date"
        />

        <input
          type="date"
          value={filters[NOTE_FILTERS.DATE_TO]}
          onChange={(e) => onFilterChange(NOTE_FILTERS.DATE_TO, e.target.value)}
          className="px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
          placeholder="To Date"
        />
      </div>
    </div>
  );
};

export default BasicFilters;
