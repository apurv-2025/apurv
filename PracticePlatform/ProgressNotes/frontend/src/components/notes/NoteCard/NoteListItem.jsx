import React from 'react';
import { Eye, Lock } from 'lucide-react';

const NoteListItem = ({ note, isSelected, onSelect, onView }) => {
  return (
    <div className={`bg-white border-b border-gray-200 transition-colors ${
      isSelected ? 'bg-blue-50' : 'hover:bg-gray-50'
    }`}>
      <div className="p-4">
        <div className="flex items-center space-x-4">
          <input
            type="checkbox"
            checked={isSelected}
            onChange={() => onSelect(note.id)}
          />
          
          <div className="flex-1 grid grid-cols-1 md:grid-cols-5 gap-4 items-center">
            <div>
              <div className="font-medium text-gray-900">
                {note.patient?.first_name} {note.patient?.last_name}
              </div>
              <div className="text-sm text-gray-500">
                MRN: {note.patient?.medical_record_number}
              </div>
            </div>
            
            <div className="text-sm text-gray-900">
              {note.note_type}
            </div>
            
            <div className="text-sm text-gray-900">
              {new Date(note.session_date).toLocaleDateString()}
            </div>
            
            <div className="text-sm text-gray-900">
              {note.clinician?.first_name} {note.clinician?.last_name}
            </div>
            
            <div className="flex items-center space-x-2">
              {note.is_draft && (
                <span className="px-2 py-1 text-xs bg-yellow-100 text-yellow-800 rounded">
                  Draft
                </span>
              )}
              {note.is_signed && (
                <span className="px-2 py-1 text-xs bg-green-100 text-green-800 rounded flex items-center">
                  <Lock className="h-3 w-3 mr-1" />
                  Signed
                </span>
              )}
              <button
                onClick={() => onView(note)}
                className="text-blue-600 hover:text-blue-800"
              >
                <Eye className="h-4 w-4" />
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default NoteListItem;
