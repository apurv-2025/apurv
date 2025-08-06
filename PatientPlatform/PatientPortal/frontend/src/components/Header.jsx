import React from 'react';
import { User, Bell } from 'lucide-react';
import { useAuth } from '../contexts/AuthContext';

const Header = ({ activeTab }) => {
  const { user } = useAuth();

  return (
    <div className="bg-white shadow-sm border-b border-gray-200 px-6 py-4 sticky top-0 z-10">
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-2xl font-bold text-gray-800 capitalize">
            {activeTab.replace('-', ' ')}
          </h2>
          <p className="text-gray-600">Welcome back, {user?.first_name || 'User'}</p>
        </div>
        <div className="flex items-center space-x-4">
          <button className="relative p-2 text-gray-600 hover:text-gray-800 hover:bg-gray-100 rounded-full transition-colors">
            <Bell className="w-6 h-6" />
            <span className="absolute -top-1 -right-1 w-3 h-3 bg-red-500 rounded-full"></span>
          </button>
          <div className="w-8 h-8 bg-gray-300 rounded-full flex items-center justify-center hover:bg-gray-400 transition-colors cursor-pointer">
            <User className="w-5 h-5 text-gray-600" />
          </div>
        </div>
      </div>
    </div>
  );
};

export default Header; 