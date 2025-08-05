import React, { useState, useEffect } from 'react';
import { 
  Bot, 
  Shield, 
  MessageSquare, 
  BarChart3
} from 'lucide-react';
import { api } from '../services/api';

const Dashboard = () => {
  const [agents, setAgents] = useState([]);
  const [stats, setStats] = useState({
    totalAgents: 0,
    activeAgents: 0,
    totalInteractions: 0,
    averageConfidence: 0
  });

  useEffect(() => {
    loadAgents();
  }, []);

  const loadAgents = async () => {
    try {
      const agentData = await api.getAgents();
      setAgents(agentData);
      setStats({
        totalAgents: agentData.length,
        activeAgents: agentData.filter(a => a.is_active).length,
        totalInteractions: Math.floor(Math.random() * 1000), // Mock data
        averageConfidence: 0.85 // Mock data
      });
    } catch (error) {
      console.error('Error loading agents:', error);
    }
  };

  return (
    <div className="p-8">
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900 mb-2">Dashboard</h1>
        <p className="text-gray-600">Overview of your AI agents and performance</p>
      </div>

      {/* Stats Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
        <div className="bg-white p-6 rounded-xl shadow-sm border">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-gray-600">Total Agents</p>
              <p className="text-3xl font-bold text-gray-900">{stats.totalAgents}</p>
            </div>
            <Bot className="w-12 h-12 text-blue-600" />
          </div>
        </div>

        <div className="bg-white p-6 rounded-xl shadow-sm border">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-gray-600">Active Agents</p>
              <p className="text-3xl font-bold text-green-600">{stats.activeAgents}</p>
            </div>
            <Shield className="w-12 h-12 text-green-600" />
          </div>
        </div>

        <div className="bg-white p-6 rounded-xl shadow-sm border">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-gray-600">Interactions</p>
              <p className="text-3xl font-bold text-purple-600">{stats.totalInteractions}</p>
            </div>
            <MessageSquare className="w-12 h-12 text-purple-600" />
          </div>
        </div>

        <div className="bg-white p-6 rounded-xl shadow-sm border">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-gray-600">Avg Confidence</p>
              <p className="text-3xl font-bold text-orange-600">
                {(stats.averageConfidence * 100).toFixed(0)}%
              </p>
            </div>
            <BarChart3 className="w-12 h-12 text-orange-600" />
          </div>
        </div>
      </div>

      {/* Recent Agents */}
      <div className="bg-white rounded-xl shadow-sm border">
        <div className="p-6 border-b">
          <h2 className="text-xl font-semibold text-gray-900">Recent Agents</h2>
        </div>
        <div className="p-6">
          {agents.length === 0 ? (
            <div className="text-center py-8">
              <Bot className="w-16 h-16 text-gray-300 mx-auto mb-4" />
              <p className="text-gray-500">No agents created yet</p>
              <p className="text-sm text-gray-400 mt-2">Create your first AI agent to get started</p>
            </div>
          ) : (
            <div className="space-y-4">
              {agents.slice(0, 5).map((agent) => (
                <div key={agent.id} className="flex items-center justify-between p-4 border border-gray-200 rounded-lg">
                  <div className="flex items-center space-x-4">
                    <div className="w-10 h-10 bg-blue-100 rounded-full flex items-center justify-center">
                      <Bot className="w-5 h-5 text-blue-600" />
                    </div>
                    <div>
                      <h3 className="font-medium text-gray-900">{agent.name}</h3>
                      <p className="text-sm text-gray-500">{agent.role} • {agent.description}</p>
                    </div>
                  </div>
                  <div className="flex items-center space-x-2">
                    <span className={`px-2 py-1 text-xs rounded-full ${
                      agent.is_active 
                        ? 'bg-green-100 text-green-800' 
                        : 'bg-gray-100 text-gray-800'
                    }`}>
                      {agent.is_active ? 'Active' : 'Inactive'}
                    </span>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
