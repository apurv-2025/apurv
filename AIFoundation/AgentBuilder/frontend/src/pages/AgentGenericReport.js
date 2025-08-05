import React, { useState, useEffect } from 'react';
import { 
  Bot, 
  BarChart3, 
  Download, 
  Calendar, 
  Users, 
  Clock, 
  DollarSign, 
  TrendingUp, 
  TrendingDown, 
  FileText, 
  MessageSquare, 
  CheckCircle, 
  AlertCircle, 
  ArrowRight, 
  Target, 
  Activity, 
  Zap, 
  RefreshCw,
  Filter,
  UserCheck,
  PhoneCall,
  Settings,
  PieChart,
  LineChart,
  Minimize,
  Maximize
} from 'lucide-react';

const GenericAgentReporting = () => {
  const [selectedAgent, setSelectedAgent] = useState(null);
  const [activeTab, setActiveTab] = useState('overview');
  const [timeRange, setTimeRange] = useState('30d');
  const [reportType, setReportType] = useState('comprehensive');

  // Generic agents data - applicable to any agent type
  const agents = [
    {
      id: 1,
      name: "Billing Support Bot",
      type: "billing",
      status: "active",
      // Universal autonomous work metrics
      autonomousWork: {
        totalRequests: 15420,
        fullyAutonomous: 14187,  // Completed without human intervention
        partialAutonomous: 456,  // Started autonomous, needed human input
        humanRequired: 777,      // Required human from start
        autonomyRate: 92.0,      // Percentage of fully autonomous tasks
        humanHandoffRate: 8.0,   // Percentage requiring human intervention
        avgTaskComplexity: 3.2,  // Scale 1-5
        successRate: 94.5        // Successful completion rate
      },
      // Universal interaction metrics
      interactions: {
        totalSessions: 15420,
        avgSessionDuration: 4.2,        // minutes
        userInitiated: 13876,           // User started conversation
        agentInitiated: 1544,           // Agent started (proactive)
        peakHours: "9-11 AM, 2-4 PM",
        uniqueUsers: 3247,
        returningUsers: 8934,
        newUsers: 6486,
        satisfactionScore: 4.3          // Out of 5
      },
      // Universal performance metrics
      performance: {
        responseTime: 0.8,              // seconds
        uptime: 99.2,                   // percentage
        errorRate: 1.2,                 // percentage
        accuracyRate: 94.5,             // percentage
        throughput: 512,                // requests per hour
        concurrentHandling: 45          // simultaneous conversations
      },
      // Universal efficiency metrics
      efficiency: {
        costPerRequest: 0.23,           // dollars
        timeToResolution: 3.4,          // minutes
        escalationRate: 8.0,            // percentage
        reQueryRate: 12.5,              // users asking follow-up questions
        taskCompletionRate: 87.8,       // percentage
        userDropoffRate: 4.2            // percentage who abandon mid-conversation
      }
    },
    {
      id: 2,
      name: "Customer Service Bot",
      type: "support",
      status: "active",
      autonomousWork: {
        totalRequests: 8932,
        fullyAutonomous: 7861,
        partialAutonomous: 312,
        humanRequired: 759,
        autonomyRate: 88.0,
        humanHandoffRate: 12.0,
        avgTaskComplexity: 2.8,
        successRate: 91.2
      },
      interactions: {
        totalSessions: 8932,
        avgSessionDuration: 3.8,
        userInitiated: 7943,
        agentInitiated: 989,
        peakHours: "8-10 AM, 1-3 PM",
        uniqueUsers: 2156,
        returningUsers: 5234,
        newUsers: 3698,
        satisfactionScore: 4.1
      },
      performance: {
        responseTime: 1.2,
        uptime: 98.7,
        errorRate: 2.1,
        accuracyRate: 91.2,
        throughput: 298,
        concurrentHandling: 32
      },
      efficiency: {
        costPerRequest: 0.31,
        timeToResolution: 4.1,
        escalationRate: 12.0,
        reQueryRate: 15.3,
        taskCompletionRate: 84.6,
        userDropoffRate: 6.8
      }
    },
    {
      id: 3,
      name: "General Assistant Bot",
      type: "general",
      status: "active",
      autonomousWork: {
        totalRequests: 6543,
        fullyAutonomous: 5890,
        partialAutonomous: 289,
        humanRequired: 364,
        autonomyRate: 90.0,
        humanHandoffRate: 10.0,
        avgTaskComplexity: 2.5,
        successRate: 89.7
      },
      interactions: {
        totalSessions: 6543,
        avgSessionDuration: 5.7,
        userInitiated: 5234,
        agentInitiated: 1309,
        peakHours: "10 AM-12 PM, 3-5 PM",
        uniqueUsers: 1892,
        returningUsers: 3421,
        newUsers: 3122,
        satisfactionScore: 4.4
      },
      performance: {
        responseTime: 0.6,
        uptime: 99.8,
        errorRate: 0.9,
        accuracyRate: 89.7,
        throughput: 187,
        concurrentHandling: 28
      },
      efficiency: {
        costPerRequest: 0.18,
        timeToResolution: 2.9,
        escalationRate: 10.0,
        reQueryRate: 8.7,
        taskCompletionRate: 92.3,
        userDropoffRate: 3.1
      }
    }
  ];

  // Universal metrics definitions - applicable to all agent types
  const universalMetrics = {
    autonomousWork: [
      {
        name: "Fully Autonomous Tasks",
        description: "Tasks completed entirely without human intervention",
        key: "fullyAutonomous",
        format: "number",
        good: "higher"
      },
      {
        name: "Autonomy Rate",
        description: "Percentage of tasks handled completely autonomously",
        key: "autonomyRate",
        format: "percentage",
        good: "higher"
      },
      {
        name: "Human Handoff Rate",
        description: "Percentage of tasks requiring human intervention",
        key: "humanHandoffRate",
        format: "percentage",
        good: "lower"
      },
      {
        name: "Success Rate",
        description: "Percentage of tasks completed successfully",
        key: "successRate",
        format: "percentage",
        good: "higher"
      },
      {
        name: "Task Complexity",
        description: "Average complexity of handled tasks (1-5 scale)",
        key: "avgTaskComplexity",
        format: "decimal",
        good: "context"
      }
    ],
    interactions: [
      {
        name: "Total Sessions",
        description: "Total number of conversation sessions",
        key: "totalSessions",
        format: "number",
        good: "higher"
      },
      {
        name: "Session Duration",
        description: "Average length of conversation sessions",
        key: "avgSessionDuration",
        format: "minutes",
        good: "context"
      },
      {
        name: "User Initiated",
        description: "Sessions started by users",
        key: "userInitiated",
        format: "number",
        good: "context"
      },
      {
        name: "Agent Initiated",
        description: "Proactive sessions started by agent",
        key: "agentInitiated",
        format: "number",
        good: "context"
      },
      {
        name: "Satisfaction Score",
        description: "Average user satisfaction rating (1-5)",
        key: "satisfactionScore",
        format: "rating",
        good: "higher"
      },
      {
        name: "Unique Users",
        description: "Number of distinct users served",
        key: "uniqueUsers",
        format: "number",
        good: "higher"
      }
    ],
    performance: [
      {
        name: "Response Time",
        description: "Average time to respond to user queries",
        key: "responseTime",
        format: "seconds",
        good: "lower"
      },
      {
        name: "Uptime",
        description: "System availability percentage",
        key: "uptime",
        format: "percentage",
        good: "higher"
      },
      {
        name: "Error Rate",
        description: "Percentage of failed or incorrect responses",
        key: "errorRate",
        format: "percentage",
        good: "lower"
      },
      {
        name: "Accuracy Rate",
        description: "Percentage of correct responses provided",
        key: "accuracyRate",
        format: "percentage",
        good: "higher"
      },
      {
        name: "Throughput",
        description: "Number of requests processed per hour",
        key: "throughput",
        format: "number",
        good: "higher"
      },
      {
        name: "Concurrent Handling",
        description: "Maximum simultaneous conversations",
        key: "concurrentHandling",
        format: "number",
        good: "higher"
      }
    ],
    efficiency: [
      {
        name: "Cost Per Request",
        description: "Average cost to process one request",
        key: "costPerRequest",
        format: "currency",
        good: "lower"
      },
      {
        name: "Time to Resolution",
        description: "Average time to fully resolve user issues",
        key: "timeToResolution",
        format: "minutes",
        good: "lower"
      },
      {
        name: "Escalation Rate",
        description: "Percentage of cases escalated to humans",
        key: "escalationRate",
        format: "percentage",
        good: "lower"
      },
      {
        name: "Re-Query Rate",
        description: "Users asking follow-up questions",
        key: "reQueryRate",
        format: "percentage",
        good: "lower"
      },
      {
        name: "Task Completion Rate",
        description: "Percentage of started tasks completed",
        key: "taskCompletionRate",
        format: "percentage",
        good: "higher"
      },
      {
        name: "User Dropoff Rate",
        description: "Users abandoning conversation mid-way",
        key: "userDropoffRate",
        format: "percentage",
        good: "lower"
      }
    ]
  };

  // Generate trend data for charts
  const generateTrendData = (days = 30, baseValue = 100, variance = 20) => {
    return Array.from({ length: days }, (_, i) => ({
      date: new Date(Date.now() - (days - i) * 24 * 60 * 60 * 1000).toLocaleDateString('en-US', { month: 'short', day: 'numeric' }),
      value: Math.max(0, baseValue + (Math.random() - 0.5) * variance * 2),
      dayOfWeek: new Date(Date.now() - (days - i) * 24 * 60 * 60 * 1000).getDay()
    }));
  };

  const formatValue = (value, format) => {
    switch (format) {
      case 'number':
        return value.toLocaleString();
      case 'percentage':
        return `${value}%`;
      case 'currency':
        return `$${value}`;
      case 'minutes':
        return `${value}m`;
      case 'seconds':
        return `${value}s`;
      case 'rating':
        return `${value}/5`;
      case 'decimal':
        return value.toFixed(1);
      default:
        return value;
    }
  };

  const getMetricValue = (agent, category, key) => {
    return agent[category] ? agent[category][key] : 0;
  };

  const getTrendIcon = (good, currentValue, previousValue = null) => {
    if (!previousValue) return null;
    
    const isImproving = good === 'higher' ? currentValue > previousValue : currentValue < previousValue;
    return isImproving ? 
      <TrendingUp className="w-3 h-3 text-green-600" /> : 
      <TrendingDown className="w-3 h-3 text-red-600" />;
  };

  useEffect(() => {
    if (agents.length > 0 && !selectedAgent) {
      setSelectedAgent(agents[0]);
    }
  }, [agents, selectedAgent]);

  const exportReport = () => {
    const reportData = {
      agent: selectedAgent?.name,
      timeRange,
      autonomousWork: selectedAgent?.autonomousWork,
      interactions: selectedAgent?.interactions,
      performance: selectedAgent?.performance,
      efficiency: selectedAgent?.efficiency,
      generatedAt: new Date().toISOString()
    };
    
    console.log('Exporting Generic Agent Report:', reportData);
    alert('Report exported successfully! Check console for data.');
  };

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <div className="bg-white border-b border-gray-200 px-6 py-4">
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-4">
            <BarChart3 className="w-8 h-8 text-blue-600" />
            <div>
              <h1 className="text-2xl font-bold text-gray-900">Agent Reporting Dashboard</h1>
              <p className="text-gray-600">Universal performance metrics for all agent types</p>
            </div>
          </div>
          <div className="flex items-center space-x-4">
            <select
              value={timeRange}
              onChange={(e) => setTimeRange(e.target.value)}
              className="border border-gray-300 rounded-lg px-3 py-2 focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            >
              <option value="7d">Last 7 Days</option>
              <option value="30d">Last 30 Days</option>
              <option value="90d">Last 90 Days</option>
              <option value="1y">Last Year</option>
            </select>
            <button
              onClick={exportReport}
              className="bg-green-600 text-white px-4 py-2 rounded-lg flex items-center space-x-2 hover:bg-green-700 transition-colors"
            >
              <Download className="w-4 h-4" />
              <span>Export Report</span>
            </button>
            <button className="bg-blue-600 text-white px-4 py-2 rounded-lg flex items-center space-x-2 hover:bg-blue-700 transition-colors">
              <RefreshCw className="w-4 h-4" />
              <span>Refresh</span>
            </button>
          </div>
        </div>
      </div>

      <div className="flex">
        {/* Sidebar - Agent Selection */}
        <div className="w-80 bg-white border-r border-gray-200 h-screen overflow-y-auto">
          <div className="p-6">
            <h2 className="text-lg font-semibold text-gray-900 mb-4">Select Agent</h2>
            
            <div className="space-y-4">
              {agents.map((agent) => (
                <div
                  key={agent.id}
                  onClick={() => setSelectedAgent(agent)}
                  className={`p-4 border rounded-lg cursor-pointer transition-all ${
                    selectedAgent?.id === agent.id 
                      ? 'border-blue-300 bg-blue-50' 
                      : 'border-gray-200 hover:border-blue-200 hover:bg-gray-50'
                  }`}
                >
                  <div className="flex items-start justify-between mb-3">
                    <h3 className="font-medium text-gray-900">{agent.name}</h3>
                    <span className="px-2 py-1 rounded-full text-xs font-medium bg-green-100 text-green-800">
                      {agent.status}
                    </span>
                  </div>
                  
                  <div className="space-y-2 text-sm">
                    <div className="flex justify-between text-gray-600">
                      <span>Autonomy Rate:</span>
                      <span className="font-medium">{agent.autonomousWork.autonomyRate}%</span>
                    </div>
                    <div className="flex justify-between text-gray-600">
                      <span>Total Requests:</span>
                      <span className="font-medium">{agent.autonomousWork.totalRequests.toLocaleString()}</span>
                    </div>
                    <div className="flex justify-between text-gray-600">
                      <span>Success Rate:</span>
                      <span className="font-medium">{agent.autonomousWork.successRate}%</span>
                    </div>
                    <div className="flex justify-between text-gray-600">
                      <span>Avg Response:</span>
                      <span className="font-medium">{agent.performance.responseTime}s</span>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>

        {/* Main Content */}
        <div className="flex-1 p-6">
          {!selectedAgent ? (
            <div className="flex items-center justify-center h-64">
              <div className="text-center">
                <BarChart3 className="w-16 h-16 text-gray-400 mx-auto mb-4" />
                <h3 className="text-lg font-medium text-gray-900 mb-2">Select an Agent for Reporting</h3>
                <p className="text-gray-600">Choose an agent from the sidebar to view detailed performance reports</p>
              </div>
            </div>
          ) : (
            <div>
              {/* Agent Header */}
              <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6 mb-6">
                <div className="flex items-center justify-between mb-4">
                  <div>
                    <h2 className="text-xl font-bold text-gray-900">{selectedAgent.name}</h2>
                    <p className="text-gray-600">Universal performance metrics for {timeRange}</p>
                  </div>
                  <div className="flex items-center space-x-6">
                    <div className="text-center">
                      <div className="text-2xl font-bold text-blue-600">{selectedAgent.autonomousWork.autonomyRate}%</div>
                      <div className="text-sm text-gray-600">Autonomy Rate</div>
                    </div>
                    <div className="text-center">
                      <div className="text-2xl font-bold text-green-600">{selectedAgent.autonomousWork.fullyAutonomous.toLocaleString()}</div>
                      <div className="text-sm text-gray-600">Autonomous Tasks</div>
                    </div>
                    <div className="text-center">
                      <div className="text-2xl font-bold text-purple-600">{selectedAgent.interactions.totalSessions.toLocaleString()}</div>
                      <div className="text-sm text-gray-600">Total Sessions</div>
                    </div>
                    <div className="text-center">
                      <div className="text-2xl font-bold text-orange-600">{selectedAgent.performance.responseTime}s</div>
                      <div className="text-sm text-gray-600">Avg Response</div>
                    </div>
                  </div>
                </div>

                {/* Tabs */}
                <div className="border-b border-gray-200">
                  <nav className="-mb-px flex space-x-8">
                    {['overview', 'autonomous-work', 'interactions', 'performance', 'efficiency'].map((tab) => (
                      <button
                        key={tab}
                        onClick={() => setActiveTab(tab)}
                        className={`py-2 px-1 border-b-2 font-medium text-sm transition-colors ${
                          activeTab === tab
                            ? 'border-blue-500 text-blue-600'
                            : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                        }`}
                      >
                        {tab.replace('-', ' ').replace(/\b\w/g, l => l.toUpperCase())}
                      </button>
                    ))}
                  </nav>
                </div>
              </div>

              {/* Tab Content */}
              {activeTab === 'overview' && (
                <div className="space-y-6">
                  {/* Key Metrics Grid */}
                  <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
                    <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
                      <div className="flex items-center justify-between">
                        <div>
                          <p className="text-sm text-gray-600">Fully Autonomous</p>
                          <p className="text-2xl font-bold text-blue-600">{selectedAgent.autonomousWork.fullyAutonomous.toLocaleString()}</p>
                          <p className="text-xs text-green-600 mt-1">
                            <TrendingUp className="w-3 h-3 inline mr-1" />
                            92% of total requests
                          </p>
                        </div>
                        <Bot className="w-8 h-8 text-blue-600" />
                      </div>
                    </div>
                    
                    <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
                      <div className="flex items-center justify-between">
                        <div>
                          <p className="text-sm text-gray-600">Human Handoffs</p>
                          <p className="text-2xl font-bold text-orange-600">{selectedAgent.autonomousWork.humanRequired}</p>
                          <p className="text-xs text-green-600 mt-1">
                            <TrendingDown className="w-3 h-3 inline mr-1" />
                            {selectedAgent.autonomousWork.humanHandoffRate}% of requests
                          </p>
                        </div>
                        <Users className="w-8 h-8 text-orange-600" />
                      </div>
                    </div>
                    
                    <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
                      <div className="flex items-center justify-between">
                        <div>
                          <p className="text-sm text-gray-600">User Sessions</p>
                          <p className="text-2xl font-bold text-purple-600">{selectedAgent.interactions.totalSessions.toLocaleString()}</p>
                          <p className="text-xs text-blue-600 mt-1">
                            <MessageSquare className="w-3 h-3 inline mr-1" />
                            {selectedAgent.interactions.avgSessionDuration}m avg duration
                          </p>
                        </div>
                        <MessageSquare className="w-8 h-8 text-purple-600" />
                      </div>
                    </div>
                    
                    <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
                      <div className="flex items-center justify-between">
                        <div>
                          <p className="text-sm text-gray-600">Success Rate</p>
                          <p className="text-2xl font-bold text-green-600">{selectedAgent.autonomousWork.successRate}%</p>
                          <p className="text-xs text-green-600 mt-1">
                            <CheckCircle className="w-3 h-3 inline mr-1" />
                            Tasks completed successfully
                          </p>
                        </div>
                        <Target className="w-8 h-8 text-green-600" />
                      </div>
                    </div>
                  </div>

                  {/* Interaction Breakdown */}
                  <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                    <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
                      <h3 className="text-lg font-semibold text-gray-900 mb-4">Autonomous vs Human Work</h3>
                      <div className="space-y-4">
                        <div className="flex items-center justify-between">
                          <span className="text-sm text-gray-600">Fully Autonomous</span>
                          <div className="flex items-center space-x-2">
                            <span className="text-sm font-medium">{selectedAgent.autonomousWork.fullyAutonomous.toLocaleString()}</span>
                            <div className="w-24 bg-gray-200 rounded-full h-2">
                              <div 
                                className="bg-blue-600 h-2 rounded-full" 
                                style={{ width: `${selectedAgent.autonomousWork.autonomyRate}%` }}
                              ></div>
                            </div>
                          </div>
                        </div>
                        <div className="flex items-center justify-between">
                          <span className="text-sm text-gray-600">Partial Human Input</span>
                          <div className="flex items-center space-x-2">
                            <span className="text-sm font-medium">{selectedAgent.autonomousWork.partialAutonomous}</span>
                            <div className="w-24 bg-gray-200 rounded-full h-2">
                              <div 
                                className="bg-yellow-500 h-2 rounded-full" 
                                style={{ width: `${(selectedAgent.autonomousWork.partialAutonomous / selectedAgent.autonomousWork.totalRequests) * 100}%` }}
                              ></div>
                            </div>
                          </div>
                        </div>
                        <div className="flex items-center justify-between">
                          <span className="text-sm text-gray-600">Human Required</span>
                          <div className="flex items-center space-x-2">
                            <span className="text-sm font-medium">{selectedAgent.autonomousWork.humanRequired}</span>
                            <div className="w-24 bg-gray-200 rounded-full h-2">
                              <div 
                                className="bg-red-500 h-2 rounded-full" 
                                style={{ width: `${selectedAgent.autonomousWork.humanHandoffRate}%` }}
                              ></div>
                            </div>
                          </div>
                        </div>
                      </div>
                    </div>

                    <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
                      <h3 className="text-lg font-semibold text-gray-900 mb-4">User Interaction Patterns</h3>
                      <div className="space-y-4">
                        <div className="flex items-center justify-between">
                          <span className="text-sm text-gray-600">User Initiated</span>
                          <div className="flex items-center space-x-2">
                            <span className="text-sm font-medium">{selectedAgent.interactions.userInitiated.toLocaleString()}</span>
                            <span className="text-xs text-blue-600">
                              {Math.round((selectedAgent.interactions.userInitiated / selectedAgent.interactions.totalSessions) * 100)}%
                            </span>
                          </div>
                        </div>
                        <div className="flex items-center justify-between">
                          <span className="text-sm text-gray-600">Agent Initiated</span>
                          <div className="flex items-center space-x-2">
                            <span className="text-sm font-medium">{selectedAgent.interactions.agentInitiated.toLocaleString()}</span>
                            <span className="text-xs text-purple-600">
                              {Math.round((selectedAgent.interactions.agentInitiated / selectedAgent.interactions.totalSessions) * 100)}%
                            </span>
                          </div>
                        </div>
                        <div className="flex items-center justify-between">
                          <span className="text-sm text-gray-600">Unique Users</span>
                          <span className="text-sm font-medium">{selectedAgent.interactions.uniqueUsers.toLocaleString()}</span>
                        </div>
                        <div className="flex items-center justify-between">
                          <span className="text-sm text-gray-600">Satisfaction Score</span>
                          <div className="flex items-center space-x-2">
                            <span className="text-sm font-medium">{selectedAgent.interactions.satisfactionScore}/5</span>
                            <div className="flex space-x-1">
                              {[1,2,3,4,5].map(star => (
                                <div
                                  key={star}
                                  className={`w-3 h-3 rounded-full ${
                                    star <= selectedAgent.interactions.satisfactionScore ? 'bg-yellow-400' : 'bg-gray-200'
                                  }`}
                                ></div>
                              ))}
                            </div>
                          </div>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              )}

              {activeTab === 'autonomous-work' && (
                <div className="space-y-6">
                  <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                    {universalMetrics.autonomousWork.map((metric) => {
                      const value = getMetricValue(selectedAgent, 'autonomousWork', metric.key);
                      return (
                        <div key={metric.key} className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
                          <div className="flex items-center justify-between mb-3">
                            <h3 className="font-medium text-gray-900">{metric.name}</h3>
                            <div className={`p-2 rounded-lg ${
                              metric.good === 'higher' ? 'bg-blue-100' :
                              metric.good === 'lower' ? 'bg-green-100' : 'bg-gray-100'
                            }`}>
                              {metric.good === 'higher' ? <TrendingUp className="w-4 h-4 text-blue-600" /> :
                               metric.good === 'lower' ? <TrendingDown className="w-4 h-4 text-green-600" /> :
                               <Activity className="w-4 h-4 text-gray-600" />}
                            </div>
                          </div>
                          <div className="text-2xl font-bold text-gray-900 mb-2">
                            {formatValue(value, metric.format)}
                          </div>
                          <p className="text-sm text-gray-600">{metric.description}</p>
                        </div>
                      );
                    })}
                  </div>
                </div>
              )}

              {activeTab === 'interactions' && (
                <div className="space-y-6">
                  <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                    {universalMetrics.interactions.map((metric) => {
                      const value = getMetricValue(selectedAgent, 'interactions', metric.key);
                      return (
                        <div key={metric.key} className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
                          <div className="flex items-center justify-between mb-3">
                            <h3 className="font-medium text-gray-900">{metric.name}</h3>
                            <div className={`p-2 rounded-lg ${
                              metric.good === 'higher' ? 'bg-blue-100' :
                              metric.good === 'lower' ? 'bg-green-100' : 'bg-gray-100'
                            }`}>
                              {metric.good === 'higher' ? <TrendingUp className="w-4 h-4 text-blue-600" /> :
                               metric.good === 'lower' ? <TrendingDown className="w-4 h-4 text-green-600" /> :
                               <MessageSquare className="w-4 h-4 text-gray-600" />}
                            </div>
                          </div>
                          <div className="text-2xl font-bold text-gray-900 mb-2">
                            {formatValue(value, metric.format)}
                          </div>
                          <p className="text-sm text-gray-600">{metric.description}</p>
                        </div>
                      );
                    })}
                  </div>

                  {/* Interaction Timeline */}
                  <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
                    <h3 className="text-lg font-semibold text-gray-900 mb-4">Interaction Timeline</h3>
                    <div className="space-y-4">
                      <div className="flex items-center justify-between p-4 bg-blue-50 rounded-lg">
                        <div>
                          <h4 className="font-medium text-blue-900">Peak Hours</h4>
                          <p className="text-sm text-blue-700">{selectedAgent.interactions.peakHours}</p>
                        </div>
                        <Clock className="w-6 h-6 text-blue-600" />
                      </div>
                      <div className="grid grid-cols-3 gap-4">
                        <div className="text-center p-4 bg-gray-50 rounded-lg">
                          <div className="text-xl font-bold text-gray-900">{selectedAgent.interactions.newUsers.toLocaleString()}</div>
                          <div className="text-sm text-gray-600">New Users</div>
                        </div>
                        <div className="text-center p-4 bg-gray-50 rounded-lg">
                          <div className="text-xl font-bold text-gray-900">{selectedAgent.interactions.returningUsers.toLocaleString()}</div>
                          <div className="text-sm text-gray-600">Returning Users</div>
                        </div>
                        <div className="text-center p-4 bg-gray-50 rounded-lg">
                          <div className="text-xl font-bold text-gray-900">
                            {Math.round((selectedAgent.interactions.returningUsers / selectedAgent.interactions.uniqueUsers) * 100)}%
                          </div>
                          <div className="text-sm text-gray-600">Return Rate</div>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              )}

              {activeTab === 'performance' && (
                <div className="space-y-6">
                  <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                    {universalMetrics.performance.map((metric) => {
                      const value = getMetricValue(selectedAgent, 'performance', metric.key);
                      return (
                        <div key={metric.key} className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
                          <div className="flex items-center justify-between mb-3">
                            <h3 className="font-medium text-gray-900">{metric.name}</h3>
                            <div className={`p-2 rounded-lg ${
                              metric.good === 'higher' ? 'bg-blue-100' :
                              metric.good === 'lower' ? 'bg-green-100' : 'bg-gray-100'
                            }`}>
                              {metric.good === 'higher' ? <TrendingUp className="w-4 h-4 text-blue-600" /> :
                               metric.good === 'lower' ? <TrendingDown className="w-4 h-4 text-green-600" /> :
                               <Activity className="w-4 h-4 text-gray-600" />}
                            </div>
                          </div>
                          <div className="text-2xl font-bold text-gray-900 mb-2">
                            {formatValue(value, metric.format)}
                          </div>
                          <p className="text-sm text-gray-600">{metric.description}</p>
                          
                          {/* Performance indicator bar */}
                          <div className="mt-3">
                            <div className="w-full bg-gray-200 rounded-full h-2">
                              <div 
                                className={`h-2 rounded-full ${
                                  (metric.key === 'uptime' && value >= 99) ||
                                  (metric.key === 'accuracyRate' && value >= 90) ||
                                  (metric.key === 'responseTime' && value <= 2) ||
                                  (metric.key === 'errorRate' && value <= 2) ||
                                  (metric.key === 'throughput' && value >= 200) ||
                                  (metric.key === 'concurrentHandling' && value >= 20)
                                    ? 'bg-green-500' : 'bg-yellow-500'
                                }`}
                                style={{ 
                                  width: metric.key === 'uptime' || metric.key === 'accuracyRate' ? `${value}%` :
                                         metric.key === 'responseTime' ? `${Math.min(100, (5 - value) * 20)}%` :
                                         metric.key === 'errorRate' ? `${Math.max(0, 100 - (value * 20))}%` :
                                         metric.key === 'throughput' ? `${Math.min(100, (value / 500) * 100)}%` :
                                         `${Math.min(100, (value / 50) * 100)}%`
                                }}
                              ></div>
                            </div>
                          </div>
                        </div>
                      );
                    })}
                  </div>
                </div>
              )}

              {activeTab === 'efficiency' && (
                <div className="space-y-6">
                  <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                    {universalMetrics.efficiency.map((metric) => {
                      const value = getMetricValue(selectedAgent, 'efficiency', metric.key);
                      return (
                        <div key={metric.key} className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
                          <div className="flex items-center justify-between mb-3">
                            <h3 className="font-medium text-gray-900">{metric.name}</h3>
                            <div className={`p-2 rounded-lg ${
                              metric.good === 'higher' ? 'bg-blue-100' :
                              metric.good === 'lower' ? 'bg-green-100' : 'bg-gray-100'
                            }`}>
                              {metric.good === 'higher' ? <TrendingUp className="w-4 h-4 text-blue-600" /> :
                               metric.good === 'lower' ? <TrendingDown className="w-4 h-4 text-green-600" /> :
                               <Zap className="w-4 h-4 text-gray-600" />}
                            </div>
                          </div>
                          <div className="text-2xl font-bold text-gray-900 mb-2">
                            {formatValue(value, metric.format)}
                          </div>
                          <p className="text-sm text-gray-600">{metric.description}</p>
                        </div>
                      );
                    })}
                  </div>

                  {/* Efficiency Summary */}
                  <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
                    <h3 className="text-lg font-semibold text-gray-900 mb-4">Efficiency Summary</h3>
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                      <div>
                        <h4 className="font-medium text-gray-900 mb-3">Cost Efficiency</h4>
                        <div className="space-y-2">
                          <div className="flex justify-between">
                            <span className="text-sm text-gray-600">Cost per Request:</span>
                            <span className="font-medium">${selectedAgent.efficiency.costPerRequest}</span>
                          </div>
                          <div className="flex justify-between">
                            <span className="text-sm text-gray-600">Monthly Volume:</span>
                            <span className="font-medium">{Math.round(selectedAgent.autonomousWork.totalRequests * 1.2).toLocaleString()}</span>
                          </div>
                          <div className="flex justify-between">
                            <span className="text-sm text-gray-600">Monthly Cost:</span>
                            <span className="font-medium text-green-600">
                              ${Math.round(selectedAgent.autonomousWork.totalRequests * 1.2 * selectedAgent.efficiency.costPerRequest).toLocaleString()}
                            </span>
                          </div>
                        </div>
                      </div>
                      <div>
                        <h4 className="font-medium text-gray-900 mb-3">Time Efficiency</h4>
                        <div className="space-y-2">
                          <div className="flex justify-between">
                            <span className="text-sm text-gray-600">Avg Resolution Time:</span>
                            <span className="font-medium">{selectedAgent.efficiency.timeToResolution}m</span>
                          </div>
                          <div className="flex justify-between">
                            <span className="text-sm text-gray-600">Task Completion:</span>
                            <span className="font-medium">{selectedAgent.efficiency.taskCompletionRate}%</span>
                          </div>
                          <div className="flex justify-between">
                            <span className="text-sm text-gray-600">User Dropoff:</span>
                            <span className="font-medium text-orange-600">{selectedAgent.efficiency.userDropoffRate}%</span>
                          </div>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              )}
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default GenericAgentReporting;