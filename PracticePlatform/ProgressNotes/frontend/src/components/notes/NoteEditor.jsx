import React, { useState, useEffect } from 'react';
import { FileText, Lock, CheckCircle, Clock, Save, AlertCircle } from 'lucide-react';
import { NoteTemplates } from './templates';
import { NOTE_TYPES } from '../../utils/constants';
import { formatDateForInput } from '../../utils/helpers';
import APIService from '../../services/api';
import ErrorMessage from '../common/ErrorMessage';

const NoteEditor = ({ note, patients, onSave, onCancel, mode = 'create' }) => {
  const [formData, setFormData] = useState({
    patient_id: note?.patient_id || '',
    note_type: note?.note_type || NOTE_TYPES.SOAP,
    session_date: note?.session_date ? formatDateForInput(note.session_date) : '',
    content: note?.content || {}
  });
  
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState('');
  const [lastSaved, setLastSaved] = useState(null);
  const [hasUnsavedChanges, setHasUnsavedChanges] = useState(false);

  const isReadOnly = note?.is_signed && note?.is_locked;

  // Auto-save functionality
  useEffect(() => {
    if (mode === 'edit' && note?.id && hasUnsavedChanges && !isReadOnly) {
      const timer = setTimeout(async () => {
        try {
          await APIService.saveDraft(note.id, formData.content);
          setLastSaved(new Date());
          setHasUnsavedChanges(false);
        } catch (err) {
          console.error('Auto-save failed:', err);
        }
      }, 2000);

      return () => clearTimeout(timer);
    }
  }, [formData.content, hasUnsavedChanges, mode, note?.id, isReadOnly]);

  const handleContentChange = (newContent) => {
    setFormData(prev => ({ ...prev, content: newContent }));
    setHasUnsavedChanges(true);
  };

  const handleSubmit = async () => {
    if (!formData.patient_id || !formData.session_date) {
      setError('Please fill in all required fields');
      return;
    }

    setSaving(true);
    setError('');

    try {
      await onSave(formData);
    } catch (err) {
      setError('Failed to save note. Please try again.');
    } finally {
      setSaving(false);
    }
  };

  const renderNoteTemplate = () => {
    const TemplateComponent = NoteTemplates[formData.note_type] || NoteTemplates[NOTE_TYPES.SOAP];
    
    return (
      <TemplateComponent
        content={formData.content}
        onChange={handleContentChange}
        isReadOnly={isReadOnly}
      />
    );
  };

  return (
    <div className="max-w-4xl mx-auto p-6">
      <div className="bg-white rounded-lg shadow">
        {/* Header */}
        <div className="px-6 py-4 border-b border-gray-200">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-3">
              <FileText className="h-6 w-6 text-blue-600" />
              <h1 className="text-xl font-bold text-gray-900">
                {mode === 'create' ? 'Create New Progress Note' : 'Edit Progress Note'}
              </h1>
              {note?.is_signed && (
                <div className="flex items-center space-x-1 text-green-600">
                  <Lock className="h-4 w-4" />
                  <span className="text-sm">Signed</span>
                </div>
              )}
            </div>
            
            <div className="flex items-center space-x-3">
              {lastSaved && (
                <div className="flex items-center space-x-1 text-green-600 text-sm">
                  <CheckCircle className="h-4 w-4" />
                  <span>Saved {lastSaved.toLocaleTimeString()}</span>
                </div>
              )}
              {hasUnsavedChanges && (
                <div className="flex items-center space-x-1 text-yellow-600 text-sm">
                  <Clock className="h-4 w-4" />
                  <span>Auto-saving...</span>
                </div>
              )}
            </div>
          </div>
        </div>

        {/* Form */}
        <div className="p-6">
          {error && <ErrorMessage error={error} />}

          {/* Basic Information */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Patient *
              </label>
              <select
                value={formData.patient_id}
                onChange={(e) => setFormData(prev => ({ ...prev, patient_id: e.target.value }))}
                disabled={isReadOnly || mode === 'edit'}
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 disabled:bg-gray-100"
                required
              >
                <option value="">Select a patient</option>
                {patients?.map((patient) => (
                  <option key={patient.id} value={patient.id}>
                    {patient.first_name} {patient.last_name} - {patient.medical_record_number}
                  </option>
                ))}
              </select>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Note Type *
              </label>
              <select
                value={formData.note_type}
                onChange={(e) => setFormData(prev => ({ ...prev, note_type: e.target.value }))}
                disabled={isReadOnly}
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 disabled:bg-gray-100"
              >
                {Object.values(NOTE_TYPES).map(type => (
                  <option key={type} value={type}>{type} Note</option>
                ))}
              </select>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Session Date & Time *
              </label>
              <input
                type="datetime-local"
                value={formData.session_date}
                onChange={(e) => setFormData(prev => ({ ...prev, session_date: e.target.value }))}
                disabled={isReadOnly}
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 disabled:bg-gray-100"
                required
              />
            </div>
          </div>

          {/* Note Content */}
          <div className="mb-8">
            <h2 className="text-lg font-medium text-gray-900 mb-4">Note Content</h2>
            {renderNoteTemplate()}
          </div>

          {/* Actions */}
          <div className="flex items-center justify-between pt-6 border-t border-gray-200">
            <button
              type="button"
              onClick={onCancel}
              className="px-4 py-2 text-gray-700 bg-gray-100 hover:bg-gray-200 rounded-md transition-colors"
            >
              Cancel
            </button>

            <div className="flex space-x-3">
              {!isReadOnly && (
                <button
                  type="button"
                  onClick={handleSubmit}
                  disabled={saving}
                  className="px-6 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 disabled:opacity-50 flex items-center"
                >
                  <Save className="h-4 w-4 mr-2" />
                  {saving ? 'Saving...' : mode === 'create' ? 'Create Note' : 'Update Note'}
                </button>
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default NoteEditor;
