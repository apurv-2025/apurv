import React, { useState } from 'react';
import { Plus } from 'lucide-react';
import { useNotes } from '../../../hooks/useNotes';
import { VIEW_MODES, NOTE_FILTERS } from '../../../utils/constants';
import BasicFilters from '../NotesFilter/BasicFilters';
import BulkActions from '../BulkActions/BulkActions';
import NoteCard from '../NoteCard/NoteCard';
import NoteListItem from '../NoteCard/NoteListItem';
import Pagination from '../../common/Pagination/Pagination';

const EnhancedNotesList = ({ onSelectNote, onCreateNote, onEditNote }) => {
  const {
    notes,
    loading,
    totalPages,
    filters,
    sortBy,
    sortOrder,
    updateFilter,
    updateSort,
    refetch
  } = useNotes();

  const [selectedNotes, setSelectedNotes] = useState([]);
  const [viewMode, setViewMode] = useState(VIEW_MODES.LIST);
  const [showAdvancedSearch, setShowAdvancedSearch] = useState(false);

  const handleSelectNote = (noteId) => {
    setSelectedNotes(prev => 
      prev.includes(noteId) 
        ? prev.filter(id => id !== noteId)
        : [...prev, noteId]
    );
  };

  const handleSelectAll = () => {
    if (selectedNotes.length === notes.length) {
      setSelectedNotes([]);
    } else {
      setSelectedNotes(notes.map(note => note.id));
    }
  };

  const handleBulkActionComplete = () => {
    setSelectedNotes([]);
    refetch();
  };

  const renderSortHeader = () => {
    if (viewMode !== VIEW_MODES.LIST) return null;

    return (
      <div className="bg-white rounded-lg shadow mb-4">
        <div className="p-4 border-b border-gray-200">
          <div className="flex items-center space-x-4">
            <button
              onClick={handleSelectAll}
              className="text-sm text-blue-600 hover:text-blue-800"
            >
              {selectedNotes.length === notes.length ? 'Deselect All' : 'Select All'}
            </button>
            <div className="flex items-center space-x-2">
              <span className="text-sm text-gray-600">Sort by:</span>
              <button
                onClick={() => updateSort('session_date')}
                className={`text-sm ${sortBy === 'session_date' ? 'text-blue-600' : 'text-gray-600'} hover:text-blue-800`}
              >
                Date {sortBy === 'session_date' && (sortOrder === 'asc' ? '↑' : '↓')}
              </button>
              <button
                onClick={() => updateSort('patient_name')}
                className={`text-sm ${sortBy === 'patient_name' ? 'text-blue-600' : 'text-gray-600'} hover:text-blue-800`}
              >
                Patient {sortBy === 'patient_name' && (sortOrder === 'asc' ? '↑' : '↓')}
              </button>
              <button
                onClick={() => updateSort('note_type')}
                className={`text-sm ${sortBy === 'note_type' ? 'text-blue-600' : 'text-gray-600'} hover:text-blue-800`}
              >
                Type {sortBy === 'note_type' && (sortOrder === 'asc' ? '↑' : '↓')}
              </button>
            </div>
          </div>
        </div>
        
        {/* List Header */}
        <div className="grid grid-cols-1 md:grid-cols-5 gap-4 p-4 bg-gray-50 border-b border-gray-200 text-sm font-medium text-gray-700">
          <div>Patient</div>
          <div>Type</div>
          <div>Session Date</div>
          <div>Clinician</div>
          <div>Status</div>
        </div>
      </div>
    );
  };

  const renderNotes = () => {
    if (loading) {
      return (
        <div className="col-span-full p-8 text-center">Loading notes...</div>
      );
    }

    if (notes.length === 0) {
      return (
        <div className="col-span-full p-8 text-center text-gray-500">
          No notes found. Create your first note to get started.
        </div>
      );
    }

    return notes.map((note) => 
      viewMode === VIEW_MODES.GRID ? (
        <NoteCard
          key={note.id}
          note={note}
          isSelected={selectedNotes.includes(note.id)}
          onSelect={handleSelectNote}
          onView={onSelectNote}
          onEdit={onEditNote}
        />
      ) : (
        <NoteListItem
          key={note.id}
          note={note}
          isSelected={selectedNotes.includes(note.id)}
          onSelect={handleSelectNote}
          onView={onSelectNote}
        />
      )
    );
  };

  return (
    <div className="p-6">
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-2xl font-bold text-gray-900">Progress Notes</h1>
        <div className="flex items-center space-x-3">
          <button
            onClick={() => setViewMode(viewMode === VIEW_MODES.LIST ? VIEW_MODES.GRID : VIEW_MODES.LIST)}
            className="px-3 py-2 text-gray-600 border border-gray-300 rounded-md hover:bg-gray-50"
          >
            {viewMode === VIEW_MODES.LIST ? 'Grid View' : 'List View'}
          </button>
          <button
            onClick={onCreateNote}
            className="bg-blue-600 text-white px-4 py-2 rounded-md hover:bg-blue-700 flex items-center"
          >
            <Plus className="h-4 w-4 mr-2" />
            New Note
          </button>
        </div>
      </div>

      <BasicFilters 
        filters={filters}
        onFilterChange={updateFilter}
        onShowAdvanced={() => setShowAdvancedSearch(true)}
      />

      <BulkActions
        selectedNotes={selectedNotes}
        onActionComplete={handleBulkActionComplete}
      />

      {renderSortHeader()}

      {/* Notes Content */}
      <div className={viewMode === VIEW_MODES.GRID ? 'grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4' : 'bg-white rounded-lg shadow'}>
        {renderNotes()}
      </div>

      {/* Pagination */}
      {totalPages > 1 && (
        <div className="mt-6">
          <Pagination
            currentPage={filters[NOTE_FILTERS.PAGE]}
            totalPages={totalPages}
            onPageChange={(page) => updateFilter(NOTE_FILTERS.PAGE, page)}
          />
        </div>
      )}
    </div>
  );
};

export default EnhancedNotesList;
