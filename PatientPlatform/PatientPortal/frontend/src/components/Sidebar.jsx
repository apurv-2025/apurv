import React from 'react';
import { Heart, Activity, Calendar, Pill, TestTube, Mail, User, Settings, LogOut } from 'lucide-react';

const Sidebar = ({ activeTab, setActiveTab, onLogout }) => {
  const menuItems = [
    { id: 'dashboard', label: 'Dashboard', icon: Activity },
    { id: 'appointments', label: 'Appointments', icon: Calendar },
    { id: 'medications', label: 'Medications', icon: Pill },
    { id: 'lab-results', label: 'Lab Results', icon: TestTube },
    { id: 'messages', label: 'Messages', icon: Mail },
    { id: 'profile', label: 'Profile', icon: User },
    { id: 'settings', label: 'Settings', icon: Settings }
  ];

  return (
    <div className="w-64 bg-white shadow-lg h-screen fixed left-0 top-0 overflow-y-auto">
      <div className="p-6 border-b border-gray-200">
        <div className="flex items-center space-x-3">
          <div className="w-10 h-10 bg-blue-600 rounded-full flex items-center justify-center">
            <Heart className="w-6 h-6 text-white" />
          </div>
          <h1 className="text-xl font-bold text-gray-800">HealthPortal</h1>
        </div>
      </div>

      <nav className="mt-6">
        {menuItems.map(({ id, label, icon: Icon }) => (
          <button
            key={id}
            onClick={() => setActiveTab(id)}
            className={`w-full flex items-center space-x-3 px-6 py-3 text-left hover:bg-blue-50 transition-colors ${
              activeTab === id ? 'bg-blue-50 border-r-4 border-blue-600 text-blue-600' : 'text-gray-700'
            }`}
          >
            <Icon className="w-5 h-5" />
            <span>{label}</span>
          </button>
        ))}
      </nav>

      <div className="absolute bottom-6 left-6 right-6">
        <button 
          onClick={onLogout}
          className="w-full flex items-center space-x-3 px-4 py-2 text-gray-700 hover:bg-gray-100 rounded-lg transition-colors"
        >
          <LogOut className="w-5 h-5" />
          <span>Sign Out</span>
        </button>
      </div>
    </div>
  );
};

export default Sidebar; 