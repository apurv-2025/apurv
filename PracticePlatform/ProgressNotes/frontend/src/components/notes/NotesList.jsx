// src/components/NotesList.jsx
import React, { useState } from 'react';
import { 
  Search, 
  Filter, 
  Download, 
  Archive, 
  Eye, 
  Edit, 
  Trash2,
  Plus,
  Calendar,
  Clock,
  User,
  Lock
} from 'lucide-react';
import NoteCard from './ui/NoteCard';
import NoteListItem from './ui/NoteListItem';
import SearchFilters from './ui/SearchFilters';
import BulkActions from './ui/BulkActions';
import Pagination from './ui/Pagination';

const NotesList = ({
  notes = [],
  totalPages = 1,
  filters = {},
  sortBy = 'session_date',
  sortOrder = 'desc',
  selectedNotes = [],
  onSelectNote,
  onEditNote,
  onCreateNote,
  onDeleteNote,
  onSignNote,
  onFilterChange,
  onSortChange,
  onToggleSelection,
  onSelectAll,
  onBulkAction
}) => {
  const [viewMode, setViewMode] = useState('list'); // 'list' or 'grid'
  const [showAdvancedSearch, setShowAdvancedSearch] = useState(false);

  const handleSort = (field) => {
    if (sortBy === field) {
      onSortChange(field, sortOrder === 'asc' ? 'desc' : 'asc');
    } else {
      onSortChange(field, 'desc');
    }
  };

  const getSortIcon = (field) => {
    if (sortBy === field) {
      return sortOrder === 'asc' ? '↑' : '↓';
    }
    return '';
  };

  const isAllSelected = selectedNotes.length === notes.length && notes.length > 0;
  const isSomeSelected = selectedNotes.length > 0 && selectedNotes.length < notes.length;

  return (
    <div className="p-6">
      {/* Header */}
      <div className="flex justify-between items-center mb-6">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">Progress Notes</h1>
          <p className="text-gray-600 mt-1">
            {notes.length} note{notes.length !== 1 ? 's' : ''} found
          </p>
        </div>
        <div className="flex items-center space-x-3">
          <button
            onClick={() => setViewMode(viewMode === 'list' ? 'grid' : 'list')}
            className="px-3 py-2 text-gray-600 border border-gray-300 rounded-md hover:bg-gray-50 transition-colors"
          >
            {viewMode === 'list' ? 'Grid View' : 'List View'}
          </button>
          <button
            onClick={onCreateNote}
            className="bg-blue-600 text-white px-4 py-2 rounded-md hover:bg-blue-700 transition-colors flex items-center"
          >
            <Plus className="h-4 w-4 mr-2" />
            New Note
          </button>
        </div>
      </div>

      {/* Search and Filters */}
      <SearchFilters
        filters={filters}
        onFilterChange={onFilterChange}
        showAdvanced={showAdvancedSearch}
        onToggleAdvanced={() => setShowAdvancedSearch(!showAdvancedSearch)}
      />

      {/* Bulk Actions */}
      {selectedNotes.length > 0 && (
        <BulkActions
          selectedCount={selectedNotes.length}
          onBulkAction={onBulkAction}
        />
      )}

      {/* List/Grid Content */}
      {viewMode === 'list' ? (
        <div className="bg-white rounded-lg shadow">
          {/* List Header */}
          <div className="p-4 border-b border-gray-200">
            <div className="flex items-center space-x-4">
              <label className="flex items-center">
                <input
                  type="checkbox"
                  checked={isAllSelected}
                  ref={input => {
                    if (input) input.indeterminate = isSomeSelected;
                  }}
                  onChange={onSelectAll}
                  className="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded"
                />
                <span className="ml-2 text-sm text-gray-600">
                  {isAllSelected ? 'Deselect All' : 'Select All'}
                </span>
              </label>
              
              <div className="flex items-center space-x-4 ml-auto">
                <span className="text-sm text-gray-600">Sort by:</span>
                <button
                  onClick={() => handleSort('session_date')}
                  className={`text-sm font-medium transition-colors ${
                    sortBy === 'session_date' ? 'text-blue-600' : 'text-gray-600 hover:text-blue-600'
                  }`}
                >
                  Date {getSortIcon('session_date')}
                </button>
                <button
                  onClick={() => handleSort('patient_name')}
                  className={`text-sm font-medium transition-colors ${
                    sortBy === 'patient_name' ? 'text-blue-600' : 'text-gray-600 hover:text-blue-600'
                  }`}
                >
                  Patient {getSortIcon('patient_name')}
                </button>
                <button
                  onClick={() => handleSort('note_type')}
                  className={`text-sm font-medium transition-colors ${
                    sortBy === 'note_type' ? 'text-blue-600' : 'text-gray-600 hover:text-blue-600'
                  }`}
                >
                  Type {getSortIcon('note_type')}
                </button>
              </div>
            </div>
          </div>
          
          {/* List Column Headers */}
          <div className="grid grid-cols-1 md:grid-cols-6 gap-4 p-4 bg-gray-50 border-b border-gray-200 text-sm font-medium text-gray-700">
            <div className="md:col-span-2">Patient</div>
            <div>Type</div>
            <div>Session Date</div>
            <div>Clinician</div>
            <div>Status</div>
          </div>

          {/* List Items */}
          <div className="divide-y divide-gray-200">
            {notes.length > 0 ? (
              notes.map((note) => (
                <NoteListItem
                  key={note.id}
                  note={note}
                  isSelected={selectedNotes.includes(note.id)}
                  onSelect={() => onToggleSelection(note.id)}
                  onView={() => onSelectNote(note, 'view')}
                  onEdit={() => onEditNote(note)}
                  onDelete={() => onDeleteNote(note.id)}
                  onSign={() => onSignNote(note.id)}
                />
              ))
            ) : (
              <div className="p-12 text-center text-gray-500">
                <div className="mb-4">
                  <Search className="h-12 w-12 text-gray-300 mx-auto" />
                </div>
                <h3 className="text-lg font-medium text-gray-900 mb-2">No notes found</h3>
                <p className="text-gray-600 mb-4">
                  {Object.values(filters).some(v => v) 
                    ? 'Try adjusting your search filters or create a new note.'
                    : 'Create your first note to get started.'
                  }
                </p>
                <button
                  onClick={onCreateNote}
                  className="bg-blue-600 text-white px-4 py-2 rounded-md hover:bg-blue-700 transition-colors"
                >
                  Create First Note
                </button>
              </div>
            )}
          </div>
        </div>
      ) : (
        /* Grid View */
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {notes.length > 0 ? (
            notes.map((note) => (
              <NoteCard
                key={note.id}
                note={note}
                isSelected={selectedNotes.includes(note.id)}
                onSelect={() => onToggleSelection(note.id)}
                onView={() => onSelectNote(note, 'view')}
                onEdit={() => onEditNote(note)}
                onDelete={() => onDeleteNote(note.id)}
                onSign={() => onSignNote(note.id)}
              />
            ))
          ) : (
            <div className="col-span-full p-12 text-center text-gray-500">
              <div className="mb-4">
                <Search className="h-12 w-12 text-gray-300 mx-auto" />
              </div>
              <h3 className="text-lg font-medium text-gray-900 mb-2">No notes found</h3>
              <p className="text-gray-600 mb-4">
                {Object.values(filters).some(v => v) 
                  ? 'Try adjusting your search filters or create a new note.'
                  : 'Create your first note to get started.'
                }
              </p>
              <button
                onClick={onCreateNote}
                className="bg-blue-600 text-white px-4 py-2 rounded-md hover:bg-blue-700 transition-colors"
              >
                Create First Note
              </button>
            </div>
          )}
        </div>
      )}

      {/* Pagination */}
      {totalPages > 1 && (
        <div className="mt-6">
          <Pagination
            currentPage={filters.page || 1}
            totalPages={totalPages}
            onPageChange={(page) => onFilterChange('page', page)}
          />
        </div>
      )}
    </div>
  );
};

export default NotesList;
