import React, { useState, useEffect } from 'react';
import { 
  Save, 
  FileText, 
  Calendar, 
  User, 
  Clock,
  AlertCircle,
  CheckCircle,
  Upload,
  X,
  Edit,
  Lock
} from 'lucide-react';

// Note Template Components
const SOAPNoteTemplate = ({ content, onChange, isReadOnly }) => {
  const handleFieldChange = (field, value) => {
    onChange({ ...content, [field]: value });
  };

  return (
    <div className="space-y-6">
      <div>
        <label className="block text-sm font-medium text-gray-700 mb-2">
          Subjective
        </label>
        <textarea
          value={content.subjective || ''}
          onChange={(e) => handleFieldChange('subjective', e.target.value)}
          disabled={isReadOnly}
          rows={4}
          className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 disabled:bg-gray-100"
          placeholder="Patient's subjective report, symptoms, concerns..."
        />
      </div>
      
      <div>
        <label className="block text-sm font-medium text-gray-700 mb-2">
          Objective
        </label>
        <textarea
          value={content.objective || ''}
          onChange={(e) => handleFieldChange('objective', e.target.value)}
          disabled={isReadOnly}
          rows={4}
          className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 disabled:bg-gray-100"
          placeholder="Observable data, mental status exam, behavioral observations..."
        />
      </div>
      
      <div>
        <label className="block text-sm font-medium text-gray-700 mb-2">
          Assessment
        </label>
        <textarea
          value={content.assessment || ''}
          onChange={(e) => handleFieldChange('assessment', e.target.value)}
          disabled={isReadOnly}
          rows={4}
          className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 disabled:bg-gray-100"
          placeholder="Clinical impressions, diagnosis, progress evaluation..."
        />
      </div>
      
      <div>
        <label className="block text-sm font-medium text-gray-700 mb-2">
          Plan
        </label>
        <textarea
          value={content.plan || ''}
          onChange={(e) => handleFieldChange('plan', e.target.value)}
          disabled={isReadOnly}
          rows={4}
          className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 disabled:bg-gray-100"
          placeholder="Treatment plan, interventions, next steps, homework..."
        />
      </div>
    </div>
  );
};

const DAPNoteTemplate = ({ content, onChange, isReadOnly }) => {
  const handleFieldChange = (field, value) => {
    onChange({ ...content, [field]: value });
  };

  return (
    <div className="space-y-6">
      <div>
        <label className="block text-sm font-medium text-gray-700 mb-2">
          Data
        </label>
        <textarea
          value={content.data || ''}
          onChange={(e) => handleFieldChange('data', e.target.value)}
          disabled={isReadOnly}
          rows={5}
          className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 disabled:bg-gray-100"
          placeholder="Factual information about the session, what was observed and discussed..."
        />
      </div>
      
      <div>
        <label className="block text-sm font-medium text-gray-700 mb-2">
          Assessment
        </label>
        <textarea
          value={content.assessment || ''}
          onChange={(e) => handleFieldChange('assessment', e.target.value)}
          disabled={isReadOnly}
          rows={4}
          className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 disabled:bg-gray-100"
          placeholder="Professional interpretation of the data, progress analysis..."
        />
      </div>
      
      <div>
        <label className="block text-sm font-medium text-gray-700 mb-2">
          Plan
        </label>
        <textarea
          value={content.plan || ''}
          onChange={(e) => handleFieldChange('plan', e.target.value)}
          disabled={isReadOnly}
          rows={4}
          className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 disabled:bg-gray-100"
          placeholder="Next steps, interventions, goals for future sessions..."
        />
      </div>
    </div>
  );
};

