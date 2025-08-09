import React from 'react';
import { Calendar, User, Clock, Eye, Edit, MoreVertical, Lock } from 'lucide-react';

const NoteCard = ({ note, isSelected, onSelect, onView, onEdit }) => {
  return (
    <div className={`bg-white rounded-lg shadow border transition-all ${
      isSelected ? 'border-blue-500 ring-2 ring-blue-200' : 'border-gray-200 hover:shadow-md'
    }`}>
      <div className="p-4">
        <div className="flex items-start justify-between">
          <div className="flex items-start space-x-3">
            <input
              type="checkbox"
              checked={isSelected}
              onChange={() => onSelect(note.id)}
              className="mt-1"
            />
            <div className="flex-1">
              <div className="flex items-center space-x-2 mb-2">
                <h3 className="font-medium text-gray-900">
                  {note.patient?.first_name} {note.patient?.last_name}
                </h3>
                <span className="px-2 py-1 text-xs bg-blue-100 text-blue-800 rounded">
                  {note.note_type}
                </span>
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
              </div>
              
              <div className="text-sm text-gray-600 space-y-1">
                <div className="flex items-center">
                  <Calendar className="h-4 w-4 mr-1" />
                  Session: {new Date(note.session_date).toLocaleDateString()}
                </div>
                <div className="flex items-center">
                  <User className="h-4 w-4 mr-1" />
                  {note.clinician?.first_name} {note.clinician?.last_name}
                </div>
                <div className="flex items-center">
                  <Clock className="h-4 w-4 mr-1" />
                  Created: {new Date(note.created_at).toLocaleDateString()}
                </div>
              </div>

              {/* Note Preview */}
              <div className="mt-3 p-2 bg-gray-50 rounded text-sm text-gray-700">
                {Object.entries(note.content || {}).slice(0, 2).map(([key, value]) => (
                  <div key={key} className="truncate">
                    <span className="font-medium capitalize">{key}:</span> {String(value).substring(0, 100)}...
                  </div>
                ))}
              </div>
            </div>
          </div>
          
          <div className="flex items-center space-x-2">
            <button
              onClick={() => onView(note)}
              className="p-2 text-gray-400 hover:text-blue-600"
              title="View Note"
            >
              <Eye className="h-4 w-4" />
            </button>
            {!note.is_locked && (
              <button
                onClick={() => onEdit(note)}
                className="p-2 text-gray-400 hover:text-green-600"
                title="Edit Note"
              >
                <Edit className="h-4 w-4" />
              </button>
            )}
            <button className="p-2 text-gray-400 hover:text-gray-600">
              <MoreVertical className="h-4 w-4" />
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default NoteCard;
