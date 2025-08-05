import React, { useState, useEffect } from 'react';
import { 
  Bot, 
  Activity, 
  Shield, 
  AlertTriangle, 
  CheckCircle, 
  X, 
  Clock, 
  Users, 
  Database, 
  Lock, 
  FileText, 
  Eye, 
  Download, 
  RefreshCw, 
  Settings, 
  BarChart3, 
  TrendingUp, 
  TrendingDown, 
  Zap, 
  Heart, 
  AlertCircle, 
  Key, 
  UserCheck, 
  Calendar, 
  Globe, 
  Server, 
  Monitor,
  Clipboard,
  Scale
} from 'lucide-react';

const AgentMonitoringCompliance = () => {
  const [selectedAgent, setSelectedAgent] = useState(null);
  const [activeTab, setActiveTab] = useState('overview');
  const [timeRange, setTimeRange] = useState('24h');
  const [alertsCount, setAlertsCount] = useState(0);
  const [reportDateRange, setReportDateRange] = useState('30d');
  const [reportType, setReportType] = useState('efficiency');

  // Mock agents data with health and compliance metrics
  const agents = [
    {
      id: 1,
      name: "Billing Support Bot",
      status: "healthy",
      complianceScore: 98,
      healthScore: 95,
      uptime: 99.8,
      lastChecked: "2025-01-28 10:30 AM",
      violations: 0,
      hipaaCompliant: true,
      gdprCompliant: true,
      responseTime: 245,
      errorRate: 0.2,
      totalInteractions: 15420
    },
    {
      id: 2,
      name: "Front Desk Assistant",
      status: "warning",
      complianceScore: 85,
      healthScore: 88,
      uptime: 97.5,
      lastChecked: "2025-01-28 10:25 AM",
      violations: 2,
      hipaaCompliant: true,
      gdprCompliant: false,
      responseTime: 520,
      errorRate: 1.8,
      totalInteractions: 8932
    },
    {
      id: 3,
      name: "Patient Portal Assistant",
      status: "critical",
      complianceScore: 72,
      healthScore: 65,
      uptime: 94.2,
      lastChecked: "2025-01-28 10:20 AM",
      violations: 5,
      hipaaCompliant: false,
      gdprCompliant: true,
      responseTime: 890,
      errorRate: 4.5,
      totalInteractions: 3421
    }
  ];

  // Health metrics for healthcare domain
  const healthMetrics = [
    {
      name: 'Response Time',
      value: selectedAgent?.responseTime || 0,
      unit: 'ms',
      threshold: 500,
      status: (selectedAgent?.responseTime || 0) < 500 ? 'good' : 'warning',
      icon: Clock,
      description: 'Average response time for patient queries'
    },
    {
      name: 'Uptime',
      value: selectedAgent?.uptime || 0,
      unit: '%',
      threshold: 99.5,
      status: (selectedAgent?.uptime || 0) >= 99.5 ? 'good' : 'warning',
      icon: Activity,
      description: 'System availability for patient interactions'
    },
    {
      name: 'Error Rate',
      value: selectedAgent?.errorRate || 0,
      unit: '%',
      threshold: 1.0,
      status: (selectedAgent?.errorRate || 0) <= 1.0 ? 'good' : 'critical',
      icon: AlertTriangle,
      description: 'Percentage of failed or incorrect responses'
    },
    {
      name: 'Patient Satisfaction',
      value: 94.2,
      unit: '%',
      threshold: 90,
      status: 94.2 >= 90 ? 'good' : 'warning',
      icon: Heart,
      description: 'Patient satisfaction score from feedback'
    },
    {
      name: 'Data Accuracy',
      value: 98.7,
      unit: '%',
      threshold: 95,
      status: 98.7 >= 95 ? 'good' : 'warning',
      icon: Database,
      description: 'Accuracy of medical information provided'
    },
    {
      name: 'Security Score',
      value: 96.5,
      unit: '%',
      threshold: 95,
      status: 96.5 >= 95 ? 'good' : 'critical',
      icon: Shield,
      description: 'Overall security posture and vulnerability status'
    }
  ];

  // Compliance frameworks for healthcare
  const complianceFrameworks = [
    {
      name: 'HIPAA',
      fullName: 'Health Insurance Portability and Accountability Act',
      status: selectedAgent?.hipaaCompliant ? 'compliant' : 'violation',
      score: selectedAgent?.hipaaCompliant ? 98 : 72,
      lastAudit: '2025-01-25',
      requirements: [
        { name: 'PHI Encryption', status: 'compliant', critical: true },
        { name: 'Access Controls', status: 'compliant', critical: true },
        { name: 'Audit Logging', status: selectedAgent?.hipaaCompliant ? 'compliant' : 'violation', critical: true },
        { name: 'Data Backup', status: 'compliant', critical: false },
        { name: 'Incident Response', status: 'compliant', critical: true }
      ],
      icon: Shield
    },
    {
      name: 'GDPR',
      fullName: 'General Data Protection Regulation',
      status: selectedAgent?.gdprCompliant ? 'compliant' : 'violation',
      score: selectedAgent?.gdprCompliant ? 95 : 68,
      lastAudit: '2025-01-22',
      requirements: [
        { name: 'Consent Management', status: selectedAgent?.gdprCompliant ? 'compliant' : 'violation', critical: true },
        { name: 'Data Minimization', status: 'compliant', critical: true },
        { name: 'Right to Erasure', status: 'compliant', critical: false },
        { name: 'Privacy by Design', status: selectedAgent?.gdprCompliant ? 'compliant' : 'violation', critical: true },
        { name: 'Breach Notification', status: 'compliant', critical: true }
      ],
      icon: Globe
    },
    {
      name: 'SOC 2',
      fullName: 'Service Organization Control 2',
      status: 'compliant',
      score: 92,
      lastAudit: '2025-01-20',
      requirements: [
        { name: 'Security Controls', status: 'compliant', critical: true },
        { name: 'Availability', status: 'compliant', critical: true },
        { name: 'Processing Integrity', status: 'compliant', critical: false },
        { name: 'Confidentiality', status: 'compliant', critical: true },
        { name: 'Privacy', status: 'compliant', critical: false }
      ],
      icon: Lock
    },
    {
      name: 'FDA 21 CFR Part 11',
      fullName: 'Electronic Records and Signatures',
      status: 'compliant',
      score: 89,
      lastAudit: '2025-01-18',
      requirements: [
        { name: 'Electronic Signatures', status: 'compliant', critical: true },
        { name: 'Audit Trails', status: 'compliant', critical: true },
        { name: 'Record Integrity', status: 'compliant', critical: true },
        { name: 'Access Controls', status: 'compliant', critical: false },
        { name: 'System Validation', status: 'compliant', critical: true }
      ],
      icon: FileText
    }
  ];

  // Recent compliance alerts and violations
  const recentAlerts = [
    {
      id: 1,
      type: 'violation',
      severity: 'high',
      framework: 'HIPAA',
      message: 'Unauthorized access attempt detected in patient data queries',
      timestamp: '2025-01-28 09:45 AM',
      agent: 'Patient Portal Assistant',
      resolved: false
    },
    {
      id: 2,
      type: 'warning',
      severity: 'medium',
      framework: 'GDPR',
      message: 'Consent verification failed for 3 patient interactions',
      timestamp: '2025-01-28 08:30 AM',
      agent: 'Front Desk Assistant',
      resolved: false
    },
    {
      id: 3,
      type: 'info',
      severity: 'low',
      framework: 'SOC 2',
      message: 'Routine security scan completed successfully',
      timestamp: '2025-01-28 07:15 AM',
      agent: 'All Agents',
      resolved: true
    }
  ];

  useEffect(() => {
    setAlertsCount(recentAlerts.filter(alert => !alert.resolved).length);
  }, []);

  const getStatusColor = (status) => {
    switch (status) {
      case 'healthy':
      case 'good':
      case 'compliant':
        return 'text-green-600 bg-green-100';
      case 'warning':
        return 'text-yellow-600 bg-yellow-100';
      case 'critical':
      case 'violation':
        return 'text-red-600 bg-red-100';
      default:
        return 'text-gray-600 bg-gray-100';
    }
  };

  const getSeverityColor = (severity) => {
    switch (severity) {
      case 'high':
        return 'text-red-600 bg-red-100';
      case 'medium':
        return 'text-yellow-600 bg-yellow-100';
      case 'low':
        return 'text-blue-600 bg-blue-100';
      default:
        return 'text-gray-600 bg-gray-100';
    }
  };

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <div className="bg-white border-b border-gray-200 px-6 py-4">
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-4">
            <Shield className="w-8 h-8 text-blue-600" />
            <div>
              <h1 className="text-2xl font-bold text-gray-900">Agent Monitoring & Compliance</h1>
              <p className="text-gray-600">Healthcare compliance and performance monitoring</p>
            </div>
          </div>
          <div className="flex items-center space-x-4">
            {alertsCount > 0 && (
              <div className="flex items-center space-x-2 bg-red-50 px-3 py-2 rounded-lg">
                <AlertTriangle className="w-4 h-4 text-red-600" />
                <span className="text-red-600 font-medium">{alertsCount} Active Alerts</span>
              </div>
            )}
            <select
              value={timeRange}
              onChange={(e) => setTimeRange(e.target.value)}
              className="border border-gray-300 rounded-lg px-3 py-2 focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            >
              <option value="1h">Last Hour</option>
              <option value="24h">Last 24 Hours</option>
              <option value="7d">Last 7 Days</option>
              <option value="30d">Last 30 Days</option>
            </select>
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
            <h2 className="text-lg font-semibold text-gray-900 mb-4">Agents</h2>
            
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
                    <span className={`px-2 py-1 rounded-full text-xs font-medium ${getStatusColor(agent.status)}`}>
                      {agent.status}
                    </span>
                  </div>
                  
                  <div className="space-y-2 text-sm">
                    <div className="flex justify-between text-gray-600">
                      <span>Health Score:</span>
                      <span className="font-medium">{agent.healthScore}%</span>
                    </div>
                    <div className="flex justify-between text-gray-600">
                      <span>Compliance:</span>
                      <span className="font-medium">{agent.complianceScore}%</span>
                    </div>
                    <div className="flex justify-between text-gray-600">
                      <span>Violations:</span>
                      <span className={`font-medium ${agent.violations > 0 ? 'text-red-600' : 'text-green-600'}`}>
                        {agent.violations}
                      </span>
                    </div>
                    <div className="text-xs text-gray-500">
                      Last checked: {agent.lastChecked}
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
                <Monitor className="w-16 h-16 text-gray-400 mx-auto mb-4" />
                <h3 className="text-lg font-medium text-gray-900 mb-2">Select an Agent to Monitor</h3>
                <p className="text-gray-600">Choose an agent from the sidebar to view health and compliance metrics</p>
              </div>
            </div>
          ) : (
            <div>
              {/* Agent Header */}
              <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6 mb-6">
                <div className="flex items-center justify-between mb-4">
                  <div>
                    <h2 className="text-xl font-bold text-gray-900">{selectedAgent.name}</h2>
                    <p className="text-gray-600">Health and compliance monitoring dashboard</p>
                  </div>
                  <div className="flex items-center space-x-6">
                    <div className="text-center">
                      <div className="text-2xl font-bold text-green-600">{selectedAgent.healthScore}%</div>
                      <div className="text-sm text-gray-600">Health Score</div>
                    </div>
                    <div className="text-center">
                      <div className="text-2xl font-bold text-blue-600">{selectedAgent.complianceScore}%</div>
                      <div className="text-sm text-gray-600">Compliance</div>
                    </div>
                    <div className="text-center">
                      <div className={`text-2xl font-bold ${selectedAgent.violations === 0 ? 'text-green-600' : 'text-red-600'}`}>
                        {selectedAgent.violations}
                      </div>
                      <div className="text-sm text-gray-600">Violations</div>
                    </div>
                  </div>
                </div>

                {/* Tabs */}
                <div className="border-b border-gray-200">
                  <nav className="-mb-px flex space-x-8">
                    {['overview', 'health-metrics', 'compliance', 'alerts', 'audit-logs'].map((tab) => (
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
                  {/* Quick Stats */}
                  <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
                    <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
                      <div className="flex items-center justify-between">
                        <div>
                          <p className="text-sm text-gray-600">Uptime</p>
                          <p className="text-2xl font-bold text-green-600">{selectedAgent.uptime}%</p>
                        </div>
                        <Activity className="w-8 h-8 text-green-600" />
                      </div>
                    </div>
                    
                    <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
                      <div className="flex items-center justify-between">
                        <div>
                          <p className="text-sm text-gray-600">Response Time</p>
                          <p className="text-2xl font-bold text-blue-600">{selectedAgent.responseTime}ms</p>
                        </div>
                        <Clock className="w-8 h-8 text-blue-600" />
                      </div>
                    </div>
                    
                    <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
                      <div className="flex items-center justify-between">
                        <div>
                          <p className="text-sm text-gray-600">Error Rate</p>
                          <p className="text-2xl font-bold text-orange-600">{selectedAgent.errorRate}%</p>
                        </div>
                        <AlertTriangle className="w-8 h-8 text-orange-600" />
                      </div>
                    </div>
                    
                    <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
                      <div className="flex items-center justify-between">
                        <div>
                          <p className="text-sm text-gray-600">Interactions</p>
                          <p className="text-2xl font-bold text-purple-600">{selectedAgent.totalInteractions.toLocaleString()}</p>
                        </div>
                        <Users className="w-8 h-8 text-purple-600" />
                      </div>
                    </div>
                  </div>

                  {/* Compliance Frameworks Status */}
                  <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
                    <h3 className="text-lg font-semibold text-gray-900 mb-4">Compliance Status</h3>
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                      {complianceFrameworks.slice(0, 4).map((framework) => (
                        <div key={framework.name} className="flex items-center justify-between p-4 bg-gray-50 rounded-lg">
                          <div className="flex items-center space-x-3">
                            <framework.icon className="w-5 h-5 text-gray-600" />
                            <div>
                              <h4 className="font-medium text-gray-900">{framework.name}</h4>
                              <p className="text-sm text-gray-600">Score: {framework.score}%</p>
                            </div>
                          </div>
                          <span className={`px-3 py-1 rounded-full text-xs font-medium ${getStatusColor(framework.status)}`}>
                            {framework.status}
                          </span>
                        </div>
                      ))}
                    </div>
                  </div>
                </div>
              )}

              {activeTab === 'health-metrics' && (
                <div className="space-y-6">
                  <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                    {healthMetrics.map((metric) => {
                      const IconComponent = metric.icon;
                      return (
                        <div key={metric.name} className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
                          <div className="flex items-center justify-between mb-4">
                            <div className="flex items-center space-x-3">
                              <div className={`p-2 rounded-lg ${
                                metric.status === 'good' ? 'bg-green-100' :
                                metric.status === 'warning' ? 'bg-yellow-100' : 'bg-red-100'
                              }`}>
                                <IconComponent className={`w-5 h-5 ${
                                  metric.status === 'good' ? 'text-green-600' :
                                  metric.status === 'warning' ? 'text-yellow-600' : 'text-red-600'
                                }`} />
                              </div>
                              <h3 className="font-medium text-gray-900">{metric.name}</h3>
                            </div>
                            <span className={`px-2 py-1 rounded-full text-xs font-medium ${getStatusColor(metric.status)}`}>
                              {metric.status}
                            </span>
                          </div>
                          
                          <div className="mb-3">
                            <div className="flex items-baseline space-x-2">
                              <span className="text-2xl font-bold text-gray-900">{metric.value}</span>
                              <span className="text-sm text-gray-600">{metric.unit}</span>
                            </div>
                            <div className="text-sm text-gray-500 mt-1">
                              Threshold: {metric.threshold}{metric.unit}
                            </div>
                          </div>
                          
                          <p className="text-sm text-gray-600">{metric.description}</p>
                        </div>
                      );
                    })}
                  </div>
                </div>
              )}

              {activeTab === 'compliance' && (
                <div className="space-y-6">
                  {complianceFrameworks.map((framework) => {
                    const IconComponent = framework.icon;
                    return (
                      <div key={framework.name} className="bg-white rounded-lg shadow-sm border border-gray-200">
                        <div className="p-6 border-b border-gray-200">
                          <div className="flex items-center justify-between">
                            <div className="flex items-center space-x-4">
                              <IconComponent className="w-6 h-6 text-gray-600" />
                              <div>
                                <h3 className="text-lg font-semibold text-gray-900">{framework.name}</h3>
                                <p className="text-sm text-gray-600">{framework.fullName}</p>
                              </div>
                            </div>
                            <div className="text-right">
                              <span className={`px-3 py-1 rounded-full text-sm font-medium ${getStatusColor(framework.status)}`}>
                                {framework.status} - {framework.score}%
                              </span>
                              <p className="text-xs text-gray-500 mt-1">Last audit: {framework.lastAudit}</p>
                            </div>
                          </div>
                        </div>
                        
                        <div className="p-6">
                          <h4 className="font-medium text-gray-900 mb-4">Requirements Status</h4>
                          <div className="space-y-3">
                            {framework.requirements.map((req, index) => (
                              <div key={index} className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
                                <div className="flex items-center space-x-3">
                                  <div className={`w-3 h-3 rounded-full ${
                                    req.status === 'compliant' ? 'bg-green-500' : 'bg-red-500'
                                  }`}></div>
                                  <span className="text-sm font-medium text-gray-900">{req.name}</span>
                                  {req.critical && (
                                    <span className="bg-red-100 text-red-800 px-2 py-1 rounded-full text-xs font-medium">
                                      Critical
                                    </span>
                                  )}
                                </div>
                                <span className={`px-2 py-1 rounded-full text-xs font-medium ${getStatusColor(req.status)}`}>
                                  {req.status}
                                </span>
                              </div>
                            ))}
                          </div>
                        </div>
                      </div>
                    );
                  })}
                </div>
              )}

              {activeTab === 'alerts' && (
                <div className="space-y-6">
                  <div className="bg-white rounded-lg shadow-sm border border-gray-200">
                    <div className="p-6 border-b border-gray-200">
                      <h3 className="text-lg font-semibold text-gray-900">Recent Alerts & Violations</h3>
                    </div>
                    <div className="divide-y divide-gray-200">
                      {recentAlerts.map((alert) => (
                        <div key={alert.id} className="p-6 hover:bg-gray-50">
                          <div className="flex items-start justify-between">
                            <div className="flex items-start space-x-4">
                              <div className={`p-2 rounded-lg ${
                                alert.type === 'violation' ? 'bg-red-100' :
                                alert.type === 'warning' ? 'bg-yellow-100' : 'bg-blue-100'
                              }`}>
                                {alert.type === 'violation' ? (
                                  <AlertTriangle className={`w-4 h-4 ${
                                    alert.type === 'violation' ? 'text-red-600' :
                                    alert.type === 'warning' ? 'text-yellow-600' : 'text-blue-600'
                                  }`} />
                                ) : alert.type === 'warning' ? (
                                  <AlertCircle className="w-4 h-4 text-yellow-600" />
                                ) : (
                                  <CheckCircle className="w-4 h-4 text-blue-600" />
                                )}
                              </div>
                              <div className="flex-1">
                                <div className="flex items-center space-x-3 mb-2">
                                  <h4 className="font-medium text-gray-900">{alert.framework}</h4>
                                  <span className={`px-2 py-1 rounded-full text-xs font-medium ${getSeverityColor(alert.severity)}`}>
                                    {alert.severity}
                                  </span>
                                </div>
                                <p className="text-sm text-gray-700">{alert.message}</p>
                                <div className="flex items-center space-x-4 mt-2 text-xs text-gray-500">
                                  <span>{alert.timestamp}</span>
                                  <span>Agent: {alert.agent}</span>
                                </div>
                              </div>
                            </div>
                            <div className="flex items-center space-x-2">
                              {alert.resolved ? (
                                <span className="bg-green-100 text-green-800 px-2 py-1 rounded-full text-xs font-medium">
                                  Resolved
                                </span>
                              ) : (
                                <button className="bg-blue-600 text-white px-3 py-1 rounded text-xs hover:bg-blue-700 transition-colors">
                                  Resolve
                                </button>
                              )}
                            </div>
                          </div>
                        </div>
                      ))}
                    </div>
                  </div>
                </div>
              )}

              {activeTab === 'audit-logs' && (
                <div className="bg-white rounded-lg shadow-sm border border-gray-200">
                  <div className="p-6 border-b border-gray-200">
                    <div className="flex items-center justify-between">
                      <h3 className="text-lg font-semibold text-gray-900">Audit Logs</h3>
                      <button className="bg-green-600 text-white px-4 py-2 rounded-lg flex items-center space-x-2 hover:bg-green-700 transition-colors">
                        <Download className="w-4 h-4" />
                        <span>Export Logs</span>
                      </button>
                    </div>
                  </div>
                  <div className="divide-y divide-gray-200">
                    {[
                      {
                        timestamp: '2025-01-28 10:30:15',
                        user: 'System',
                        action: 'Compliance Check Completed',
                        details: 'HIPAA compliance verification passed',
                        status: 'Success'
                      },
                      {
                        timestamp: '2025-01-28 09:45:22',
                        user: 'Admin',
                        action: 'Access Control Updated',
                        details: 'Modified user permissions for PHI access',
                        status: 'Success'
                      },
                      {
                        timestamp: '2025-01-28 09:30:08',
                        user: 'System',
                        action: 'Security Scan',
                        details: 'Automated vulnerability assessment completed',
                        status: 'Success'
                      },
                      {
                        timestamp: '2025-01-28 08:15:33',
                        user: 'Patient Portal Assistant',
                        action: 'Data Access Violation',
                        details: 'Attempted access to restricted patient records',
                        status: 'Violation'
                      },
                      {
                        timestamp: '2025-01-28 07:45:12',
                        user: 'System',
                        action: 'Backup Completed',
                        details: 'Daily encrypted backup of patient data',
                        status: 'Success'
                      },
                      {
                        timestamp: '2025-01-28 06:30:00',
                        user: 'System',
                        action: 'Health Check',
                        details: 'All agent health metrics within normal range',
                        status: 'Success'
                      }
                    ].map((log, index) => (
                      <div key={index} className="p-6 hover:bg-gray-50">
                        <div className="flex items-center justify-between">
                          <div className="flex-1">
                            <div className="flex items-center space-x-3 mb-2">
                              <h4 className="font-medium text-gray-900">{log.action}</h4>
                              <span className={`px-2 py-1 rounded-full text-xs font-medium ${
                                log.status === 'Success' ? 'bg-green-100 text-green-800' :
                                log.status === 'Violation' ? 'bg-red-100 text-red-800' :
                                'bg-yellow-100 text-yellow-800'
                              }`}>
                                {log.status}
                              </span>
                            </div>
                            <p className="text-sm text-gray-700 mb-2">{log.details}</p>
                            <div className="flex items-center space-x-4 text-xs text-gray-500">
                              <span>{log.timestamp}</span>
                              <span>User: {log.user}</span>
                            </div>
                          </div>
                          <button className="p-2 text-gray-400 hover:text-gray-600">
                            <Eye className="w-4 h-4" />
                          </button>
                        </div>
                      </div>
                    ))}
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

export default AgentMonitoringCompliance;