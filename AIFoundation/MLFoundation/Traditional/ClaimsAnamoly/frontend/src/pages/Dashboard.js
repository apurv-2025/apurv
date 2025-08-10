import React, { useEffect, useState, useCallback } from 'react';
import { 
  ChartBarIcon, 
  ServerIcon, 
  ExclamationTriangleIcon,
  CheckCircleIcon,
  ClockIcon
} from '@heroicons/react/24/outline';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, PieChart, Pie, Cell } from 'recharts';
import { useAppStore } from '../store/appStore';
import { apiService } from '../services/apiService';

const stats = [
  { name: 'Total Claims', stat: '5,000', icon: ChartBarIcon, change: '+12%', changeType: 'increase' },
  { name: 'Anomalies Detected', stat: '400', icon: ExclamationTriangleIcon, change: '+8%', changeType: 'increase' },
  { name: 'Model Accuracy', stat: '94.2%', icon: CheckCircleIcon, change: '+2.1%', changeType: 'increase' },
  { name: 'API Response Time', stat: '45ms', icon: ClockIcon, change: '-12%', changeType: 'decrease' },
];

const anomalyData = [
  { name: 'Normal', value: 4600, color: '#10B981' },
  { name: 'Anomalous', value: 400, color: '#EF4444' },
];

const performanceData = [
  { time: '00:00', accuracy: 92, precision: 89, recall: 85 },
  { time: '04:00', accuracy: 93, precision: 90, recall: 87 },
  { time: '08:00', accuracy: 94, precision: 91, recall: 88 },
  { time: '12:00', accuracy: 94.2, precision: 91.5, recall: 89 },
  { time: '16:00', accuracy: 94.5, precision: 92, recall: 89.5 },
  { time: '20:00', accuracy: 94.2, precision: 91.8, recall: 89.2 },
];

