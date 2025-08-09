import React, { useState, useEffect } from 'react';
import { 
  Calendar, Clock, User, Phone, Mail, MapPin, Heart, Activity, TrendingUp, 
  MessageCircle, FileText, Pill, CreditCard, AlertCircle, CheckCircle, 
  ArrowRight, Download, Bell, Video, Stethoscope, ClipboardList
} from 'lucide-react';
import { useAuth } from '../contexts/AuthContext';
import { useAPI } from '../hooks/useAPI';

const EnhancedDashboard = () => {
  const { user } = useAuth();
  const { get } = useAPI();
  const [stats, setStats] = useState({
    upcomingAppointments: 0,
    unreadMessages: 0,
    newResults: 0,
    prescriptionsDue: 0,
    outstandingBills: 0
  });

  const [dashboardData, setDashboardData] = useState({
    upcomingAppointments: [],
    recentMessages: [],
    recentResults: [],
    currentPrescriptions: [],
    vitals: [],
    alerts: []
  });

  useEffect(() => {
    const fetchDashboardData = async () => {
      try {
        // Fetch all dashboard data
        const [appointments, messages, labResults, medications] = await Promise.all([
          get('/appointments'),
          get('/messages'),
          get('/lab-results'),
          get('/medications')
        ]);

        // Mock data for enhanced features (would come from real APIs)
        const mockData = {
          upcomingAppointments: [
            { 
              id: 1, 
              doctor: 'Dr. Sarah Johnson', 
              specialty: 'Cardiology',
              date: '2024-02-15', 
              time: '10:00 AM',
              type: 'Follow-up',
              status: 'confirmed'
            },
            { 
              id: 2, 
              doctor: 'Dr. Michael Chen', 
              specialty: 'Internal Medicine',
              date: '2024-02-20', 
              time: '2:30 PM',
              type: 'Annual Physical',
              status: 'confirmed'
            }
          ],
          recentMessages: [
            { 
              id: 1, 
              from: 'Dr. Johnson', 
              subject: 'Blood pressure medication adjustment',
              time: '2 hours ago',
              isRead: false,
              isUrgent: false
            },
            { 
              id: 2, 
              from: 'Clinic Staff', 
              subject: 'Appointment reminder for tomorrow',
              time: '4 hours ago',
              isRead: false,
              isUrgent: true
            }
          ],
          recentResults: [
            {
              id: 1,
              type: 'Lab Results',
              name: 'Complete Blood Count',
              date: '2024-02-10',
              status: 'Normal',
              doctor: 'Dr. Johnson',
              isNew: true
            }
          ],
          currentPrescriptions: [
            {
              id: 1,
              medication: 'Lisinopril 10mg',
              doctor: 'Dr. Johnson',
              refillsLeft: 2,
              nextRefillDate: '2024-02-25',
              status: 'active'
            },
            {
              id: 2,
              medication: 'Metformin 500mg',
              doctor: 'Dr. Chen',
              refillsLeft: 0,
              nextRefillDate: '2024-02-18',
              status: 'refill_needed'
            }
          ],
          vitals: [
            { label: 'Blood Pressure', value: '120/80', status: 'normal', color: 'text-green-600', trend: 'stable' },
            { label: 'Heart Rate', value: '72 bpm', status: 'normal', color: 'text-green-600', trend: 'stable' },
            { label: 'Weight', value: '165 lbs', status: 'stable', color: 'text-blue-600', trend: 'down' },
            { label: 'BMI', value: '24.2', status: 'normal', color: 'text-green-600', trend: 'stable' }
          ],
          alerts: [
            { type: 'prescription', message: 'Metformin refill needed by Feb 18', urgent: true },
            { type: 'appointment', message: 'Annual physical due', urgent: false },
            { type: 'billing', message: 'Payment due for recent visit', urgent: true }
          ]
        };

        setDashboardData(mockData);
        setStats({
          upcomingAppointments: mockData.upcomingAppointments.length,
          unreadMessages: mockData.recentMessages.filter(m => !m.isRead).length,
          newResults: mockData.recentResults.filter(r => r.isNew).length,
          prescriptionsDue: mockData.currentPrescriptions.filter(p => p.status === 'refill_needed').length,
          outstandingBills: 1
        });

      } catch (error) {
        console.error('Error fetching dashboard data:', error);
      }
    };

    fetchDashboardData();
  }, [get]);

  const StatCard = ({ title, value, icon: Icon, color, onClick }) => (
    <div 
      className={`bg-white rounded-lg shadow p-6 ${onClick ? 'cursor-pointer hover:shadow-md transition-shadow' : ''}`}
      onClick={onClick}
    >
      <div className="flex items-center justify-between">
        <div>
          <p className="text-sm font-medium text-gray-600">{title}</p>
          <p className="text-2xl font-bold text-gray-900">{value}</p>
        </div>
        <div className={`p-3 rounded-full ${color}`}>
          <Icon className="w-6 h-6 text-white" />
        </div>
      </div>
      {onClick && (
        <div className="mt-2 flex items-center text-sm text-blue-600">
          <span>View details</span>
          <ArrowRight className="w-4 h-4 ml-1" />
        </div>
      )}
    </div>
  );

  const AppointmentCard = ({ appointment }) => (
    <div className="bg-white p-4 rounded-lg border border-gray-200 hover:shadow-md transition-shadow">
      <div className="flex items-start justify-between">
        <div className="flex-1">
          <h4 className="font-medium text-gray-900">{appointment.doctor}</h4>
          <p className="text-sm text-gray-600">{appointment.specialty}</p>
          <div className="flex items-center mt-2 text-sm text-gray-500">
            <Calendar className="w-4 h-4 mr-1" />
            <span>{appointment.date} at {appointment.time}</span>
          </div>
          <span className="inline-block mt-2 px-2 py-1 bg-blue-100 text-blue-800 text-xs rounded-full">
            {appointment.type}
          </span>
        </div>
        <div className="flex flex-col space-y-2">
          <button className="text-blue-600 hover:text-blue-800 text-sm">Join</button>
          <button className="text-gray-600 hover:text-gray-800 text-sm">Details</button>
        </div>
      </div>
    </div>
  );

  const MessageCard = ({ message }) => (
    <div className={`bg-white p-4 rounded-lg border border-gray-200 hover:shadow-md transition-shadow ${!message.isRead ? 'border-l-4 border-l-blue-500' : ''}`}>
      <div className="flex items-start justify-between">
        <div className="flex-1">
          <div className="flex items-center space-x-2">
            <h4 className="font-medium text-gray-900">{message.from}</h4>
            {message.isUrgent && <AlertCircle className="w-4 h-4 text-red-500" />}
            {!message.isRead && <div className="w-2 h-2 bg-blue-500 rounded-full"></div>}
          </div>
          <p className="text-sm text-gray-600 mt-1">{message.subject}</p>
          <p className="text-xs text-gray-500 mt-1">{message.time}</p>
        </div>
        <MessageCircle className="w-5 h-5 text-gray-400" />
      </div>
    </div>
  );

  const ResultCard = ({ result }) => (
    <div className="bg-white p-4 rounded-lg border border-gray-200 hover:shadow-md transition-shadow">
      <div className="flex items-start justify-between">
        <div className="flex-1">
          <div className="flex items-center space-x-2">
            <h4 className="font-medium text-gray-900">{result.name}</h4>
            {result.isNew && <span className="bg-green-100 text-green-800 text-xs px-2 py-1 rounded-full">New</span>}
          </div>
          <p className="text-sm text-gray-600">{result.type} • Dr. {result.doctor}</p>
          <p className="text-xs text-gray-500 mt-1">{result.date}</p>
          <div className="flex items-center mt-2">
            <span className={`text-sm px-2 py-1 rounded-full ${
              result.status === 'Normal' ? 'bg-green-100 text-green-800' : 'bg-yellow-100 text-yellow-800'
            }`}>
              {result.status}
            </span>
          </div>
        </div>
        <div className="flex flex-col space-y-2">
          <button className="text-blue-600 hover:text-blue-800 text-sm flex items-center">
            <Download className="w-4 h-4 mr-1" />
            PDF
          </button>
        </div>
      </div>
    </div>
  );

  const PrescriptionCard = ({ prescription }) => (
    <div className="bg-white p-4 rounded-lg border border-gray-200 hover:shadow-md transition-shadow">
      <div className="flex items-start justify-between">
        <div className="flex-1">
          <h4 className="font-medium text-gray-900">{prescription.medication}</h4>
          <p className="text-sm text-gray-600">Prescribed by {prescription.doctor}</p>
          <p className="text-xs text-gray-500 mt-1">Next refill: {prescription.nextRefillDate}</p>
          <div className="flex items-center mt-2">
            <span className={`text-sm px-2 py-1 rounded-full ${
              prescription.status === 'active' ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'
            }`}>
              {prescription.refillsLeft} refills left
            </span>
          </div>
        </div>
        <div className="flex flex-col space-y-2">
          {prescription.status === 'refill_needed' && (
            <button className="text-blue-600 hover:text-blue-800 text-sm">Request Refill</button>
          )}
        </div>
      </div>
    </div>
  );

  const AlertBanner = ({ alerts }) => (
    alerts.length > 0 && (
      <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-4 mb-6">
        <div className="flex items-start space-x-3">
          <Bell className="w-5 h-5 text-yellow-600 mt-0.5" />
          <div className="flex-1">
            <h3 className="font-medium text-yellow-800">Important Notifications</h3>
            <div className="mt-2 space-y-1">
              {alerts.slice(0, 2).map((alert, index) => (
                <div key={index} className="flex items-center space-x-2">
                  {alert.urgent && <AlertCircle className="w-4 h-4 text-red-500" />}
                  <span className={`text-sm ${alert.urgent ? 'text-red-700' : 'text-yellow-700'}`}>
                    {alert.message}
                  </span>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>
    )
  );

  return (
    <div className="space-y-6">
      {/* Welcome Header */}
      <div className="bg-gradient-to-r from-blue-600 to-blue-800 rounded-lg p-6 text-white">
        <h1 className="text-2xl font-bold">Welcome back, {user?.first_name || 'Patient'}!</h1>
        <p className="mt-2 opacity-90">Here's your health summary for today</p>
      </div>

      {/* Alert Banner */}
      <AlertBanner alerts={dashboardData.alerts} />

      {/* Stats Overview */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-5 gap-6">
        <StatCard
          title="Upcoming Appointments"
          value={stats.upcomingAppointments}
          icon={Calendar}
          color="bg-blue-500"
        />
        <StatCard
          title="Unread Messages"
          value={stats.unreadMessages}
          icon={MessageCircle}
          color="bg-green-500"
        />
        <StatCard
          title="New Results"
          value={stats.newResults}
          icon={FileText}
          color="bg-purple-500"
        />
        <StatCard
          title="Refills Due"
          value={stats.prescriptionsDue}
          icon={Pill}
          color="bg-orange-500"
        />
        <StatCard
          title="Outstanding Bills"
          value={stats.outstandingBills}
          icon={CreditCard}
          color="bg-red-500"
        />
      </div>

      {/* Main Content Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Upcoming Appointments */}
        <div className="bg-white rounded-lg shadow p-6">
          <div className="flex items-center justify-between mb-4">
            <h2 className="text-lg font-semibold text-gray-900">Upcoming Appointments</h2>
            <button className="text-blue-600 hover:text-blue-800 text-sm">View All</button>
          </div>
          <div className="space-y-4">
            {dashboardData.upcomingAppointments.slice(0, 2).map(appointment => (
              <AppointmentCard key={appointment.id} appointment={appointment} />
            ))}
            {dashboardData.upcomingAppointments.length === 0 && (
              <p className="text-gray-500 text-center py-4">No upcoming appointments</p>
            )}
          </div>
          <button className="w-full mt-4 px-4 py-2 border border-blue-600 text-blue-600 rounded-lg hover:bg-blue-50 transition-colors">
            Schedule New Appointment
          </button>
        </div>

        {/* Recent Messages */}
        <div className="bg-white rounded-lg shadow p-6">
          <div className="flex items-center justify-between mb-4">
            <h2 className="text-lg font-semibold text-gray-900">Recent Messages</h2>
            <button className="text-blue-600 hover:text-blue-800 text-sm">View All</button>
          </div>
          <div className="space-y-4">
            {dashboardData.recentMessages.slice(0, 3).map(message => (
              <MessageCard key={message.id} message={message} />
            ))}
            {dashboardData.recentMessages.length === 0 && (
              <p className="text-gray-500 text-center py-4">No recent messages</p>
            )}
          </div>
        </div>

        {/* Recent Results */}
        <div className="bg-white rounded-lg shadow p-6">
          <div className="flex items-center justify-between mb-4">
            <h2 className="text-lg font-semibold text-gray-900">Recent Results</h2>
            <button className="text-blue-600 hover:text-blue-800 text-sm">View All</button>
          </div>
          <div className="space-y-4">
            {dashboardData.recentResults.slice(0, 2).map(result => (
              <ResultCard key={result.id} result={result} />
            ))}
            {dashboardData.recentResults.length === 0 && (
              <p className="text-gray-500 text-center py-4">No recent results</p>
            )}
          </div>
        </div>

        {/* Current Prescriptions */}
        <div className="bg-white rounded-lg shadow p-6">
          <div className="flex items-center justify-between mb-4">
            <h2 className="text-lg font-semibold text-gray-900">Current Prescriptions</h2>
            <button className="text-blue-600 hover:text-blue-800 text-sm">View All</button>
          </div>
          <div className="space-y-4">
            {dashboardData.currentPrescriptions.slice(0, 2).map(prescription => (
              <PrescriptionCard key={prescription.id} prescription={prescription} />
            ))}
            {dashboardData.currentPrescriptions.length === 0 && (
              <p className="text-gray-500 text-center py-4">No current prescriptions</p>
            )}
          </div>
        </div>
      </div>

      {/* Health Vitals */}
      <div className="bg-white rounded-lg shadow p-6">
        <h2 className="text-lg font-semibold text-gray-900 mb-4">Recent Vitals</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
          {dashboardData.vitals.map((vital, index) => (
            <div key={index} className="bg-gray-50 p-4 rounded-lg">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm text-gray-600">{vital.label}</p>
                  <p className={`text-lg font-semibold ${vital.color}`}>{vital.value}</p>
                  <p className="text-xs text-gray-500">{vital.status}</p>
                </div>
                <TrendingUp className={`w-5 h-5 ${vital.color}`} />
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Quick Actions */}
      <div className="bg-white rounded-lg shadow p-6">
        <h2 className="text-lg font-semibold text-gray-900 mb-4">Quick Actions</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
          <button className="flex items-center space-x-3 p-4 border border-gray-200 rounded-lg hover:bg-gray-50 transition-colors">
            <Video className="w-5 h-5 text-blue-600" />
            <span className="text-sm font-medium">Join Telehealth</span>
          </button>
          <button className="flex items-center space-x-3 p-4 border border-gray-200 rounded-lg hover:bg-gray-50 transition-colors">
            <ClipboardList className="w-5 h-5 text-green-600" />
            <span className="text-sm font-medium">Complete Forms</span>
          </button>
          <button className="flex items-center space-x-3 p-4 border border-gray-200 rounded-lg hover:bg-gray-50 transition-colors">
            <Download className="w-5 h-5 text-purple-600" />
            <span className="text-sm font-medium">Download Records</span>
          </button>
          <button className="flex items-center space-x-3 p-4 border border-gray-200 rounded-lg hover:bg-gray-50 transition-colors">
            <CreditCard className="w-5 h-5 text-orange-600" />
            <span className="text-sm font-medium">Pay Bills</span>
          </button>
        </div>
      </div>
    </div>
  );
};

export default EnhancedDashboard;