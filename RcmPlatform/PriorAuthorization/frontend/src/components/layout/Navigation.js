// File: src/components/layout/Navigation.js - Navigation Component
import React from 'react';
import { useLocation, Link } from 'react-router-dom';
import { FileText, CheckCircle, User, Clock } from 'lucide-react';

const Navigation = () => {
  const location = useLocation();
  
  const navItems = [
    { path: '/', name: 'Dashboard', icon: FileText },
    { path: '/prior-authorization', name: 'Prior Authorization', icon: CheckCircle },
    { path: '/patient-information', name: 'Patient Information', icon: User },
    { path: '/history', name: 'Request History', icon: Clock }
  ];

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 mt-6">
      <div className="border-b border-gray-200">
        <nav className="-mb-px flex space-x-8">
          {navItems.map(({ path, name, icon: Icon }) => (
            <Link
              key={path}
              to={path}
              className={`flex items-center py-2 px-1 border-b-2 font-medium text-sm ${
                location.pathname === path
                  ? 'border-purple-500 text-purple-600'
                  : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
              }`}
            >
              <Icon className="h-4 w-4 mr-2" />
              {name}
            </Link>
          ))}
        </nav>
      </div>
    </div>
  );
};

export default Navigation;

