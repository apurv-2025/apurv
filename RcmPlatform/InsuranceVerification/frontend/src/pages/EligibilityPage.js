// File: src/pages/EligibilityPage.js
import React from 'react';
import EligibilityForm from '../components/eligibility/EligibilityForm';
import EligibilityResult from '../components/eligibility/EligibilityResult';
import { useApp } from '../contexts/AppContext';

const EligibilityPage = () => {
  const { eligibilityResult } = useApp();

  return (
    <div className="space-y-6">
      <div className="text-center">
        <h1 className="text-2xl font-bold text-gray-900 mb-2">
          Eligibility and Benefits Verification
        </h1>
        <p className="text-gray-600">
          Submit EDI 270 eligibility inquiries and receive EDI 271 responses
        </p>
      </div>

      <EligibilityForm />
      
      {eligibilityResult && <EligibilityResult result={eligibilityResult} />}
    </div>
  );
};

export default EligibilityPage;
