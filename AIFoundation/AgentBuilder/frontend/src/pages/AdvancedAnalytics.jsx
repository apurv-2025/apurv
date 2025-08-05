import React, { useState, useEffect } from 'react';
import { Download } from 'lucide-react';
import MetricCard from '../components/dashboard/MetricCard';
import { InteractionsChart, UsageDistributionChart } from '../components/charts/AnalyticsCharts';
import ActivityFeed from '../components/dashboard/ActivityFeed';

const AdvancedAnalytics = () => {
  const [timeRange, setTimeRange] = useState('7d');
  const [analytics, setAnalytics] = useState({
    interactions: [],
    performance: [],
    usage: [],
    satisfaction: 85
  });

  useEffect(() => {
    // Mock data - replace with real API calls
    setAnalytics({
      interactions: [
        { date: '2025-01-01', billing: 45, frontDesk: 32, general: 18 },
        { date: '2025-01-02', billing: 52, frontDesk: 28, general: 24 },
        { date: '2025-01-03', billing: 38, frontDesk: 41, general: 19 },
        { date: '2025-01-04', billing: 61, frontDesk: 35, general: 22 },
        { date: '2025-01-05', billing: 48, frontDesk: 39, general: 27 },
        { date: '2025-01-06', billing: 55, frontDesk: 42, general: 31 },
        { date: '2025-01-07', billing: 43, frontDesk: 36, general: 25 }
      ],
      performance: [
        { metric: 'Response Time', value: 1.2, unit: 'seconds', trend: 'down' },
        { metric: 'Accuracy', value: 94, unit: '%', trend: 'up' },
        { metric: 'Resolution Rate', value: 87, unit: '%', trend: 'up' },
        { metric: 'User Satisfaction', value: 4.6, unit: '/5', trend: 'stable' }
      ],
      usage: [
        { name: 'Billing Queries', value: 40, color: '#3B82F6' },
        { name: 'Scheduling', value: 35, color: '#10B981' },
        { name: 'General Info', value: 15, color: '#F59E0B' },
        { name: 'Other', value: 10, color: '#6B7280' }
      ],
      satisfaction: 85
    });
  }, [timeRange]);

  const handleExportReport = () => {
    // Mock export functionality
    console.log('Exporting report for time range:', timeRange);
    alert('Report export feature would be implemented here');
  };

  return (
    <div className="p-8 bg-gray-50 min-h-screen">
      <div className="mb-8 flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold text-gray-900 mb-2">Advanced Analytics</h1>
          <p className="text-gray-600">Detailed insights into your AI agents' performance</p>
        </div>
        
        <div className="flex items-center space-x-4">
          <select
            value={timeRange}
            onChange={(e) => setTimeRange(e.target.value)}
            className="px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
          >
            <option value="24h">Last 24 Hours</option>
            <option value="7d">Last 7 Days</option>
            <option value="30d">Last 30 Days</option>
            <option value="90d">Last 90 Days</option>
          </select>
          
          <button 
            onClick={handleExportReport}
            className="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 flex items-center space-x-2"
          >
            <Download className="w-4 h-4" />
            <span>Export Report</span>
          </button>
        </div>
      </div>

      {/* Key Metrics */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
        {analytics.performance.map((metric, index) => (
          <MetricCard key={index} metric={metric} />
        ))}
      </div>

      {/* Charts */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 mb-8">
        <InteractionsChart data={analytics.interactions} />
        <UsageDistributionChart data={analytics.usage} />
      </div>

      {/* Recent Activity */}
      <ActivityFeed />
    </div>
  );
};

export default AdvancedAnalytics;
