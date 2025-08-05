import React from 'react';
import { Shield, AlertTriangle, Calendar } from 'lucide-react';

const ComplianceOverview = ({ overview }) => {
  const getStatusIcon = (status) => {
    switch (status) {
      case 'compliant': 
        return <Shield className="w-5 h-5 text-green-600" />;
      case 'warning': 
        return <AlertTriangle className="w-5 h-5 text-yellow-600" />;
      case 'non-compliant': 
        return <AlertTriangle className="w-5 h-5 text-red-600" />;
      default: 
        return <Shield className="w-5 h-5 text-gray-600" />;
    }
  };

  const getStatusColor = (status) => {
    switch (status) {
      case 'compliant': return 'bg-green-100';
      case 'warning': return 'bg-yellow-100';
      case 'non-compliant': return 'bg-red-100';
      default: return 'bg-gray-100';
    }
  };

  return (
    <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
      <div className="bg-white p-6 rounded-xl shadow-sm border">
        <div className="flex items-center justify-between mb-2">
          <h3 className="text-sm font-medium text-gray-600">Compliance Score</h3>
          <Shield className="w-5 h-5 text-blue-600" />
        </div>
        <div className="text-3xl font-bold text-gray-900">{overview.score}%</div>
      </div>

      <div className="bg-white p-6 rounded-xl shadow-sm border">
        <div className="flex items-center justify-between mb-2">
          <h3 className="text-sm font-medium text-gray-600">Overall Status</h3>
          <div className={`p-1 rounded-full ${getStatusColor(overview.status)}`}>
            {getStatusIcon(overview.status)}
          </div>
        </div>
        <div className="text-lg font-semibold text-gray-900 capitalize">
          {overview.status}
        </div>
      </div>

      <div className="bg-white p-6 rounded-xl shadow-sm border">
        <div className="flex items-center justify-between mb-2">
          <h3 className="text-sm font-medium text-gray-600">Open Issues</h3>
          <AlertTriangle className="w-5 h-5 text-orange-600" />
        </div>
        <div className="text-3xl font-bold text-gray-900">{overview.issues}</div>
      </div>

      <div className="bg-white p-6 rounded-xl shadow-sm border">
        <div className="flex items-center justify-between mb-2">
          <h3 className="text-sm font-medium text-gray-600">Last Audit</h3>
          <Calendar className="w-5 h-5 text-green-600" />
        </div>
        <div className="text-lg font-semibold text-gray-900">
          {new Date(overview.lastAudit).toLocaleDateString()}
        </div>
      </div>
    </div>
  );
};

export default ComplianceOverview;
