// File: src/pages/Dashboard.js - Dashboard Page
import React from 'react';
import { Link } from 'react-router-dom';
import { CheckCircle, Clock, Users, Plus, User, TrendingUp } from 'lucide-react';
import Card from '../components/common/Card';
import Button from '../components/common/Button';
import { useAuthorization } from '../contexts/AuthorizationContext';

const Dashboard = () => {
  const { requests, patients } = useAuthorization();

  const stats = [
    {
      title: 'Approved Authorizations',
      value: requests.filter(r => r.result?.response_code === 'A1').length,
      icon: CheckCircle,
      color: 'text-green-600',
      bgColor: 'bg-green-50'
    },
    {
      title: 'Pending Requests',
      value: requests.filter(r => r.status === 'submitted').length,
      icon: Clock,
      color: 'text-yellow-600',
      bgColor: 'bg-yellow-50'
    },
    {
      title: 'Registered Patients',
      value: patients.length,
      icon: Users,
      color: 'text-blue-600',
      bgColor: 'bg-blue-50'
    },
    {
      title: 'Success Rate',
      value: requests.length > 0 ? `${Math.round((requests.filter(r => r.result?.response_code === 'A1').length / requests.length) * 100)}%` : '0%',
      icon: TrendingUp,
      color: 'text-purple-600',
      bgColor: 'bg-purple-50'
    }
  ];

  const quickActions = [
    {
      title: 'EDI 278 Prior Authorization',
      description: 'Submit new prior authorization requests for medical procedures and services.',
      icon: CheckCircle,
      link: '/prior-authorization',
      color: 'bg-purple-600'
    },
    {
      title: 'EDI 275 Patient Information',
      description: 'Manage patient demographics, insurance, and medical information.',
      icon: User,
      link: '/patient-information',
      color: 'bg-blue-600'
    }
  ];

  return (
    <div className="space-y-8">
      <div className="text-center">
        <h1 className="text-3xl font-bold text-gray-900 mb-4">
          Prior Authorization Dashboard
        </h1>
        <p className="text-lg text-gray-600 max-w-2xl mx-auto">
          Manage healthcare prior authorizations with EDI 278 transactions and patient information with EDI 275
        </p>
      </div>

      {/* Statistics Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        {stats.map(({ title, value, icon: Icon, color, bgColor }) => (
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
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {quickActions.map(({ title, description, icon: Icon, link, color }) => (
            <Card key={title} className="hover:shadow-lg transition-shadow">
              <div className="flex items-start space-x-4">
                <div className={`flex-shrink-0 ${color} rounded-lg p-3`}>
                  <Icon className="h-6 w-6 text-white" />
                </div>
                <div className="flex-1">
                  <h3 className="text-lg font-medium text-gray-900 mb-2">{title}</h3>
                  <p className="text-sm text-gray-600 mb-4">{description}</p>
                  <Link to={link}>
                    <Button icon={Plus} size="small">
                      Get Started
                    </Button>
                  </Link>
                </div>
              </div>
            </Card>
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
                      request.result?.response_code === 'A1' ? 'bg-green-400' : 'bg-yellow-400'
                    }`}></div>
                    <div>
                      <p className="text-sm font-medium text-gray-900">
                        {request.patient_name}
                      </p>
                      <p className="text-xs text-gray-500">
                        Request {request.id.slice(0, 8)}... | Member: {request.member_id}
                      </p>
                    </div>
                  </div>
                  <div className="text-right">
                    <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${
                      request.result?.response_code === 'A1'
                        ? 'bg-green-100 text-green-800'
                        : 'bg-yellow-100 text-yellow-800'
                    }`}>
                      {request.result?.response_code === 'A1' ? 'Approved' : 'Pending'}
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
