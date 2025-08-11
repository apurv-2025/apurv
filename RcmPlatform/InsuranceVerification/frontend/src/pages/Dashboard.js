// File: src/pages/Dashboard.js
import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { Upload, CheckCircle, Clock, TrendingUp, FileText } from 'lucide-react';
import Card from '../components/common/Card';
import { useApp } from '../contexts/AppContext';

const Dashboard = () => {
  const { requests } = useApp();
  const [stats, setStats] = useState({
    totalRequests: 0,
    completedRequests: 0,
    pendingRequests: 0,
    successRate: 0
  });

  useEffect(() => {
    const calculateStats = () => {
      const total = requests.length;
      const completed = requests.filter(r => r.status === 'completed').length;
      const pending = requests.filter(r => r.status === 'submitted').length;
      const successRate = total > 0 ? (completed / total * 100).toFixed(1) : 0;

      setStats({
        totalRequests: total,
        completedRequests: completed,
        pendingRequests: pending,
        successRate
      });
    };

    calculateStats();
  }, [requests]);

  const statCards = [
    {
      title: 'Total Requests',
      value: stats.totalRequests,
      icon: FileText,
      color: 'text-blue-600',
      bgColor: 'bg-blue-50'
    },
    {
      title: 'Completed',
      value: stats.completedRequests,
      icon: CheckCircle,
      color: 'text-green-600',
      bgColor: 'bg-green-50'
    },
    {
      title: 'Pending',
      value: stats.pendingRequests,
      icon: Clock,
      color: 'text-yellow-600',
      bgColor: 'bg-yellow-50'
    },
    {
      title: 'Success Rate',
      value: `${stats.successRate}%`,
      icon: TrendingUp,
      color: 'text-purple-600',
      bgColor: 'bg-purple-50'
    }
  ];

  const quickActions = [
    {
      title: 'Upload Insurance Card',
      description: 'Upload and process insurance card images or PDFs',
      icon: Upload,
      link: '/upload',
      color: 'bg-blue-600'
    },
    {
      title: 'Check Eligibility',
      description: 'Submit EDI 270 eligibility verification requests',
      icon: CheckCircle,
      link: '/eligibility',
      color: 'bg-green-600'
    },
    {
      title: 'View History',
      description: 'Review past requests and responses',
      icon: Clock,
      link: '/history',
      color: 'bg-purple-600'
    }
  ];

  return (
    <div className="space-y-8">
      {/* Welcome Section */}
      <div className="text-center">
        <h1 className="text-3xl font-bold text-gray-900 mb-4">
          Insurance Verification Dashboard
        </h1>
        <p className="text-lg text-gray-600 max-w-2xl mx-auto">
          Streamline your health insurance verification process with our EDI 270/271 compliant system
        </p>
      </div>

      {/* Statistics Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        {statCards.map(({ title, value, icon: Icon, color, bgColor }) => (
          <Card key={title} className="text-center">
            <div className={`inline-flex items-center justify-center w-12 h-12 rounded-lg ${bgColor} mb-4`}>
              <Icon className={`h-6 w-6 ${color}`} />
            </div>
            <h3 className="text-2xl font-bold text-gray-900 mb-1">{value}</h3>
            <p className="text-sm text-gray-600">{title}</p>
          </Card>
        ))}
      </div>

      {/* Quick Actions */}
      <div>
        <h2 className="text-xl font-semibold text-gray-900 mb-6">Quick Actions</h2>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          {quickActions.map(({ title, description, icon: Icon, link, color }) => (
            <Link key={title} to={link} className="group">
              <Card className="hover:shadow-lg transition-shadow cursor-pointer">
                <div className="flex items-start space-x-4">
                  <div className={`flex-shrink-0 ${color} rounded-lg p-3`}>
                    <Icon className="h-6 w-6 text-white" />
                  </div>
                  <div>
                    <h3 className="text-lg font-medium text-gray-900 group-hover:text-blue-600">
                      {title}
                    </h3>
                    <p className="text-sm text-gray-600 mt-1">{description}</p>
                  </div>
                </div>
              </Card>
            </Link>
          ))}
        </div>
      </div>

      {/* Recent Activity */}
      {requests.length > 0 && (
        <div>
          <h2 className="text-xl font-semibold text-gray-900 mb-6">Recent Activity</h2>
          <Card>
            <div className="space-y-4">
              {requests.slice(0, 5).map((request) => (
                <div key={request.id} className="flex items-center justify-between py-3 border-b border-gray-100 last:border-b-0">
                  <div className="flex items-center space-x-3">
                    <div className={`h-3 w-3 rounded-full ${
                      request.status === 'completed' ? 'bg-green-400' : 'bg-yellow-400'
                    }`}></div>
                    <div>
                      <p className="text-sm font-medium text-gray-900">
                        Request {request.id.slice(0, 8)}...
                      </p>
                      <p className="text-xs text-gray-500">
                        Member ID: {request.member_id}
                      </p>
                    </div>
                  </div>
                  <div className="text-right">
                    <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${
                      request.status === 'completed'
                        ? 'bg-green-100 text-green-800'
                        : 'bg-yellow-100 text-yellow-800'
                    }`}>
                      {request.status}
                    </span>
                    <p className="text-xs text-gray-500 mt-1">
                      {new Date(request.timestamp).toLocaleDateString()}
                    </p>
                  </div>
                </div>
              ))}
            </div>
          </Card>
        </div>
      )}
    </div>
  );
};

export default Dashboard;
