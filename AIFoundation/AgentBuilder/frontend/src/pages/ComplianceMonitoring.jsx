import React, { useState, useEffect } from 'react';
import { Shield, AlertTriangle, CheckCircle, FileText } from 'lucide-react';
import ComplianceOverview from '../components/compliance/ComplianceOverview';
import ComplianceControls from '../components/compliance/ComplianceControls';

const ComplianceMonitoring = () => {
  const [complianceData, setComplianceData] = useState({
    overview: {
      score: 94,
      lastAudit: '2024-12-15',
      status: 'compliant',
      issues: 2
    },
    controls: [],
    recentActivity: []
  });

  useEffect(() => {
    // Mock data - replace with real API calls
    setComplianceData({
      overview: {
        score: 94,
        lastAudit: '2024-12-15',
        status: 'compliant',
        issues: 2
      },
      controls: [
        { name: 'Data Encryption', status: 'compliant', lastCheck: '2025-01-02' },
        { name: 'Access Controls', status: 'compliant', lastCheck: '2025-01-02' },
        { name: 'Audit Logging', status: 'compliant', lastCheck: '2025-01-02' },
        { name: 'Data Backup', status: 'warning', lastCheck: '2025-01-01' },
        { name: 'User Training', status: 'non-compliant', lastCheck: '2024-12-20' },
        { name: 'Incident Response', status: 'compliant', lastCheck: '2025-01-01' }
      ],
      recentActivity: [
        { type: 'audit', message: 'Automated security scan completed', timestamp: '2 hours ago' },
        { type: 'warning', message: 'User attempted unauthorized access', timestamp: '1 day ago' },
        { type: 'update', message: 'Security policy updated', timestamp: '3 days ago' },
        { type: 'training', message: 'Staff completed HIPAA training', timestamp: '1 week ago' }
      ]
    });
  }, []);

  const getActivityIcon = (type) => {
    switch (type) {
      case 'audit':
        return <Shield className="w-4 h-4 text-blue-600" />;
      case 'warning':
        return <AlertTriangle className="w-4 h-4 text-yellow-600" />;
      case 'update':
        return <CheckCircle className="w-4 h-4 text-green-600" />;
      case 'training':
        return <FileText className="w-4 h-4 text-purple-600" />;
      default:
        return <Shield className="w-4 h-4 text-gray-600" />;
    }
  };

  const getActivityColor = (type) => {
    switch (type) {
      case 'audit':
        return 'bg-blue-100';
      case 'warning':
        return 'bg-yellow-100';
      case 'update':
        return 'bg-green-100';
      case 'training':
        return 'bg-purple-100';
      default:
        return 'bg-gray-100';
    }
  };

  return (
    <div className="p-8">
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900 mb-2">HIPAA Compliance Dashboard</h1>
        <p className="text-gray-600">Monitor and maintain HIPAA compliance across your AI agents</p>
      </div>

      {/* Compliance Overview */}
      <div className="mb-8">
        <ComplianceOverview overview={complianceData.overview} />
      </div>

      {/* Compliance Controls */}
      <div className="mb-8">
        <ComplianceControls controls={complianceData.controls} />
      </div>

      {/* Recent Security Activity */}
      <div className="bg-white rounded-xl shadow-sm border">
        <div className="p-6 border-b">
          <h2 className="text-xl font-semibold text-gray-900">Recent Security Activity</h2>
        </div>
        <div className="p-6">
          <div className="space-y-4">
            {complianceData.recentActivity.map((activity, index) => (
              <div key={index} className="flex items-center space-x-4 p-4 border border-gray-200 rounded-lg">
                <div className={`p-2 rounded-full ${getActivityColor(activity.type)}`}>
                  {getActivityIcon(activity.type)}
                </div>
                <div className="flex-1">
                  <p className="text-sm font-medium text-gray-900">{activity.message}</p>
                  <p className="text-sm text-gray-500">{activity.timestamp}</p>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
};

export default ComplianceMonitoring;
