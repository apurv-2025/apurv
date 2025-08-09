import React, { useState } from 'react';
import { ArrowLeft } from 'lucide-react';
import PatientsList from '../components/patients/PatientsList';
import PatientForm from '../components/patients/PatientForm';

const PatientsPage = ({ onCreatePatient, onUpdatePatient }) => {
  const [currentView, setCurrentView] = useState('list');
  const [selectedPatient, setSelectedPatient] = useState(null);

  const handleCreatePatient = async (patientData) => {
    await onCreatePatient(patientData);
    setCurrentView('list');
    setSelectedPatient(null);
  };

  const handleUpdatePatient = async (patientData) => {
    await onUpdatePatient(patientData);
    setCurrentView('list');
    setSelectedPatient(null);
  };

  const handleSelectPatient = (patient) => {
    setSelectedPatient(patient);
    setCurrentView('form');
  };

  const handleCreateNewPatient = () => {
    setSelectedPatient(null);
    setCurrentView('form');
  };

  if (currentView === 'form') {
    return (
      <div>
        <div className="p-6">
          <button
            onClick={() => setCurrentView('list')}
            className="mb-4 text-blue-600 hover:text-blue-800 flex items-center"
          >
            <ArrowLeft className="h-4 w-4 mr-1" />
            Back to Patients
          </button>
        </div>
        <PatientForm
          patient={selectedPatient}
          onSave={selectedPatient ? handleUpdatePatient : handleCreatePatient}
          onCancel={() => setCurrentView('list')}
          mode={selectedPatient ? 'edit' : 'create'}
        />
      </div>
    );
  }

  return (
    <PatientsList
      onSelectPatient={handleSelectPatient}
      onCreatePatient={handleCreateNewPatient}
    />
  );
};

export default PatientsPage;
