// File: src/pages/PatientInformationPage.js - Patient Information Page
import React from 'react';
import PatientInformationForm from '../components/forms/PatientInformationForm';

const PatientInformationPage = () => {
  return (
    <div className="space-y-6">
      <div className="text-center">
        <h1 className="text-2xl font-bold text-gray-900 mb-2">
          Patient Information Management
        </h1>
        <p className="text-gray-600">
          Create and manage patient information with EDI 275 transactions
        </p>
      </div>

      <PatientInformationForm />
    </div>
  );
};

export default PatientInformationPage;