const BIRPNoteTemplate = ({ content, onChange, isReadOnly }) => {
  const handleFieldChange = (field, value) => {
    onChange({ ...content, [field]: value });
  };

  return (
    <div className="space-y-6">
      <div>
        <label className="block text-sm font-medium text-gray-700 mb-2">
          Behavior
        </label>
        <textarea
          value={content.behavior || ''}
          onChange={(e) => handleFieldChange('behavior', e.target.value)}
          disabled={isReadOnly}
          rows={4}
          className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 disabled:bg-gray-100"
          placeholder="Client behaviors observed during session..."
        />
      </div>
      
      <div>
        <label className="block text-sm font-medium text-gray-700 mb-2">
          Intervention
        </label>
        <textarea
          value={content.intervention || ''}
          onChange={(e) => handleFieldChange('intervention', e.target.value)}
          disabled={isReadOnly}
          rows={4}
          className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 disabled:bg-gray-100"
          placeholder="Therapeutic interventions used during session..."
        />
      </div>
      
      <div>
        <label className="block text-sm font-medium text-gray-700 mb-2">
          Response
        </label>
        <textarea
          value={content.response || ''}
          onChange={(e) => handleFieldChange('response', e.target.value)}
          disabled={isReadOnly}
          rows={4}
          className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 disabled:bg-gray-100"
          placeholder="Client's response to interventions..."
        />
      </div>
      
      <div>
        <label className="block text-sm font-medium text-gray-700 mb-2">
          Plan
        </label>
        <textarea
          value={content.plan || ''}
          onChange={(e) => handleFieldChange('plan', e.target.value)}
          disabled={isReadOnly}
          rows={4}
          className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 disabled:bg-gray-100"
          placeholder="Plans for future sessions and goals..."
        />
      </div>
    </div>
  );
};

const PAIPNoteTemplate = ({ content, onChange, isReadOnly }) => {
  const handleFieldChange = (field, value) => {
    onChange({ ...content, [field]: value });
  };

  return (
    <div className="space-y-6">
      <div>
        <label className="block text-sm font-medium text-gray-700 mb-2">
          Problem
        </label>
        <textarea
          value={content.problem || ''}
          onChange={(e) => handleFieldChange('problem', e.target.value)}
          disabled={isReadOnly}
          rows={4}
          className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 disabled:bg-gray-100"
          placeholder="Identified problems and issues addressed..."
        />
      </div>
      
      <div>
        <label className="block text-sm font-medium text-gray-700 mb-2">
          Assessment
        </label>
        <textarea
          value={content.assessment || ''}
          onChange={(e) => handleFieldChange('assessment', e.target.value)}
          disabled={isReadOnly}
          rows={4}
          className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 disabled:bg-gray-100"
          placeholder="Clinical assessment of the problems..."
        />
      </div>
      
      <div>
        <label className="block text-sm font-medium text-gray-700 mb-2">
          Intervention
        </label>
        <textarea
          value={content.intervention || ''}
          onChange={(e) => handleFieldChange('intervention', e.target.value)}
          disabled={isReadOnly}
          rows={4}
          className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 disabled:bg-gray-100"
          placeholder="Interventions and therapeutic techniques used..."
        />
      </div>
      
      <div>
        <label className="block text-sm font-medium text-gray-700 mb-2">
          Plan
        </label>
        <textarea
          value={content.plan || ''}
          onChange={(e) => handleFieldChange('plan', e.target.value)}
          disabled={isReadOnly}
          rows={4}
          className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 disabled:bg-gray-100"
          placeholder="Treatment plan and next steps..."
        />
      </div>
    </div>
  );
};

// Note Editor Component
const NoteEditor = ({ note, onSave, onCancel, patients, mode = 'create' }) => {
  const [formData, setFormData] = useState({
    patient_id: note?.patient_id || '',
    note_type: note?.note_type || 'SOAP',
    session_date: note?.session_date ? new Date(note.session_date).toISOString().slice(0, 16) : '',
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
          await saveDraft();
          setLastSaved(new Date());
          setHasUnsavedChanges(false);
        } catch (err) {
          console.error('Auto-save failed:', err);
        }
      }, 2000);

      return () => clearTimeout(timer);
    }
  }, [formData.content, hasUnsavedChanges]);

  const saveDraft = async () => {
    if (!note?.id) return;
    
    const API_BASE_URL = 'http://localhost:8000';
    const token = localStorage.getItem('access_token');
    
    await fetch(`${API_BASE_URL}/notes/${note.id}/draft`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        Authorization: `Bearer ${token}`,
      },
      body: JSON.stringify({ content: formData.content }),
    });
  };

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
    const templateProps = {
      content: formData.content,
      onChange: handleContentChange,
      isReadOnly
    };

    switch (formData.note_type) {
      case 'SOAP':
        return <SOAPNoteTemplate {...templateProps} />;
      case 'DAP':
        return <DAPNoteTemplate {...templateProps} />;
      case 'BIRP':
        return <BIRPNoteTemplate {...templateProps} />;
      case 'PAIP':
        return <PAIPNoteTemplate {...templateProps} />;
      default:
        return <SOAPNoteTemplate {...templateProps} />;
    }
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
          {error && (
            <div className="mb-6 bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded flex items-center">
              <AlertCircle className="h-4 w-4 mr-2" />
              {error}
            </div>
          )}

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
                <option value="SOAP">SOAP Note</option>
                <option value="DAP">DAP Note</option>
                <option value="BIRP">BIRP Note</option>
                <option value="PAIP">PAIP Note</option>
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
                <>
                  <button
                    type="button"
                    onClick={handleSubmit}
                    disabled={saving}
                    className="px-6 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 disabled:opacity-50 flex items-center"
                  >
                    <Save className="h-4 w-4 mr-2" />
                    {saving ? 'Saving...' : mode === 'create' ? 'Create Note' : 'Update Note'}
                  </button>
                </>
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

