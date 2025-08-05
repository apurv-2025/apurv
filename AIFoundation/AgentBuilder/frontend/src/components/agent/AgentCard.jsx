import React from 'react';
import { Bot, TestTube, Edit, Trash2 } from 'lucide-react';

const AgentCard = ({ agent, onBuild,onConfigure,onTest, onDeploy, onMonitor,onDelete }) => {
  return (
    <div className="bg-white rounded-xl shadow-sm border p-6">
      <div className="flex items-center justify-between mb-4">
        <div className="w-12 h-12 bg-blue-100 rounded-full flex items-center justify-center">
          <Bot className="w-6 h-6 text-blue-600" />
        </div>
        <span className={`px-2 py-1 text-xs rounded-full ${
          agent.is_active 
            ? 'bg-green-100 text-green-800' 
            : 'bg-gray-100 text-gray-800'
        }`}>
          {agent.is_active ? 'Active' : 'Inactive'}
        </span>
      </div>

      <h3 className="text-lg font-semibold text-gray-900 mb-2">{agent.name}</h3>
      <p className="text-sm text-gray-600 mb-3">{agent.description}</p>
      <p className="text-xs text-blue-600 font-medium mb-4 uppercase tracking-wide">
        {agent.role}
      </p>

      <div className="flex items-center space-x-2">
        <button
          onClick={() => onBuild(agent)}
          className="flex-1 bg-gray-600 text-white px-3 py-2 rounded-lg hover:bg-gray-700 flex items-center justify-center space-x-1 text-sm transition duration-200"
        >
          <Edit className="w-4 h-4" />
          <span>Edit</span>
        </button>

        <button
          onClick={() => onConfigure(agent)}
          className="flex-1 bg-blue-600 text-white px-3 py-2 rounded-lg hover:bg-gray-700 flex items-center justify-center space-x-1 text-sm transition duration-200"
        >
          <TestTube className="w-4 h-4" />
          <span>Manage Access</span>
        </button>

        <button
          onClick={() => onDelete(agent)}
          className="flex-1 bg-red-600 text-white px-3 py-2 rounded-lg hover:bg-gray-700 flex items-center justify-center space-x-1 text-sm transition duration-200"
        >
          <TestTube className="w-4 h-4" />
          <span>Delete</span>
        </button>
      </div>
      
    </div>
  );
};

export default AgentCard;
