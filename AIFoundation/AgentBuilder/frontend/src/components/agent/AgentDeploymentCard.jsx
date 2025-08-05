import React from 'react';
import { Bot, Cloud, CheckCircle, AlertCircle, Clock } from 'lucide-react';

const AgentDeploymentCard = ({ agent, isSelected, onClick }) => {
  const getStatusColor = (status) => {
    const statuses = {
      'not_deployed': { color: 'text-gray-600 bg-gray-100', label: 'Not Deployed' },
      'deploying': { color: 'text-blue-600 bg-blue-100', label: 'Deploying' },
      'staging': { color: 'text-yellow-600 bg-yellow-100', label: 'Staging' },
      'deployed': { color: 'text-green-600 bg-green-100', label: 'Production' },
      'failed': { color: 'text-red-600 bg-red-100', label: 'Failed' }
    };
    return statuses[status] || statuses['not_deployed'];
  };

  const statusInfo = getStatusColor(agent.deploymentStatus);

  return (
    <div
      onClick={() => onClick(agent)}
      className={`p-4 border rounded-lg cursor-pointer transition-all ${
        isSelected 
          ? 'border-blue-300 bg-blue-50' 
          : 'border-gray-200 hover:border-blue-200 hover:bg-gray-50'
      }`}
    >
      <div className="flex items-start justify-between mb-3">
        <h3 className="font-medium text-gray-900">{agent.name}</h3>
        <span className={`px-2 py-1 rounded-full text-xs font-medium ${statusInfo.color}`}>
          {statusInfo.label}
        </span>
      </div>
      
      <div className="space-y-2 text-sm">
        <div className="flex justify-between text-gray-600">
          <span>Version:</span>
          <span className="font-medium">{agent.version}</span>
        </div>
        <div className="flex justify-between text-gray-600">
          <span>Accuracy:</span>
          <span className="font-medium">{agent.accuracy}%</span>
        </div>
        {agent.cloudVendor && (
          <div className="flex justify-between text-gray-600">
            <span>Cloud:</span>
            <span className="font-medium capitalize">{agent.cloudVendor}</span>
          </div>
        )}
        <div className="flex justify-between text-gray-600">
          <span>Last Tested:</span>
          <span className="font-medium">{agent.lastTested}</span>
        </div>
      </div>
    </div>
  );
};

export default AgentDeploymentCard; 