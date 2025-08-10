// File: src/components/layout/StatusBar.js
import React, { useState, useEffect } from 'react';
import { FileText } from 'lucide-react';
import { apiService } from '../../services/apiService';

const StatusBar = () => {
  const [requestCount, setRequestCount] = useState(0);
  const [apiStatus, setApiStatus] = useState('connected');

  useEffect(() => {
    const checkApiStatus = async () => {
      try {
        await apiService.healthCheck();
        setApiStatus('connected');
      } catch (error) {
        setApiStatus('disconnected');
      }
    };

    checkApiStatus();
    const interval = setInterval(checkApiStatus, 30000); // Check every 30 seconds

    return () => clearInterval(interval);
  }, []);

  return (
    <div className="fixed bottom-0 left-0 right-0 bg-white border-t border-gray-200 px-4 py-2">
      <div className="max-w-7xl mx-auto flex items-center justify-between text-sm text-gray-600">
        <div className="flex items-center space-x-4">
          <div className="flex items-center">
            <div className={`h-2 w-2 rounded-full mr-2 ${
              apiStatus === 'connected' ? 'bg-green-400' : 'bg-red-400'
            }`}></div>
            API {apiStatus === 'connected' ? 'Connected' : 'Disconnected'}
          </div>
          <div className="flex items-center">
            <FileText className="h-4 w-4 mr-1" />
            EDI 270/271 Compliant
          </div>
        </div>
        <div>
          Processed {requestCount} requests
        </div>
      </div>
    </div>
  );
};

export default StatusBar;
