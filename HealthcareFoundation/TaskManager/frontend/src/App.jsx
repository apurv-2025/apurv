// src/App.jsx (Corrected with proper imports)
import React, { useState } from 'react';
import Sidebar from './components/Layout/Sidebar';
import Header from './components/Layout/Header';
import TasksView from './components/Tasks/TasksView';
import ClientsView from './components/Clients/ClientsView';
import SettingsView from './components/Settings/SettingsView';
import Toast from './components/UI/Toast';
import { ToastProvider, useToast } from './context/ToastContext';

const AppContent = () => {
  const [activeView, setActiveView] = useState('tasks');
  const [sidebarCollapsed, setSidebarCollapsed] = useState(false);
  const { toasts, removeToast } = useToast();

  const renderContent = () => {
    switch (activeView) {
      case 'tasks':
        return <TasksView />;
      case 'clients':
        return <ClientsView />;
      case 'settings':
        return <SettingsView />;
      case 'calendar':
        return (
          <div className="p-6 text-center">
            <h2 className="text-xl font-semibold mb-4">Calendar View</h2>
            <p className="text-gray-600">Calendar integration coming soon...</p>
          </div>
        );
      case 'analytics':
        return (
          <div className="p-6 text-center">
            <h2 className="text-xl font-semibold mb-4">Analytics</h2>
            <p className="text-gray-600">Analytics dashboard coming soon...</p>
          </div>
        );
      default:
        return <TasksView />;
    }
  };

  return (
    <div className="flex h-screen bg-gray-50">
      <Sidebar
        activeView={activeView}
        onViewChange={setActiveView}
        collapsed={sidebarCollapsed}
        onToggleCollapse={() => setSidebarCollapsed(!sidebarCollapsed)}
      />
      
      <div className="flex-1 flex flex-col overflow-hidden">
        <Header
          currentView={activeView}
          onSidebarToggle={() => setSidebarCollapsed(!sidebarCollapsed)}
        />
        
        <main className="flex-1 overflow-auto">
          {renderContent()}
        </main>
      </div>
      
      <Toast toasts={toasts} onRemove={removeToast} />
    </div>
  );
};

const App = () => {
  return (
    <ToastProvider>
      <AppContent />
    </ToastProvider>
  );
};

export default App;
