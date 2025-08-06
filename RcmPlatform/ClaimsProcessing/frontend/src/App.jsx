import React, { useState } from 'react';
import Header from './components/layout/Header';
import Navigation from './components/layout/Navigation';
import Dashboard from './pages/Dashboard';
import ClaimsList from './pages/ClaimsList';
import Upload from './pages/Upload';
import Agent from './pages/Agent';
import FloatingChatWidget from './components/agent/FloatingChatWidget';

const App = () => {
  const [activeTab, setActiveTab] = useState('dashboard');

  const renderContent = () => {
    switch (activeTab) {
      case 'dashboard':
        return <Dashboard />;
      case 'claims':
        return <ClaimsList />;
      case 'upload':
        return <Upload />;
      case 'agent':
        return <Agent />;
      default:
        return <Dashboard />;
    }
  };

  return (
    <div className="min-h-screen bg-gray-100">
      <Header />
      <Navigation activeTab={activeTab} onTabChange={setActiveTab} />
      
      <main className="max-w-7xl mx-auto py-6 px-4 sm:px-6 lg:px-8">
        {renderContent()}
      </main>

      {/* Floating AI Chat Widget */}
      <FloatingChatWidget />
    </div>
  );
};

export default App;
