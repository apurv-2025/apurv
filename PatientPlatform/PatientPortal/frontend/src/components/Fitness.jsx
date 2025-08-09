import React, { useState } from 'react';
import { Activity, Heart, TrendingUp, Watch, Smartphone, Zap, Target, Award } from 'lucide-react';
import { useAPI } from '../hooks/useAPI';
import { fitnessAPI } from '../services/api';

const Fitness = () => {
  const [selectedPeriod, setSelectedPeriod] = useState('week');
  const { data: fitnessData, error, refetch } = useAPI(() => fitnessAPI.getFitnessData(selectedPeriod), [selectedPeriod]);

  const mockData = {
    summary: {
      steps: 8425,
      calories: 342,
      activeMinutes: 45,
      heartRate: 72,
      distance: 5.2
    },
    devices: [
      { id: 1, name: 'Apple Watch Series 8', type: 'watch', status: 'connected', lastSync: '2 minutes ago', iconType: 'watch' },
      { id: 2, name: 'iPhone Health App', type: 'phone', status: 'connected', lastSync: '5 minutes ago', iconType: 'phone' },
      { id: 3, name: 'Fitbit Charge 5', type: 'tracker', status: 'disconnected', lastSync: '2 hours ago', iconType: 'activity' }
    ],
    goals: [
      { title: 'Daily Steps', current: 8425, target: 10000, unit: 'steps' },
      { title: 'Active Minutes', current: 45, target: 60, unit: 'min' },
      { title: 'Calories Burned', current: 342, target: 500, unit: 'cal' }
    ],
    weeklyTrend: [
      { day: 'Mon', steps: 7200, calories: 280 },
      { day: 'Tue', steps: 9100, calories: 365 },
      { day: 'Wed', steps: 8800, calories: 340 },
      { day: 'Thu', steps: 7600, calories: 295 },
      { day: 'Fri', steps: 10200, calories: 425 },
      { day: 'Sat', steps: 6800, calories: 310 },
      { day: 'Sun', steps: 8425, calories: 342 }
    ]
  };

  const data = fitnessData || mockData;

  const StatCard = ({ title, value, unit, icon: Icon, trend }) => (
    <div className="bg-white p-6 rounded-lg shadow-md border border-gray-200">
      <div className="flex items-center justify-between">
        <div>
          <p className="text-sm text-gray-600 mb-1">{title}</p>
          <p className="text-2xl font-bold text-gray-900">
            {value?.toLocaleString()} <span className="text-sm font-normal text-gray-500">{unit}</span>
          </p>
          {trend && (
            <div className="flex items-center mt-2">
              <TrendingUp className="w-4 h-4 text-green-500 mr-1" />
              <span className="text-sm text-green-600">+{trend}% vs last week</span>
            </div>
          )}
        </div>
        <div className="p-3 bg-blue-50 rounded-full">
          <Icon className="w-6 h-6 text-blue-600" />
        </div>
      </div>
    </div>
  );

  const GoalProgress = ({ title, current, target, unit }) => {
    const percentage = Math.min((current / target) * 100, 100);
    return (
      <div className="bg-white p-4 rounded-lg border border-gray-200">
        <div className="flex justify-between items-center mb-2">
          <h4 className="font-medium text-gray-900">{title}</h4>
          <span className="text-sm text-gray-600">{current}/{target} {unit}</span>
        </div>
        <div className="w-full bg-gray-200 rounded-full h-2">
          <div 
            className="bg-blue-600 h-2 rounded-full transition-all duration-300"
            style={{ width: `${Math.min(percentage, 100)}%` }}
          ></div>
        </div>
        <p className="text-xs text-gray-500 mt-1">{percentage.toFixed(0)}% of daily goal</p>
      </div>
    );
  };

  const DeviceCard = ({ device }) => {
    const getIcon = (iconType) => {
      switch (iconType) {
        case 'watch': return Watch;
        case 'phone': return Smartphone;
        case 'activity': return Activity;
        default: return Activity;
      }
    };
    
    const Icon = getIcon(device.iconType);
    return (
      <div className="bg-white p-4 rounded-lg border border-gray-200">
        <div className="flex items-center space-x-3">
          <div className={`p-2 rounded-full ${device.status === 'connected' ? 'bg-green-50' : 'bg-red-50'}`}>
            <Icon className={`w-5 h-5 ${device.status === 'connected' ? 'text-green-600' : 'text-red-600'}`} />
          </div>
          <div className="flex-1">
            <h4 className="font-medium text-gray-900">{device.name}</h4>
            <p className="text-sm text-gray-600">Last sync: {device.lastSync}</p>
          </div>
          <div className={`px-2 py-1 rounded-full text-xs font-medium ${
            device.status === 'connected' 
              ? 'bg-green-100 text-green-800' 
              : 'bg-red-100 text-red-800'
          }`}>
            {device.status}
          </div>
        </div>
      </div>
    );
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">Fitness Dashboard</h1>
          <p className="text-gray-600">Track your activity and health metrics</p>
        </div>
        <div className="flex space-x-2">
          {['day', 'week', 'month'].map(period => (
            <button
              key={period}
              onClick={() => setSelectedPeriod(period)}
              className={`px-4 py-2 rounded-lg text-sm font-medium transition-colors ${
                selectedPeriod === period
                  ? 'bg-blue-600 text-white'
                  : 'bg-white text-gray-700 border border-gray-300 hover:bg-gray-50'
              }`}
            >
              {period.charAt(0).toUpperCase() + period.slice(1)}
            </button>
          ))}
        </div>
      </div>

      {/* Summary Stats */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-5 gap-6">
        <StatCard title="Steps" value={data.summary?.steps} unit="steps" icon={Activity} trend={8} />
        <StatCard title="Calories" value={data.summary?.calories} unit="cal" icon={Zap} trend={12} />
        <StatCard title="Active Minutes" value={data.summary?.activeMinutes} unit="min" icon={Target} trend={5} />
        <StatCard title="Heart Rate" value={data.summary?.heartRate} unit="bpm" icon={Heart} />
        <StatCard title="Distance" value={data.summary?.distance} unit="km" icon={TrendingUp} trend={15} />
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Daily Goals */}
        <div className="bg-white p-6 rounded-lg shadow-md border border-gray-200">
          <div className="flex items-center justify-between mb-4">
            <h2 className="text-lg font-semibold text-gray-900">Daily Goals</h2>
            <Award className="w-5 h-5 text-yellow-500" />
          </div>
          <div className="space-y-4">
            {data.goals?.map((goal, index) => (
              <GoalProgress key={index} {...goal} />
            ))}
          </div>
        </div>

        {/* Connected Devices */}
        <div className="bg-white p-6 rounded-lg shadow-md border border-gray-200">
          <h2 className="text-lg font-semibold text-gray-900 mb-4">Connected Devices</h2>
          <div className="space-y-3">
            {data.devices?.map(device => (
              <DeviceCard key={device.id} device={device} />
            ))}
          </div>
          <button className="w-full mt-4 px-4 py-2 border border-blue-600 text-blue-600 rounded-lg hover:bg-blue-50 transition-colors">
            + Add New Device
          </button>
        </div>

        {/* Weekly Trend */}
        <div className="bg-white p-6 rounded-lg shadow-md border border-gray-200">
          <h2 className="text-lg font-semibold text-gray-900 mb-4">Weekly Activity</h2>
          <div className="space-y-3">
            {data.weeklyTrend?.map((day, index) => (
              <div key={index} className="flex items-center justify-between">
                <span className="text-sm text-gray-600 w-12">{day.day}</span>
                <div className="flex-1 mx-3">
                  <div className="bg-gray-200 rounded-full h-2">
                    <div 
                      className="bg-blue-600 h-2 rounded-full"
                      style={{ width: `${(day.steps / 12000) * 100}%` }}
                    ></div>
                  </div>
                </div>
                <span className="text-sm text-gray-900 w-16 text-right">{day.steps}</span>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Integration Status */}
      <div className="bg-gradient-to-r from-blue-50 to-indigo-50 p-6 rounded-lg border border-blue-200">
        <div className="flex items-center space-x-3">
          <div className="p-2 bg-blue-600 rounded-full">
            <Activity className="w-5 h-5 text-white" />
          </div>
          <div>
            <h3 className="font-semibold text-gray-900">Fitness Integration Active</h3>
            <p className="text-gray-600">Data is being synced from 2 connected devices. Last updated 2 minutes ago.</p>
          </div>
        </div>
      </div>

      {error && (
        <div className="bg-red-50 border border-red-200 rounded-lg p-4">
          <p className="text-red-700">Error loading fitness data: {error}</p>
          <button 
            onClick={refetch}
            className="mt-2 px-4 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700 transition-colors"
          >
            Retry
          </button>
        </div>
      )}
    </div>
  );
};

export default Fitness;