import React from 'react';
import { useAuth } from '../../contexts/AuthContext';
import { Bell, User, LogOut } from 'lucide-react';

const Header = () => {
  const { user, logout } = useAuth();

  return (
    <header className="bg-white shadow-sm border-b border-gray-200">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center h-16">
          {/* Logo */}
          <div className="flex items-center">
            <h1 className="text-xl font-semibold text-gray-900">
              AI-Native Scheduling
            </h1>
          </div>

          {/* Right side */}
          <div className="flex items-center space-x-4">
            {/* Notifications */}
            <button className="p-2 text-gray-400 hover:text-gray-500 focus:outline-none focus:ring-2 focus:ring-primary-500 rounded-md">
              <Bell className="h-5 w-5" />
            </button>

            {/* User menu */}
            <div className="relative">
              <button className="flex items-center space-x-2 text-sm text-gray-700 hover:text-gray-900 focus:outline-none focus:ring-2 focus:ring-primary-500 rounded-md p-2">
                <User className="h-5 w-5" />
                <span>{user?.first_name} {user?.last_name}</span>
              </button>
            </div>

            {/* Logout */}
            <button
              onClick={logout}
              className="flex items-center space-x-2 text-sm text-gray-700 hover:text-gray-900 focus:outline-none focus:ring-2 focus:ring-primary-500 rounded-md p-2"
            >
              <LogOut className="h-5 w-5" />
              <span>Logout</span>
            </button>
          </div>
        </div>
      </div>
    </header>
  );
};

export default Header; 