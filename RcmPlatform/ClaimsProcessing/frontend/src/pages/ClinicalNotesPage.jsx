// src/pages/ClinicalNotesPage.jsx
import React, { useState } from 'react';
import { FileText, Plus } from 'lucide-react';
import ClinicalNoteForm from '../components/clinical/ClinicalNoteForm';
import ClinicalNoteList from '../components/clinical/ClinicalNoteList';
import ClaimForm from '../components/claims/ClaimForm';

const ClinicalNotesPage = () => {
  const [activeTab, setActiveTab] = useState('create');
  const [extractedCodes, setExtractedCodes] = useState(null);
  const [showClaimForm, setShowClaimForm] = useState(false);

  const handleNoteCreated = (note) => {
    if (note.processed_codes) {
      setExtractedCodes(note.processed_codes);
      setShowClaimForm(true);
    }
  };

  const handleClaimCreated = (claim) => {
    setShowClaimForm(false);
    setExtractedCodes(null);
    // Could show success message or redirect
  };

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      {/* Header */}
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900">Clinical Notes Processing</h1>
        <p className="mt-2 text-gray-600">
          Process clinical notes with AI-powered code extraction and create claims
        </p>
      </div>

      {/* Navigation Tabs */}
      <div className="border-b border-gray-200 mb-8">
        <nav className="flex space-x-8">
          <button
            onClick={() => setActiveTab('create')}
            className={`py-2 px-1 border-b-2 font-medium text-sm ${
              activeTab === 'create'
                ? 'border-blue-500 text-blue-600'
                : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
            }`}
          >
            <div className="flex items-center space-x-2">
              <Plus size={18} />
              <span>Create Note</span>
            </div>
          </button>
          <button
            onClick={() => setActiveTab('list')}
            className={`py-2 px-1 border-b-2 font-medium text-sm ${
              activeTab === 'list'
                ? 'border-blue-500 text-blue-600'
                : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
            }`}
          >
            <div className="flex items-center space-x-2">
              <FileText size={18} />
              <span>All Notes</span>
            </div>
          </button>
        </nav>
      </div>

      {/* Content */}
      <div className="space-y-8">
        {activeTab === 'create' && (
          <>
            <ClinicalNoteForm onNoteCreated={handleNoteCreated} />
            
            {showClaimForm && extractedCodes && (
              <div className="border-t border-gray-200 pt-8">
                <div className="mb-4">
                  <h2 className="text-xl font-semibold text-gray-900">
                    Create Claim from Extracted Codes
                  </h2>
                  <p className="text-gray-600">
                    The AI has extracted medical codes. You can now create a claim.
                  </p>
                </div>
                <ClaimForm 
                  extractedCodes={extractedCodes} 
                  onClaimCreated={handleClaimCreated}
                />
              </div>
            )}
          </>
        )}

        {activeTab === 'list' && <ClinicalNoteList />}
      </div>
    </div>
  );
};

export default ClinicalNotesPage;
