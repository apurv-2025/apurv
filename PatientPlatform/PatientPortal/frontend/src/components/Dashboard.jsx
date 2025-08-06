import React, { useState, useEffect } from 'react';
import { Calendar, Clock, User, Phone, Mail, MapPin, Heart, Activity, TrendingUp } from 'lucide-react';
import { useAuth } from '../contexts/AuthContext';
import { useAPI } from '../hooks/useAPI';

const Dashboard = () => {
  const { user } = useAuth();
  const { get } = useAPI();
  const [stats, setStats] = useState({
    appointments: 0,
    medications: 0,
    labResults: 0,
    messages: 0
  });

  useEffect(() => {
    const fetchStats = async () => {
      try {
        const [appointments, medications, labResults, messages] = await Promise.all([
          get('/appointments'),
          get('/medications'),
          get('/lab-results'),
          get('/messages')
        ]);

        setStats({
          appointments: appointments.length,
          medications: medications.length,
          labResults: labResults.length,
          messages: messages.filter(m => !m.is_read).length
        });
      } catch (error) {
        console.error('Error fetching stats:', error);
      }
    };

    fetchStats();
  }, [get]);

  const StatCard = ({ title, value, icon: Icon, color }) => (
    <div className="bg-white rounded-lg shadow p-6">
      <div className="flex items-center justify-between">
        <div>
          <p className="text-sm font-medium text-gray-600">{title}</p>
          <p className="text-2xl font-bold text-gray-900">{value}</p>
        </div>
        <div className={`p-3 rounded-full ${color}`}>
          <Icon className="w-6 h-6 text-white" />
        </div>
      </div>
    </div>
  );

  return (
    <div className="space-y-6">
      {/* Welcome Section */}
      <div className="bg-gradient-to-r from-blue-600 to-blue-700 rounded-lg p-6 text-white">
        <h1 className="text-2xl font-bold mb-2">Welcome back, {user?.first_name || 'User'}!</h1>
        <p className="text-blue-100">Here's what's happening with your health today.</p>
      </div>

      {/* Stats Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <StatCard
          title="Upcoming Appointments"
          value={stats.appointments}
          icon={Calendar}
          color="bg-blue-500"
        />
        <StatCard
          title="Active Medications"
          value={stats.medications}
          icon={Activity}
          color="bg-green-500"
        />
        <StatCard
          title="Lab Results"
          value={stats.labResults}
          icon={TrendingUp}
          color="bg-purple-500"
        />
        <StatCard
          title="Unread Messages"
          value={stats.messages}
          icon={Mail}
          color="bg-orange-500"
        />
      </div>

      {/* Quick Actions */}
      <div className="bg-white rounded-lg shadow p-6">
        <h3 className="text-lg font-semibold text-gray-800 mb-4">Quick Actions</h3>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <button className="flex items-center space-x-3 p-4 border border-gray-200 rounded-lg hover:bg-gray-50 transition-colors">
            <Calendar className="w-5 h-5 text-blue-600" />
            <span className="text-gray-700">Schedule Appointment</span>
          </button>
          <button className="flex items-center space-x-3 p-4 border border-gray-200 rounded-lg hover:bg-gray-50 transition-colors">
            <Phone className="w-5 h-5 text-green-600" />
            <span className="text-gray-700">Contact Doctor</span>
          </button>
          <button className="flex items-center space-x-3 p-4 border border-gray-200 rounded-lg hover:bg-gray-50 transition-colors">
            <Mail className="w-5 h-5 text-purple-600" />
            <span className="text-gray-700">Send Message</span>
          </button>
        </div>
      </div>

      {/* Recent Activity */}
      <div className="bg-white rounded-lg shadow p-6">
        <h3 className="text-lg font-semibold text-gray-800 mb-4">Recent Activity</h3>
        <div className="space-y-4">
          <div className="flex items-center space-x-4 p-3 bg-gray-50 rounded-lg">
            <div className="w-10 h-10 bg-blue-100 rounded-full flex items-center justify-center">
              <Calendar className="w-5 h-5 text-blue-600" />
            </div>
            <div className="flex-1">
              <p className="text-sm font-medium text-gray-800">Appointment scheduled</p>
              <p className="text-xs text-gray-600">Annual checkup with Dr. Johnson</p>
            </div>
            <span className="text-xs text-gray-500">2 hours ago</span>
          </div>
          <div className="flex items-center space-x-4 p-3 bg-gray-50 rounded-lg">
            <div className="w-10 h-10 bg-green-100 rounded-full flex items-center justify-center">
              <Activity className="w-5 h-5 text-green-600" />
            </div>
            <div className="flex-1">
              <p className="text-sm font-medium text-gray-800">Medication refill requested</p>
              <p className="text-xs text-gray-600">Lisinopril 10mg</p>
            </div>
            <span className="text-xs text-gray-500">1 day ago</span>
          </div>
          <div className="flex items-center space-x-4 p-3 bg-gray-50 rounded-lg">
            <div className="w-10 h-10 bg-purple-100 rounded-full flex items-center justify-center">
              <TrendingUp className="w-5 h-5 text-purple-600" />
            </div>
            <div className="flex-1">
              <p className="text-sm font-medium text-gray-800">Lab results available</p>
              <p className="text-xs text-gray-600">Blood work completed</p>
            </div>
            <span className="text-xs text-gray-500">3 days ago</span>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Dashboard; 