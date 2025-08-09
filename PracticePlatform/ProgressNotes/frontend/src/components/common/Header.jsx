import React from 'react';
import { User, LogOut } from 'lucide-react';
import { useAuth } from '../../hooks/useAuth';

const Header = ({ currentView, setCurrentView, onLogout }) => {
  const { user } = useAuth();

  const navItems = [
    { key: 'dashboard', label: 'Dashboard' },
    { key: 'notes', label: 'Progress Notes' },
    { key: 'patients', label: 'Patients' }
  ];

  return (
    <header className="bg-white shadow">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center py-6">
          <div className="flex items-center">
            <h1 className="text-xl font-bold text-gray-900">Mental Health Practice</h1>
            <nav className="ml-10 flex space-x-8">
              {navItems.map(({ key, label }) => (
                <button
                  key={key}
                  onClick={() => setCurrentView(key)}
                  className={`px-3 py-2 rounded-md text-sm font-medium ${
                    currentView === key || currentView.startsWith(key)
                      ? 'bg-blue-100 text-blue-700' 
                      : 'text-gray-500 hover:text-gray-700'
                  }`}
                >
                  {label}
                </button>
              ))}
            </nav>
          </div>
          
          <div className="flex items-center space-x-4">
            <div className="flex items-center space-x-2">
              <User className="h-4 w-4 text-gray-500" />
              <span className="text-sm text-gray-700">
                {user?.first_name} {user?.last_name}
              </span>
              <span className="px-2 py-1 text-xs bg-gray-100 text-gray-600 rounded">
                {user?.role}
              </span>
            </div>
            <button
              onClick={onLogout}
              className="flex items-center space-x-1 text-gray-500 hover:text-gray-700"
            >
              <LogOut className="h-4 w-4" />
              <span className="text-sm">Logout</span>
            </button>
          </div>
        </div>
      </div>
    </header>
  );
};

export default Header;
