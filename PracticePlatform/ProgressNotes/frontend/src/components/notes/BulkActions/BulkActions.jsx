import React, { useState } from 'react';
import { Download, Archive, Trash2 } from 'lucide-react';
import NotesService from '../../../services/notesService';
import { useNotificationContext } from '../../common/Notification/NotificationProvider';

const BulkActions = ({ selectedNotes, onActionComplete }) => {
  const [loading, setLoading] = useState(false);
  const { showSuccess, showError } = useNotificationContext();

  const handleBulkAction = async (action) => {
    if (selectedNotes.length === 0) return;
    
    setLoading(true);
    try {
      switch (action) {
        case 'archive':
          await NotesService.bulkArchiveNotes(selectedNotes);
          showSuccess(`${selectedNotes.length} notes archived successfully`);
          break;
        case 'export':
          await NotesService.exportNotes(selectedNotes);
          showSuccess(`Export started for ${selectedNotes.length} notes`);
          break;
        case 'delete':
          if (window.confirm(`Delete ${selectedNotes.length} notes? This cannot be undone.`)) {
            await NotesService.bulkDeleteNotes(selectedNotes);
            showSuccess(`${selectedNotes.length} notes deleted successfully`);
          } else {
            return;
          }
          break;
        default:
          return;
      }
      onActionComplete?.();
    } catch (error) {
      showError(`Bulk action failed: ${error.message}`);
    } finally {
      setLoading(false);
    }
  };

  if (selectedNotes.length === 0) return null;

  return (
    <div className="bg-blue-50 border border-blue-200 rounded-lg p-4 mb-4">
      <div className="flex items-center justify-between">
        <span className="text-blue-800">
          {selectedNotes.length} note{selectedNotes.length > 1 ? 's' : ''} selected
        </span>
        <div className="flex items-center space-x-2">
          <button
            onClick={() => handleBulkAction('export')}
            disabled={loading}
            className="px-3 py-1 text-blue-600 border border-blue-600 rounded text-sm hover:bg-blue-50 disabled:opacity-50"
          >
            <Download className="h-4 w-4 mr-1 inline" />
            Export
          </button>
          <button
            onClick={() => handleBulkAction('archive')}
            disabled={loading}
            className="px-3 py-1 text-gray-600 border border-gray-600 rounded text-sm hover:bg-gray-50 disabled:opacity-50"
          >
            <Archive className="h-4 w-4 mr-1 inline" />
            Archive
          </button>
          <button
            onClick={() => handleBulkAction('delete')}
            disabled={loading}
            className="px-3 py-1 text-red-600 border border-red-600 rounded text-sm hover:bg-red-50 disabled:opacity-50"
          >
            <Trash2 className="h-4 w-4 mr-1 inline" />
            Delete
          </button>
        </div>
      </div>
    </div>
  );
};

export default BulkActions;