// Note Viewer Component
const NoteViewer = ({ note, onEdit, onSign, onUnlock, canEdit, canSign, canUnlock }) => {
  const [showSignModal, setShowSignModal] = useState(false);
  const [showUnlockModal, setShowUnlockModal] = useState(false);
  const [unlockReason, setUnlockReason] = useState('');
  const [signing, setSigning] = useState(false);
  const [unlocking, setUnlocking] = useState(false);

  const handleSign = async () => {
    setSigning(true);
    try {
      await onSign(note.id);
      setShowSignModal(false);
    } catch (error) {
      console.error('Error signing note:', error);
    } finally {
      setSigning(false);
    }
  };

  const handleUnlock = async () => {
    if (!unlockReason.trim()) return;
    
    setUnlocking(true);
    try {
      await onUnlock(note.id, unlockReason);
      setShowUnlockModal(false);
      setUnlockReason('');
    } catch (error) {
      console.error('Error unlocking note:', error);
    } finally {
      setUnlocking(false);
    }
  };

  const renderNoteContent = () => {
    const content = note.content || {};
    
    switch (note.note_type) {
      case 'SOAP':
        return (
          <div className="space-y-6">
            <div>
              <h4 className="font-medium text-gray-900 mb-2">Subjective</h4>
              <p className="text-gray-700 whitespace-pre-wrap">{content.subjective || 'No content'}</p>
            </div>
            <div>
              <h4 className="font-medium text-gray-900 mb-2">Objective</h4>
              <p className="text-gray-700 whitespace-pre-wrap">{content.objective || 'No content'}</p>
            </div>
            <div>
              <h4 className="font-medium text-gray-900 mb-2">Assessment</h4>
              <p className="text-gray-700 whitespace-pre-wrap">{content.assessment || 'No content'}</p>
            </div>
            <div>
              <h4 className="font-medium text-gray-900 mb-2">Plan</h4>
              <p className="text-gray-700 whitespace-pre-wrap">{content.plan || 'No content'}</p>
            </div>
          </div>
        );
      case 'DAP':
        return (
          <div className="space-y-6">
            <div>
              <h4 className="font-medium text-gray-900 mb-2">Data</h4>
              <p className="text-gray-700 whitespace-pre-wrap">{content.data || 'No content'}</p>
            </div>
            <div>
              <h4 className="font-medium text-gray-900 mb-2">Assessment</h4>
              <p className="text-gray-700 whitespace-pre-wrap">{content.assessment || 'No content'}</p>
            </div>
            <div>
              <h4 className="font-medium text-gray-900 mb-2">Plan</h4>
              <p className="text-gray-700 whitespace-pre-wrap">{content.plan || 'No content'}</p>
            </div>
          </div>
        );
      default:
        return <pre className="text-gray-700 whitespace-pre-wrap">{JSON.stringify(content, null, 2)}</pre>;
    }
  };

  return (
    <div className="max-w-4xl mx-auto p-6">
      <div className="bg-white rounded-lg shadow">
        {/* Header */}
        <div className="px-6 py-4 border-b border-gray-200">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-3">
              <FileText className="h-6 w-6 text-blue-600" />
              <div>
                <h1 className="text-xl font-bold text-gray-900">Progress Note</h1>
                <p className="text-sm text-gray-600">
                  {note.patient?.first_name} {note.patient?.last_name} - {note.note_type}
                </p>
              </div>
            </div>
            
            <div className="flex items-center space-x-2">
              {note.is_draft && (
                <span className="px-2 py-1 text-xs bg-yellow-100 text-yellow-800 rounded">
                  Draft
                </span>
              )}
              {note.is_signed && (
                <span className="px-2 py-1 text-xs bg-green-100 text-green-800 rounded">
                  Signed
                </span>
              )}
              {note.is_locked && (
                <Lock className="h-4 w-4 text-green-600" />
              )}
            </div>
          </div>
        </div>

        {/* Note Information */}
        <div className="px-6 py-4 bg-gray-50 border-b border-gray-200">
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4 text-sm">
            <div>
              <span className="font-medium text-gray-700">Session Date:</span>
              <p className="text-gray-900">{new Date(note.session_date).toLocaleDateString()}</p>
              <p className="text-gray-600">{new Date(note.session_date).toLocaleTimeString()}</p>
            </div>
            <div>
              <span className="font-medium text-gray-700">Clinician:</span>
              <p className="text-gray-900">{note.clinician?.first_name} {note.clinician?.last_name}</p>
            </div>
            <div>
              <span className="font-medium text-gray-700">Created:</span>
              <p className="text-gray-900">{new Date(note.created_at).toLocaleDateString()}</p>
            </div>
            <div>
              <span className="font-medium text-gray-700">Version:</span>
              <p className="text-gray-900">{note.version}</p>
            </div>
          </div>
        </div>

        {/* Note Content */}
        <div className="p-6">
          <h2 className="text-lg font-medium text-gray-900 mb-4">Note Content</h2>
          {renderNoteContent()}
        </div>

        {/* Actions */}
        <div className="px-6 py-4 border-t border-gray-200 flex justify-between">
          <div className="text-xs text-gray-500">
            {note.signed_at && (
              <p>Signed on {new Date(note.signed_at).toLocaleString()}</p>
            )}
            {note.unlock_reason && (
              <p>Unlocked: {note.unlock_reason}</p>
            )}
          </div>
          
          <div className="flex space-x-3">
            {canEdit && !note.is_locked && (
              <button
                onClick={() => onEdit(note)}
                className="px-4 py-2 text-blue-600 border border-blue-600 rounded-md hover:bg-blue-50"
              >
                <Edit className="h-4 w-4 mr-2 inline" />
                Edit
              </button>
            )}
            
            {canSign && !note.is_signed && (
              <button
                onClick={() => setShowSignModal(true)}
                className="px-4 py-2 bg-green-600 text-white rounded-md hover:bg-green-700"
              >
                Sign Note
              </button>
            )}
            
            {canUnlock && note.is_locked && (
              <button
                onClick={() => setShowUnlockModal(true)}
                className="px-4 py-2 bg-orange-600 text-white rounded-md hover:bg-orange-700"
              >
                Unlock Note
              </button>
            )}
          </div>
        </div>
      </div>

      {/* Sign Modal */}
      {showSignModal && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-white rounded-lg p-6 w-full max-w-md">
            <h3 className="text-lg font-medium text-gray-900 mb-4">Sign Progress Note</h3>
            <p className="text-gray-600 mb-6">
              By signing this note, you certify that the information is accurate and complete. 
              Once signed, the note will be locked and require supervisor approval to unlock.
            </p>
            <div className="flex justify-end space-x-3">
              <button
                onClick={() => setShowSignModal(false)}
                className="px-4 py-2 text-gray-700 border border-gray-300 rounded-md hover:bg-gray-50"
              >
                Cancel
              </button>
              <button
                onClick={handleSign}
                disabled={signing}
                className="px-4 py-2 bg-green-600 text-white rounded-md hover:bg-green-700 disabled:opacity-50"
              >
                {signing ? 'Signing...' : 'Sign Note'}
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Unlock Modal */}
      {showUnlockModal && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-white rounded-lg p-6 w-full max-w-md">
            <h3 className="text-lg font-medium text-gray-900 mb-4">Unlock Progress Note</h3>
            <p className="text-gray-600 mb-4">
              Please provide a reason for unlocking this signed note:
            </p>
            <textarea
              value={unlockReason}
              onChange={(e) => setUnlockReason(e.target.value)}
              rows={3}
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 mb-4"
              placeholder="Reason for unlocking..."
            />
            <div className="flex justify-end space-x-3">
              <button
                onClick={() => setShowUnlockModal(false)}
                className="px-4 py-2 text-gray-700 border border-gray-300 rounded-md hover:bg-gray-50"
              >
                Cancel
              </button>
              <button
                onClick={handleUnlock}
                disabled={unlocking || !unlockReason.trim()}
                className="px-4 py-2 bg-orange-600 text-white rounded-md hover:bg-orange-700 disabled:opacity-50"
              >
                {unlocking ? 'Unlocking...' : 'Unlock Note'}
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export { NoteEditor, NoteViewer, SOAPNoteTemplate, DAPNoteTemplate, BIRPNoteTemplate, PAIPNoteTemplate };
