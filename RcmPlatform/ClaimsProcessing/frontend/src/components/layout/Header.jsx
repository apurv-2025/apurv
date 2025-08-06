import React from 'react';
import { FileText } from 'lucide-react';

const Header = () => {
  return (
    <header className="bg-white shadow">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center py-6">
          <div className="flex items-center">
            <FileText className="w-8 h-8 text-blue-600 mr-3" />
            <h1 className="text-2xl font-bold text-gray-900">Claims Processing</h1>
          </div>
          <div className="flex items-center space-x-4">
            <span className="text-sm text-gray-500">Powered by Apurv RCM 1.0</span>
            <div className="w-2 h-2 bg-green-400 rounded-full"></div>
          </div>
        </div>
      </div>
    </header>
  );
};

export default Header;
