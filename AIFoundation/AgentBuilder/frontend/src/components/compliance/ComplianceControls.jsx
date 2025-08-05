import React from 'react';
import { CheckCircle, AlertTriangle, Shield } from 'lucide-react';

const ComplianceControls = ({ controls }) => {
  const getStatusColor = (status) => {
    switch (status) {
      case 'compliant': return 'text-green-600 bg-green-100';
      case 'warning': return 'text-yellow-600 bg-yellow-100';
      case 'non-compliant': return 'text-red-600 bg-red-100';
      default: return 'text-gray-600 bg-gray-100';
    }
  };

  const getStatusIcon = (status) => {
    switch (status) {
      case 'compliant': return <CheckCircle className="w-5 h-5" />;
      case 'warning': return <AlertTriangle className="w-5 h-5" />;
      case 'non-compliant': return <AlertTriangle className="w-5 h-5" />;
      default: return <Shield className="w-5 h-5" />;
    }
  };

  return (
    <div className="bg-white rounded-xl shadow-sm border">
      <div className="p-6 border-b">
        <h2 className="text-xl font-semibold text-gray-900">Compliance Controls</h2>
      </div>
      <div className="p-6">
        <div className="space-y-4">
          {controls.map((control, index) => (
            <div key={index} className="flex items-center justify-between p-4 border border-gray-200 rounded-lg">
              <div className="flex items-center space-x-4">
                <div className={`p-2 rounded-full ${getStatusColor(control.status)}`}>
                  {getStatusIcon(control.status)}
                </div>
                <div>
                  <h3 className="font-medium text-gray-900">{control.name}</h3>
                  <p className="text-sm text-gray-500">Last checked: {control.lastCheck}</p>
                </div>
              </div>
              <span className={`px-3 py-1 text-sm rounded-full ${getStatusColor(control.status)}`}>
                {control.status.replace('-', ' ')}
              </span>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default ComplianceControls;
