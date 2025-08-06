import React, { useState } from 'react';
import Sidebar from './Sidebar';
import Header from './Header';
import Dashboard from './Dashboard';
import Appointments from './Appointments';
import Medications from './Medications';
import LabResults from './LabResults';
import Messages from './Messages';
import Profile from './Profile';
import Agent from './Agent';
import { useAuth } from '../contexts/AuthContext';

const PatientPortal = () => {
  const [activeTab, setActiveTab] = useState('dashboard');
  const { logout } = useAuth();

  const handleLogout = () => {
    logout();
  };

  const renderContent = () => {
    switch (activeTab) {
      case 'dashboard':
        return <Dashboard />;
      case 'appointments':
        return <Appointments />;
      case 'medications':
        return <Medications />;
      case 'lab-results':
        return <LabResults />;
      case 'messages':
        return <Messages />;
      case 'agent':
        return <Agent />;
      case 'profile':
        return <Profile />;
      default:
        return <Dashboard />;
    }
  };

  return (
    <div className="flex h-screen bg-gray-50">
      <Sidebar activeTab={activeTab} setActiveTab={setActiveTab} onLogout={handleLogout} />
      <div className="flex-1 ml-64 flex flex-col">
        <Header activeTab={activeTab} />
        <main className="flex-1 p-6 overflow-y-auto">
          {renderContent()}
        </main>
      </div>
    </div>
  );
};

export default PatientPortal; 