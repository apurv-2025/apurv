import React from 'react';
import { Bot, Brain, CheckCircle, AlertCircle, Clock } from 'lucide-react';

const AgentTrainingCard = ({ agent, isSelected, onClick }) => {
  const getStatusColor = (status) => {
    switch (status) {
      case 'trained': return 'text-green-600 bg-green-100';
      case 'training': return 'text-blue-600 bg-blue-100';
      case 'needs_training': return 'text-orange-600 bg-orange-100';
      default: return 'text-gray-600 bg-gray-100';
    }
  };

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
        <span className={`px-2 py-1 rounded-full text-xs font-medium ${getStatusColor(agent.trainingStatus)}`}>
          {agent.trainingStatus.replace('_', ' ')}
        </span>
      </div>
      
      <div className="space-y-2 text-sm">
        <div className="flex justify-between text-gray-600">
          <span>Accuracy:</span>
          <span className="font-medium">{agent.accuracy}%</span>
        </div>
        <div className="flex justify-between text-gray-600">
          <span>Training Data:</span>
          <span className="font-medium">{agent.trainingData.toLocaleString()}</span>
        </div>
        <div className="flex justify-between text-gray-600">
          <span>Last Trained:</span>
          <span className="font-medium">{agent.lastTrained}</span>
        </div>
      </div>
    </div>
  );
};

export default AgentTrainingCard; 