function Dashboard() {
  const { addNotification } = useAppStore();
  const [systemStatus, setSystemStatus] = useState('loading');

  const checkSystemHealth = useCallback(async () => {
    try {
      const response = await apiService.getHealth();
      setSystemStatus(response.status === 'healthy' ? 'healthy' : 'unhealthy');
    } catch (error) {
      setSystemStatus('unhealthy');
      addNotification({
        type: 'error',
        title: 'System Health Check Failed',
        message: 'Unable to connect to the API server'
      });
    }
  }, [addNotification]);

  useEffect(() => {
    checkSystemHealth();
    const interval = setInterval(checkSystemHealth, 30000); // Check every 30 seconds
    return () => clearInterval(interval);
  }, [checkSystemHealth]);

  const getStatusColor = (status) => {
    switch (status) {
      case 'healthy':
        return 'text-success-600 bg-success-100';
      case 'unhealthy':
        return 'text-danger-600 bg-danger-100';
      default:
        return 'text-warning-600 bg-warning-100';
    }
  };

  const getStatusIcon = (status) => {
    switch (status) {
      case 'healthy':
        return <CheckCircleIcon className="h-5 w-5" />;
      case 'unhealthy':
        return <ExclamationTriangleIcon className="h-5 w-5" />;
      default:
        return <ClockIcon className="h-5 w-5" />;
    }
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="md:flex md:items-center md:justify-between">
        <div className="min-w-0 flex-1">
          <h2 className="text-2xl font-bold leading-7 text-gray-900 sm:truncate sm:text-3xl sm:tracking-tight">
            Dashboard
          </h2>
        </div>
        <div className="mt-4 flex md:ml-4 md:mt-0">
          <div className={`inline-flex items-center rounded-full px-3 py-1 text-sm font-medium ${getStatusColor(systemStatus)}`}>
            {getStatusIcon(systemStatus)}
            <span className="ml-2 capitalize">{systemStatus}</span>
          </div>
        </div>
      </div>

      {/* Stats */}
      <div className="grid grid-cols-1 gap-5 sm:grid-cols-2 lg:grid-cols-4">
        {stats.map((item) => (
          <div key={item.name} className="relative overflow-hidden rounded-lg bg-white px-4 pb-12 pt-5 shadow sm:px-6 sm:pt-6">
            <dt>
              <div className="absolute rounded-md bg-primary-500 p-3">
                <item.icon className="h-6 w-6 text-white" aria-hidden="true" />
              </div>
              <p className="ml-16 truncate text-sm font-medium text-gray-500">{item.name}</p>
            </dt>
            <dd className="ml-16 flex items-baseline pb-6 sm:pb-7">
              <p className="text-2xl font-semibold text-gray-900">{item.stat}</p>
              <p
                className={`ml-2 flex items-baseline text-sm font-semibold ${
                  item.changeType === 'increase' ? 'text-success-600' : 'text-danger-600'
                }`}
              >
                {item.change}
              </p>
            </dd>
          </div>
        ))}
      </div>

      {/* Charts */}
      <div className="grid grid-cols-1 gap-6 lg:grid-cols-2">
        {/* Performance Chart */}
        <div className="bg-white shadow rounded-lg p-6">
          <h3 className="text-lg font-medium text-gray-900 mb-4">Model Performance Over Time</h3>
          <ResponsiveContainer width="100%" height={300}>
            <LineChart data={performanceData}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="time" />
              <YAxis />
              <Tooltip />
              <Line type="monotone" dataKey="accuracy" stroke="#3B82F6" strokeWidth={2} name="Accuracy" />
              <Line type="monotone" dataKey="precision" stroke="#10B981" strokeWidth={2} name="Precision" />
              <Line type="monotone" dataKey="recall" stroke="#F59E0B" strokeWidth={2} name="Recall" />
            </LineChart>
          </ResponsiveContainer>
        </div>

        {/* Anomaly Distribution */}
        <div className="bg-white shadow rounded-lg p-6">
          <h3 className="text-lg font-medium text-gray-900 mb-4">Claims Distribution</h3>
          <ResponsiveContainer width="100%" height={300}>
            <PieChart>
              <Pie
                data={anomalyData}
                cx="50%"
                cy="50%"
                labelLine={false}
                label={({ name, percent }) => `${name} ${(percent * 100).toFixed(0)}%`}
                outerRadius={80}
                fill="#8884d8"
                dataKey="value"
              >
                {anomalyData.map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={entry.color} />
                ))}
              </Pie>
              <Tooltip />
            </PieChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* Recent Activity */}
      <div className="bg-white shadow rounded-lg">
        <div className="px-4 py-5 sm:p-6">
          <h3 className="text-lg font-medium text-gray-900 mb-4">Recent Activity</h3>
          <div className="flow-root">
            <ul className="-mb-8">
              <li>
                <div className="relative pb-8">
                  <span className="absolute top-4 left-4 -ml-px h-full w-0.5 bg-gray-200" aria-hidden="true" />
                  <div className="relative flex space-x-3">
                    <div>
                      <span className="h-8 w-8 rounded-full bg-success-500 flex items-center justify-center ring-8 ring-white">
                        <CheckCircleIcon className="h-5 w-5 text-white" />
                      </span>
                    </div>
                    <div className="flex min-w-0 flex-1 justify-between space-x-4 pt-1.5">
                      <div>
                        <p className="text-sm text-gray-500">
                          Model training completed with <span className="font-medium text-gray-900">94.2% accuracy</span>
                        </p>
                      </div>
                      <div className="whitespace-nowrap text-right text-sm text-gray-500">
                        <time dateTime="2025-08-10">2 hours ago</time>
                      </div>
                    </div>
                  </div>
                </div>
              </li>
              <li>
                <div className="relative pb-8">
                  <span className="absolute top-4 left-4 -ml-px h-full w-0.5 bg-gray-200" aria-hidden="true" />
                  <div className="relative flex space-x-3">
                    <div>
                      <span className="h-8 w-8 rounded-full bg-primary-500 flex items-center justify-center ring-8 ring-white">
                        <ServerIcon className="h-5 w-5 text-white" />
                      </span>
                    </div>
                    <div className="flex min-w-0 flex-1 justify-between space-x-4 pt-1.5">
                      <div>
                        <p className="text-sm text-gray-500">
                          API server started on <span className="font-medium text-gray-900">port 8000</span>
                        </p>
                      </div>
                      <div className="whitespace-nowrap text-right text-sm text-gray-500">
                        <time dateTime="2025-08-10">4 hours ago</time>
                      </div>
                    </div>
                  </div>
                </div>
              </li>
              <li>
                <div className="relative pb-8">
                  <div className="relative flex space-x-3">
                    <div>
                      <span className="h-8 w-8 rounded-full bg-warning-500 flex items-center justify-center ring-8 ring-white">
                        <ExclamationTriangleIcon className="h-5 w-5 text-white" />
                      </span>
                    </div>
                    <div className="flex min-w-0 flex-1 justify-between space-x-4 pt-1.5">
                      <div>
                        <p className="text-sm text-gray-500">
                          <span className="font-medium text-gray-900">400 anomalies</span> detected in latest batch
                        </p>
                      </div>
                      <div className="whitespace-nowrap text-right text-sm text-gray-500">
                        <time dateTime="2025-08-10">6 hours ago</time>
                      </div>
                    </div>
                  </div>
                </div>
              </li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  );
}

export default Dashboard; 