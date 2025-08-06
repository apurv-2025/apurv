import React from 'react';
import { Activity, FileText, Upload, Bot } from 'lucide-react';
import { NAVIGATION_TABS } from '../../utils/constants';

const Navigation = ({ activeTab, onTabChange }) => {
  const getIcon = (iconName) => {
    const icons = {
      Activity,
      FileText,
      Upload,
      Bot
    };
    return icons[iconName] || Activity;
  };

  return (
    <nav className="bg-white border-b">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex space-x-8">
          {NAVIGATION_TABS.map((tab) => {
            const Icon = getIcon(tab.icon);
            return (
              <button
                key={tab.id}
                onClick={() => onTabChange(tab.id)}
                className={`flex items-center px-3 py-4 text-sm font-medium border-b-2 transition-colors ${
                  activeTab === tab.id
                    ? 'border-blue-500 text-blue-600'
                    : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                }`}
              >
                <Icon className="w-4 h-4 mr-2" />
                {tab.label}
              </button>
            );
          })}
        </div>
      </div>
    </nav>
  );
};

export default Navigation;
