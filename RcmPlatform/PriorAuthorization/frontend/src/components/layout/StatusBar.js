// File: src/components/layout/StatusBar.js - Status Bar Component
import React from 'react';
import { FileText } from 'lucide-react';
import { useAuthorization } from '../../contexts/AuthorizationContext';

const StatusBar = () => {
  const { requests, patients } = useAuthorization();

  return (
    <div className="fixed bottom-0 left-0 right-0 bg-white border-t border-gray-200 px-4 py-2">
      <div className="max-w-7xl mx-auto flex items-center justify-between text-sm text-gray-600">
        <div className="flex items-center space-x-4">
          <div className="flex items-center">
            <div className="h-2 w-2 bg-green-400 rounded-full mr-2"></div>
            System Online
          </div>
          <div className="flex items-center">
            <FileText className="h-4 w-4 mr-1" />
            EDI 278/275 Ready
          </div>
        </div>
        <div className="flex items-center space-x-4">
          <span>Requests: {requests.length}</span>
          <span>Patients: {patients.length}</span>
        </div>
      </div>
    </div>
  );
};

export default StatusBar;
