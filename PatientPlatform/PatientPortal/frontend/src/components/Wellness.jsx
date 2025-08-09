import React, { useState } from 'react';
import { Brain, Moon, Droplets, Leaf, Wind, Smile, BarChart3, Calendar, Target, TrendingUp } from 'lucide-react';
import { useAPI } from '../hooks/useAPI';
import { wellnessAPI } from '../services/api';

const Wellness = () => {
  const [selectedCategory, setSelectedCategory] = useState('all');
  const { data: wellnessData, error, refetch } = useAPI(() => wellnessAPI.getWellnessData(), []);

  const mockData = {
    mentalHealth: {
      moodScore: 7.5,
      stressLevel: 3,
      meditationMinutes: 15,
      sleepQuality: 8.2
    },
    physicalWellness: {
      hydrationLevel: 85,
      nutritionScore: 7.8,
      recoveryScore: 8.5,
      energyLevel: 8
    },
    habits: [
      { name: 'Morning Meditation', streak: 12, target: 365, iconType: 'brain', color: 'purple' },
      { name: 'Hydration Goal', streak: 5, target: 30, iconType: 'droplets', color: 'blue' },
      { name: 'Sleep Schedule', streak: 8, target: 30, iconType: 'moon', color: 'indigo' },
      { name: 'Mindful Breathing', streak: 3, target: 21, iconType: 'wind', color: 'green' }
    ],
    apps: [
      { name: 'Headspace', type: 'Meditation', status: 'connected', sessions: 45, iconType: 'brain' },
      { name: 'MyFitnessPal', type: 'Nutrition', status: 'connected', entries: 28, iconType: 'leaf' },
      { name: 'Sleep Cycle', type: 'Sleep', status: 'connected', nights: 30, iconType: 'moon' },
      { name: 'Calm', type: 'Mindfulness', status: 'disconnected', sessions: 0, iconType: 'smile' }
    ],
    weeklyProgress: [
      { day: 'Mon', mood: 7, stress: 4, energy: 8 },
      { day: 'Tue', mood: 8, stress: 3, energy: 9 },
      { day: 'Wed', mood: 6, stress: 5, energy: 7 },
      { day: 'Thu', mood: 7, stress: 3, energy: 8 },
      { day: 'Fri', mood: 9, stress: 2, energy: 9 },
      { day: 'Sat', mood: 8, stress: 2, energy: 8 },
      { day: 'Sun', mood: 7, stress: 3, energy: 8 }
    ]
  };

  const data = wellnessData || mockData;

  const MetricCard = ({ title, value, unit, icon: Icon, color = 'blue', description }) => (
    <div className="bg-white p-6 rounded-lg shadow-md border border-gray-200">
      <div className="flex items-center justify-between">
        <div>
          <p className="text-sm text-gray-600 mb-1">{title}</p>
          <p className="text-2xl font-bold text-gray-900">
            {typeof value === 'number' ? value.toFixed(1) : value}
            <span className="text-sm font-normal text-gray-500 ml-1">{unit}</span>
          </p>
          {description && <p className="text-xs text-gray-500 mt-1">{description}</p>}
        </div>
        <div className={`p-3 rounded-full ${
          color === 'yellow' ? 'bg-yellow-50' :
          color === 'red' ? 'bg-red-50' :
          color === 'green' ? 'bg-green-50' :
          color === 'indigo' ? 'bg-indigo-50' :
          color === 'purple' ? 'bg-purple-50' :
          color === 'orange' ? 'bg-orange-50' :
          'bg-blue-50'
        }`}>
          <Icon className={`w-6 h-6 ${
            color === 'yellow' ? 'text-yellow-600' :
            color === 'red' ? 'text-red-600' :
            color === 'green' ? 'text-green-600' :
            color === 'indigo' ? 'text-indigo-600' :
            color === 'purple' ? 'text-purple-600' :
            color === 'orange' ? 'text-orange-600' :
            'text-blue-600'
          }`} />
        </div>
      </div>
    </div>
  );

  const HabitCard = ({ habit }) => {
    const percentage = (habit.streak / habit.target) * 100;
    
    const getIcon = (iconType) => {
      switch (iconType) {
        case 'brain': return Brain;
        case 'droplets': return Droplets;
        case 'moon': return Moon;
        case 'wind': return Wind;
        case 'leaf': return Leaf;
        case 'smile': return Smile;
        default: return Brain;
      }
    };
    
    const Icon = getIcon(habit.iconType);
    
    return (
      <div className="bg-white p-4 rounded-lg border border-gray-200">
        <div className="flex items-center space-x-3 mb-3">
          <div className={`p-2 rounded-full ${
            habit.color === 'purple' ? 'bg-purple-50' :
            habit.color === 'blue' ? 'bg-blue-50' :
            habit.color === 'indigo' ? 'bg-indigo-50' :
            habit.color === 'green' ? 'bg-green-50' :
            'bg-blue-50'
          }`}>
            <Icon className={`w-5 h-5 ${
              habit.color === 'purple' ? 'text-purple-600' :
              habit.color === 'blue' ? 'text-blue-600' :
              habit.color === 'indigo' ? 'text-indigo-600' :
              habit.color === 'green' ? 'text-green-600' :
              'text-blue-600'
            }`} />
          </div>
          <div className="flex-1">
            <h4 className="font-medium text-gray-900">{habit.name}</h4>
            <p className="text-sm text-gray-600">{habit.streak} day streak</p>
          </div>
        </div>
        <div className="w-full bg-gray-200 rounded-full h-2 mb-2">
          <div 
            className={`h-2 rounded-full transition-all duration-300 ${
              habit.color === 'purple' ? 'bg-purple-600' :
              habit.color === 'blue' ? 'bg-blue-600' :
              habit.color === 'indigo' ? 'bg-indigo-600' :
              habit.color === 'green' ? 'bg-green-600' :
              'bg-blue-600'
            }`}
            style={{ width: `${Math.min(percentage, 100)}%` }}
          ></div>
        </div>
        <p className="text-xs text-gray-500">{habit.streak}/{habit.target} days</p>
      </div>
    );
  };

  const AppCard = ({ app }) => {
    const getIcon = (iconType) => {
      switch (iconType) {
        case 'brain': return Brain;
        case 'droplets': return Droplets;
        case 'moon': return Moon;
        case 'wind': return Wind;
        case 'leaf': return Leaf;
        case 'smile': return Smile;
        default: return Brain;
      }
    };
    
    const Icon = getIcon(app.iconType);
    return (
      <div className="bg-white p-4 rounded-lg border border-gray-200">
        <div className="flex items-center space-x-3">
          <div className={`p-2 rounded-full ${app.status === 'connected' ? 'bg-green-50' : 'bg-gray-50'}`}>
            <Icon className={`w-5 h-5 ${app.status === 'connected' ? 'text-green-600' : 'text-gray-400'}`} />
          </div>
          <div className="flex-1">
            <h4 className="font-medium text-gray-900">{app.name}</h4>
            <p className="text-sm text-gray-600">{app.type}</p>
          </div>
          <div className="text-right">
            <div className={`px-2 py-1 rounded-full text-xs font-medium ${
              app.status === 'connected' 
                ? 'bg-green-100 text-green-800' 
                : 'bg-gray-100 text-gray-800'
            }`}>
              {app.status}
            </div>
            {app.status === 'connected' && (
              <p className="text-xs text-gray-500 mt-1">
                {app.sessions && `${app.sessions} sessions`}
                {app.entries && `${app.entries} entries`}
                {app.nights && `${app.nights} nights`}
              </p>
            )}
          </div>
        </div>
      </div>
    );
  };

  const categories = [
    { id: 'all', label: 'All', icon: BarChart3 },
    { id: 'mental', label: 'Mental Health', icon: Brain },
    { id: 'physical', label: 'Physical', icon: Target },
    { id: 'habits', label: 'Habits', icon: Calendar }
  ];

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">Wellness Center</h1>
          <p className="text-gray-600">Track your mental and physical wellbeing</p>
        </div>
        <div className="flex space-x-2">
          {categories.map(category => {
            const Icon = category.icon;
            return (
              <button
                key={category.id}
                onClick={() => setSelectedCategory(category.id)}
                className={`flex items-center space-x-2 px-4 py-2 rounded-lg text-sm font-medium transition-colors ${
                  selectedCategory === category.id
                    ? 'bg-purple-600 text-white'
                    : 'bg-white text-gray-700 border border-gray-300 hover:bg-gray-50'
                }`}
              >
                <Icon className="w-4 h-4" />
                <span>{category.label}</span>
              </button>
            );
          })}
        </div>
      </div>

      {/* Mental Health Metrics */}
      {(selectedCategory === 'all' || selectedCategory === 'mental') && (
        <div>
          <h2 className="text-lg font-semibold text-gray-900 mb-4">Mental Health</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
            <MetricCard 
              title="Mood Score" 
              value={data.mentalHealth?.moodScore} 
              unit="/10" 
              icon={Smile} 
              color="yellow"
              description="Above average"
            />
            <MetricCard 
              title="Stress Level" 
              value={data.mentalHealth?.stressLevel} 
              unit="/10" 
              icon={Brain} 
              color="red"
              description="Low stress"
            />
            <MetricCard 
              title="Meditation" 
              value={data.mentalHealth?.meditationMinutes} 
              unit="min" 
              icon={Wind} 
              color="green"
              description="Today"
            />
            <MetricCard 
              title="Sleep Quality" 
              value={data.mentalHealth?.sleepQuality} 
              unit="/10" 
              icon={Moon} 
              color="indigo"
              description="Excellent"
            />
          </div>
        </div>
      )}

      {/* Physical Wellness */}
      {(selectedCategory === 'all' || selectedCategory === 'physical') && (
        <div>
          <h2 className="text-lg font-semibold text-gray-900 mb-4">Physical Wellness</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
            <MetricCard 
              title="Hydration" 
              value={data.physicalWellness?.hydrationLevel} 
              unit="%" 
              icon={Droplets} 
              color="blue"
              description="Daily goal progress"
            />
            <MetricCard 
              title="Nutrition Score" 
              value={data.physicalWellness?.nutritionScore} 
              unit="/10" 
              icon={Leaf} 
              color="green"
              description="Good balance"
            />
            <MetricCard 
              title="Recovery Score" 
              value={data.physicalWellness?.recoveryScore} 
              unit="/10" 
              icon={TrendingUp} 
              color="purple"
              description="Well recovered"
            />
            <MetricCard 
              title="Energy Level" 
              value={data.physicalWellness?.energyLevel} 
              unit="/10" 
              icon={Target} 
              color="orange"
              description="High energy"
            />
          </div>
        </div>
      )}

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Habits Tracking */}
        {(selectedCategory === 'all' || selectedCategory === 'habits') && (
          <div className="bg-white p-6 rounded-lg shadow-md border border-gray-200">
            <h2 className="text-lg font-semibold text-gray-900 mb-4">Habit Tracking</h2>
            <div className="space-y-4">
              {data.habits?.map((habit, index) => (
                <HabitCard key={index} habit={habit} />
              ))}
            </div>
            <button className="w-full mt-4 px-4 py-2 border border-purple-600 text-purple-600 rounded-lg hover:bg-purple-50 transition-colors">
              + Add New Habit
            </button>
          </div>
        )}

        {/* Connected Apps */}
        <div className="bg-white p-6 rounded-lg shadow-md border border-gray-200">
          <h2 className="text-lg font-semibold text-gray-900 mb-4">Connected Apps</h2>
          <div className="space-y-3">
            {data.apps?.map((app, index) => (
              <AppCard key={index} app={app} />
            ))}
          </div>
          <button className="w-full mt-4 px-4 py-2 border border-purple-600 text-purple-600 rounded-lg hover:bg-purple-50 transition-colors">
            + Connect New App
          </button>
        </div>

        {/* Weekly Progress */}
        <div className="bg-white p-6 rounded-lg shadow-md border border-gray-200">
          <h2 className="text-lg font-semibold text-gray-900 mb-4">Weekly Trends</h2>
          <div className="space-y-4">
            <div>
              <h4 className="text-sm font-medium text-gray-700 mb-2">Mood Trend</h4>
              <div className="flex items-end space-x-2">
                {data.weeklyProgress?.map((day, index) => (
                  <div key={index} className="flex-1 text-center">
                    <div 
                      className="bg-yellow-200 rounded-t"
                      style={{ height: `${day.mood * 8}px` }}
                    ></div>
                    <span className="text-xs text-gray-500">{day.day}</span>
                  </div>
                ))}
              </div>
            </div>
            <div>
              <h4 className="text-sm font-medium text-gray-700 mb-2">Energy Levels</h4>
              <div className="flex items-end space-x-2">
                {data.weeklyProgress?.map((day, index) => (
                  <div key={index} className="flex-1 text-center">
                    <div 
                      className="bg-orange-200 rounded-t"
                      style={{ height: `${day.energy * 8}px` }}
                    ></div>
                    <span className="text-xs text-gray-500">{day.day}</span>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Integration Status */}
      <div className="bg-gradient-to-r from-purple-50 to-pink-50 p-6 rounded-lg border border-purple-200">
        <div className="flex items-center space-x-3">
          <div className="p-2 bg-purple-600 rounded-full">
            <Brain className="w-5 h-5 text-white" />
          </div>
          <div>
            <h3 className="font-semibold text-gray-900">Wellness Integration Active</h3>
            <p className="text-gray-600">Data synced from 3 wellness apps. Tracking mental health, sleep, and nutrition.</p>
          </div>
        </div>
      </div>

      {error && (
        <div className="bg-red-50 border border-red-200 rounded-lg p-4">
          <p className="text-red-700">Error loading wellness data: {error}</p>
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

export default Wellness;