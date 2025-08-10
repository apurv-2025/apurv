// File: src/pages/PriorAuthorizationPage.js - Prior Authorization Page
import React from 'react';
import PriorAuthorizationForm from '../components/forms/PriorAuthorizationForm';

const PriorAuthorizationPage = () => {
  return (
    <div className="space-y-6">
      <div className="text-center">
        <h1 className="text-2xl font-bold text-gray-900 mb-2">
          Prior Authorization Request
        </h1>
        <p className="text-gray-600">
          Submit EDI 278 prior authorization requests for medical procedures and services
        </p>
      </div>

      <PriorAuthorizationForm />
    </div>
  );
};

export default PriorAuthorizationPage;
