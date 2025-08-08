import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { Calendar, Users, Clock, Activity, UserPlus } from 'lucide-react';
import { toast } from 'react-toastify';
import calendarService from '../services/calendarService';
import waitlistService from '../services/waitlistService';

const Dashboard = () => {
  const navigate = useNavigate();

  // Quick action handlers
  const handleScheduleAppointment = () => {
    navigate('/calendar');
    toast.success('Navigating to appointment calendar');
  };

  const handleAddPerson = () => {
    navigate('/patients');
    toast.success('Navigating to patient management');
  };

  const handleManagePractitioners = () => {
    navigate('/practitioners');
    toast.success('Navigating to practitioner management');
  };

  const handleViewCalendar = () => {
    navigate('/calendar');
    toast.success('Navigating to calendar view');
  };

  const handleViewWaitlist = () => {
    navigate('/waitlist');
    toast.success('Navigating to waitlist management');
  };

  const handleSystemSettings = () => {
    toast.info('System settings feature coming soon!');
  };



  // State for dashboard data
  const [dashboardData, setDashboardData] = useState({
    appointments: 0,
    patients: 0,
    waitlist: 0,
    practitioners: 0
  });
  const [recentActivities, setRecentActivities] = useState([]);
  const [loading, setLoading] = useState(true);

  // Get greeting based on time of day
  const getGreeting = () => {
    const hour = new Date().getHours();
    if (hour < 12) return 'Good morning';
    if (hour < 17) return 'Good afternoon';
    return 'Good evening';
  };

  // Fetch dashboard data
  useEffect(() => {
    const fetchDashboardData = async () => {
      try {
        setLoading(true);
        
        // Fetch appointments for today
        const today = new Date().toISOString().split('T')[0];
        const appointments = await calendarService.getAppointments({
          start_date: today,
          end_date: today
        });
        
        // Fetch patients
        const patients = await calendarService.getPatients({ limit: 100 });
        
        // Fetch practitioners
        const practitioners = await calendarService.getPractitioners();
        
        // Fetch waitlist entries
        const waitlistEntries = await waitlistService.getWaitlistEntries({ limit: 100 });
        
        // Generate recent activities from real data
        const activities = [];
        
        // Add recent appointments as activities
        if (appointments.length > 0) {
          const recentAppointments = appointments.slice(0, 3);
          recentAppointments.forEach((appointment, index) => {
            activities.push({
              id: `appointment-${appointment.id}`,
              type: 'appointment',
              message: `Appointment: ${appointment.title || 'Scheduled appointment'}`,
              time: `${index + 1} hour${index > 0 ? 's' : ''} ago`,
            });
          });
        }
        
        // Add recent patients as activities
        if (patients.length > 0) {
          const recentPatients = patients.slice(0, 2);
          recentPatients.forEach((patient, index) => {
            const patientName = patient.name || `${patient.given_names?.join(' ') || ''} ${patient.family_name || ''}`.trim() || 'New patient';
            activities.push({
              id: `patient-${patient.id}`,
              type: 'patient',
              message: `Person registered: ${patientName}`,
              time: `${index + 2} hour${index > 0 ? 's' : ''} ago`,
            });
          });
        }
        
        // Add recent practitioners as activities
        if (practitioners.length > 0) {
          const recentPractitioners = practitioners.slice(0, 1);
          recentPractitioners.forEach((practitioner, index) => {
            activities.push({
              id: `practitioner-${practitioner.id}`,
              type: 'practitioner',
              message: `Practitioner active: ${practitioner.name || 'Dr. Practitioner'}`,
              time: `${index + 3} hour${index > 0 ? 's' : ''} ago`,
            });
          });
        }
        
        // Sort activities by time (most recent first)
        activities.sort((a, b) => {
          const timeA = parseInt(a.time.split(' ')[0]);
          const timeB = parseInt(b.time.split(' ')[0]);
          return timeA - timeB;
        });
        
        setDashboardData({
          appointments: appointments.length,
          patients: patients.length,
          waitlist: waitlistEntries.length,
          practitioners: practitioners.length
        });
        
        setRecentActivities(activities.slice(0, 5)); // Show top 5 activities
        
      } catch (error) {
        console.error('Error fetching dashboard data:', error);
        // Use minimal fallback data
        setDashboardData({
          appointments: 0,
          patients: 0,
          waitlist: 0,
          practitioners: 0
        });
        setRecentActivities([]);
      } finally {
        setLoading(false);
      }
    };

    fetchDashboardData();
  }, []);
  const stats = [
    {
      name: 'Today\'s Appointments',
      value: loading ? '...' : dashboardData.appointments.toString(),
      icon: Calendar,
      color: 'bg-primary-500',
      textColor: 'text-primary-600',
    },
    {
      name: 'Total Persons',
      value: loading ? '...' : dashboardData.patients.toLocaleString(),
      icon: Users,
      color: 'bg-success-500',
      textColor: 'text-success-600',
    },
    {
      name: 'Waitlist Entries',
      value: loading ? '...' : dashboardData.waitlist.toString(),
      icon: Clock,
      color: 'bg-error-500',
      textColor: 'text-error-600',
    },
    {
      name: 'Active Practitioners',
      value: loading ? '...' : dashboardData.practitioners.toString(),
      icon: Activity,
      color: 'bg-warning-500',
      textColor: 'text-warning-600',
    },
  ];



  return (
    <div className="space-y-6">
      {/* Header */}
      <div>
        <h1 className="text-2xl font-bold text-gray-900">{getGreeting()}, Welcome to Dashboard</h1>
        <p className="text-gray-600">Scheduling2.0 - Your unified medical and mental health scheduling system</p>
        {loading && (
          <div className="mt-2 text-sm text-blue-600">
            <div className="inline-flex items-center">
              <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-blue-600 mr-2"></div>
              Loading dashboard data...
            </div>
          </div>
        )}
      </div>



      {/* Stats Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        {stats.map((stat) => {
          const Icon = stat.icon;
          return (
            <div 
              key={stat.name} 
              className="card cursor-pointer hover:shadow-lg transition-shadow"
              onClick={() => {
                if (stat.name === 'Today\'s Appointments') {
                  handleViewCalendar();
                } else if (stat.name === 'Total Persons') {
                  handleAddPerson();
                } else if (stat.name === 'Waitlist Entries') {
                  handleViewWaitlist();
                } else if (stat.name === 'Active Practitioners') {
                  handleManagePractitioners();
                }
              }}
            >
              <div className="card-body">
                <div className="flex items-center">
                  <div className={`p-3 rounded-lg ${stat.color}`}>
                    <Icon className="h-6 w-6 text-white" />
                  </div>
                  <div className="ml-4">
                    <p className="text-sm font-medium text-gray-600">{stat.name}</p>
                    <p className={`text-2xl font-semibold ${stat.textColor}`}>{stat.value}</p>
                  </div>
                </div>
              </div>
            </div>
          );
        })}
      </div>

      {/* Quick Actions and Stats */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Quick Actions */}
        <div className="card lg:col-span-2">
          <div className="card-header">
            <h3 className="text-lg font-medium text-gray-900">Quick Actions</h3>
          </div>
          <div className="card-body">
            <div className="grid grid-cols-2 md:grid-cols-3 gap-4">
              <button 
                onClick={handleScheduleAppointment}
                className="btn-primary hover:bg-blue-700 transition-colors"
              >
                <Calendar className="h-5 w-5 mr-2" />
                Schedule Appointment
              </button>
              <button 
                onClick={handleAddPerson}
                className="btn-secondary hover:bg-gray-700 transition-colors"
              >
                <UserPlus className="h-5 w-5 mr-2" />
                Add Person
              </button>
              <button 
                onClick={handleManagePractitioners}
                className="btn-secondary hover:bg-gray-700 transition-colors"
              >
                <Activity className="h-5 w-5 mr-2" />
                Manage Practitioners
              </button>
              <button 
                onClick={handleViewCalendar}
                className="btn-secondary hover:bg-gray-700 transition-colors"
              >
                <Calendar className="h-5 w-5 mr-2" />
                View Calendar
              </button>
              <button 
                onClick={handleViewWaitlist}
                className="btn-secondary hover:bg-gray-700 transition-colors"
              >
                <Clock className="h-5 w-5 mr-2" />
                View Waitlist
              </button>
            </div>
          </div>
        </div>

        {/* Quick Stats Summary */}
        <div className="card">
          <div className="card-header">
            <h3 className="text-lg font-medium text-gray-900">Today's Summary</h3>
          </div>
          <div className="card-body">
            <div className="space-y-4">
              <div className="flex items-center justify-between">
                <span className="text-sm text-gray-600">Appointments Today</span>
                <span className="text-lg font-semibold text-blue-600">
                  {loading ? '...' : dashboardData.appointments}
                </span>
              </div>
              <div className="flex items-center justify-between">
                <span className="text-sm text-gray-600">Total Persons</span>
                <span className="text-lg font-semibold text-green-600">
                  {loading ? '...' : dashboardData.patients.toLocaleString()}
                </span>
              </div>
              <div className="flex items-center justify-between">
                <span className="text-sm text-gray-600">Waitlist</span>
                <span className="text-lg font-semibold text-red-600">
                  {loading ? '...' : dashboardData.waitlist}
                </span>
              </div>
              <div className="flex items-center justify-between">
                <span className="text-sm text-gray-600">Practitioners</span>
                <span className="text-lg font-semibold text-orange-600">
                  {loading ? '...' : dashboardData.practitioners}
                </span>
              </div>

            </div>
          </div>
        </div>
      </div>

      {/* Recent Activity and System Status */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Recent Activity */}
        <div className="card">
          <div className="card-header">
            <div className="flex items-center justify-between">
              <h3 className="text-lg font-medium text-gray-900">Recent Activity</h3>
              <button 
                onClick={() => {
                  toast.success('Dashboard refreshed!');
                  window.location.reload();
                }}
                className="text-sm text-blue-600 hover:text-blue-800 transition-colors"
              >
                Refresh
              </button>
            </div>
          </div>
          <div className="card-body">
            <div className="space-y-4">
              {recentActivities.map((activity) => (
                <div key={activity.id} className="flex items-start space-x-3">
                  <div className="flex-shrink-0">
                    <div className="w-2 h-2 bg-primary-500 rounded-full mt-2"></div>
                  </div>
                  <div className="flex-1 min-w-0">
                    <p className="text-sm text-gray-900">{activity.message}</p>
                    <p className="text-xs text-gray-500">{activity.time}</p>
                  </div>
                </div>
              ))}

            </div>
          </div>
        </div>

        
      </div>

      {/* System Status */}
      <div className="card">
        <div className="card-header">
          <h3 className="text-lg font-medium text-gray-900">System Status</h3>
        </div>
        <div className="card-body">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div className="flex items-center">
              <div className="status-active mr-3"></div>
              <span className="text-sm text-gray-900">Database</span>
            </div>
            <div className="flex items-center">
              <div className="status-active mr-3"></div>
              <span className="text-sm text-gray-900">Backend API</span>
            </div>
            <div className="flex items-center">
              <div className="status-active mr-3"></div>
              <span className="text-sm text-gray-900">Frontend</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Dashboard; 