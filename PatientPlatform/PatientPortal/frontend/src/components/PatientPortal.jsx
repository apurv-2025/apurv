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
import Fitness from './Fitness';
import Wellness from './Wellness';
import Settings from './Settings';
import Results from './Results';
import Prescriptions from './Prescriptions';
import Records from './Records';
import Billing from './Billing';
import FormsUploads from './FormsUploads';
import Telehealth from './Telehealth';
import Help from './Help';
import SurveyManagement from './SurveyManagement';
import { useAuth } from '../contexts/AuthContext';

const PatientPortal = () => {
  const [activeTab, setActiveTab] = useState('dashboard');
  const [searchTerm, setSearchTerm] = useState('');
  const { logout } = useAuth();

  const handleTabChange = (tab) => {
    setActiveTab(tab);
  };

  const handleSearchChange = (term) => {
    setSearchTerm(term);
    // TODO: Implement search functionality across components
    console.log('Search term:', term);
  };

  const handleLogout = () => {
    logout();
  };

  const renderContent = () => {
    switch (activeTab) {
      case 'dashboard':
        return <Dashboard />;
      case 'appointments':
        return <Appointments />;
      case 'messages':
        return <Messages />;
      case 'results':
        return <Results />;
      case 'prescriptions':
        return <Prescriptions />;
      case 'billing':
        return <Billing />;
      case 'records':
        return <Records />;
      case 'forms':
        return <FormsUploads />;
      case 'telehealth':
        return <Telehealth />;
      case 'medications':
        return <Medications />;
      case 'lab-results':
        return <LabResults />;
      case 'fitness':
        return <Fitness />;
      case 'wellness':
        return <Wellness />;
      case 'surveys':
        return <SurveyManagement />;
      case 'agent':
        return <Agent />;
      case 'profile':
        return <Profile />;
      case 'settings':
        return <Settings />;
      case 'help':
        return <Help />;
      default:
        return <Dashboard />;
    }
  };

  return (
    <div className="flex h-screen bg-gray-50">
      <Sidebar activeTab={activeTab} setActiveTab={setActiveTab} onLogout={handleLogout} />
      <div className="flex-1 ml-64 flex flex-col">
        <Header 
        activeTab={activeTab} 
        onTabChange={handleTabChange}
        onSearchChange={handleSearchChange}
      />
        <main className="flex-1 p-6 overflow-y-auto">
          {renderContent()}
        </main>
      </div>
    </div>
  );
};

export default PatientPortal; 