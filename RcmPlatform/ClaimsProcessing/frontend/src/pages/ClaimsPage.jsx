// src/pages/ClaimsPage.jsx
import React, { useState } from 'react';
import { Send, List, Plus } from 'lucide-react';
import ClaimForm from '../components/claims/ClaimForm';
import ClaimList from '../components/claims/ClaimList';

const ClaimsPage = () => {
  const [activeTab, setActiveTab] = useState('list');

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      {/* Header */}
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900">Claims Management</h1>
        <p className="mt-2 text-gray-600">
          Create, submit, and manage 837P, 837I, and 837D claims
        </p>
      </div>

      {/* Navigation Tabs */}
      <div className="border-b border-gray-200 mb-8">
        <nav className="flex space-x-8">
          <button
            onClick={() => setActiveTab('list')}
            className={`py-2 px-1 border-b-2 font-medium text-sm ${
              activeTab === 'list'
                ? 'border-blue-500 text-blue-600'
                : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
            }`}
          >
            <div className="flex items-center space-x-2">
              <List size={18} />
              <span>All Claims</span>
            </div>
          </button>
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
              <span>Create Claim</span>
            </div>
          </button>
        </nav>
      </div>

      {/* Content */}
      <div className="space-y-8">
        {activeTab === 'list' && <ClaimList />}
        {activeTab === 'create' && (
          <ClaimForm onClaimCreated={() => setActiveTab('list')} />
        )}
      </div>
    </div>
  );
};

export default ClaimsPage;
