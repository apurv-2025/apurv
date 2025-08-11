import React, { useState, useEffect } from 'react';
import { 
  Calendar, Clock, User, MapPin, Video, Phone, Plus, X, CheckCircle, 
  AlertCircle, Search, Filter, Download, Edit, Trash2, ChevronRight, MessageSquare
} from 'lucide-react';
import SurveyModal from './SurveyModal';

const EnhancedAppointments = () => {
  const [activeTab, setActiveTab] = useState('upcoming');
  const [appointments, setAppointments] = useState([]);
  const [filteredAppointments, setFilteredAppointments] = useState([]);
  const [showScheduleModal, setShowScheduleModal] = useState(false);
  const [showSurveyModal, setShowSurveyModal] = useState(false);
  const [selectedAppointment, setSelectedAppointment] = useState(null);
  const [searchTerm, setSearchTerm] = useState('');
  const [filterDoctor, setFilterDoctor] = useState('all');
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Mock comprehensive appointment data
    const mockAppointments = [
      {
        id: 1,
        doctor: 'Dr. Sarah Johnson',
        specialty: 'Cardiology',
        date: '2024-02-15',
        time: '10:00 AM',
        type: 'Follow-up',
        location: 'Main Building, Room 205',
        status: 'confirmed',
        appointmentType: 'in-person',
        reason: 'Blood pressure follow-up',
        duration: 30,
        instructions: 'Please bring your blood pressure log',
        canCancel: true,
        canReschedule: true
      },
      {
        id: 2,
        doctor: 'Dr. Michael Chen',
        specialty: 'Internal Medicine',
        date: '2024-02-20',
        time: '2:30 PM',
        type: 'Annual Physical',
        location: 'Telehealth',
        status: 'confirmed',
        appointmentType: 'telehealth',
        reason: 'Annual wellness exam',
        duration: 45,
        instructions: 'Fasting required - no food 12 hours before',
        canCancel: true,
        canReschedule: true
      },
      {
        id: 3,
        doctor: 'Dr. Emily Davis',
        specialty: 'Dermatology',
        date: '2024-01-20',
        time: '11:00 AM',
        type: 'Consultation',
        location: 'Dermatology Clinic',
        status: 'completed',
        appointmentType: 'in-person',
        reason: 'Skin examination',
        duration: 20,
        notes: 'No issues found. Continue current skincare routine.',
        canCancel: false,
        canReschedule: false,
        surveyCompleted: false
      },
      {
        id: 4,
        doctor: 'Dr. Robert Wilson',
        specialty: 'Orthopedics',
        date: '2024-01-15',
        time: '9:00 AM',
        type: 'Surgery Consultation',
        location: 'Orthopedic Center',
        status: 'cancelled',
        appointmentType: 'in-person',
        reason: 'Knee replacement consultation',
        duration: 60,
        cancellationReason: 'Patient request',
        canCancel: false,
        canReschedule: false
      }
    ];

    setAppointments(mockAppointments);
    setFilteredAppointments(mockAppointments);
    setLoading(false);
  }, []);

  useEffect(() => {
    let filtered = appointments;

    // Filter by tab
    const now = new Date();
    if (activeTab === 'upcoming') {
      filtered = filtered.filter(apt => 
        new Date(apt.date) >= now && apt.status !== 'cancelled'
      );
    } else if (activeTab === 'past') {
      filtered = filtered.filter(apt => 
        new Date(apt.date) < now || apt.status === 'completed'
      );
    } else if (activeTab === 'cancelled') {
      filtered = filtered.filter(apt => apt.status === 'cancelled');
    }

    // Filter by search term
    if (searchTerm) {
      filtered = filtered.filter(apt =>
        apt.doctor.toLowerCase().includes(searchTerm.toLowerCase()) ||
        apt.specialty.toLowerCase().includes(searchTerm.toLowerCase()) ||
        apt.type.toLowerCase().includes(searchTerm.toLowerCase()) ||
        apt.reason.toLowerCase().includes(searchTerm.toLowerCase())
      );
    }

    // Filter by doctor
    if (filterDoctor !== 'all') {
      filtered = filtered.filter(apt => apt.doctor === filterDoctor);
    }

    setFilteredAppointments(filtered);
  }, [appointments, activeTab, searchTerm, filterDoctor]);

  const getStatusColor = (status) => {
    const colors = {
      confirmed: 'bg-green-100 text-green-800 border-green-200',
      completed: 'bg-blue-100 text-blue-800 border-blue-200',
      cancelled: 'bg-red-100 text-red-800 border-red-200',
      pending: 'bg-yellow-100 text-yellow-800 border-yellow-200'
    };
    return colors[status] || colors.pending;
  };

  const getTypeIcon = (type) => {
    return type === 'telehealth' ? Video : User;
  };

  const handleCancelAppointment = async (appointmentId) => {
    // Mock cancellation
    setAppointments(prev => 
      prev.map(apt => 
        apt.id === appointmentId 
          ? { ...apt, status: 'cancelled', cancellationReason: 'Patient request' }
          : apt
      )
    );
  };

  const handleSurveyRequest = (appointment) => {
    setSelectedAppointment(appointment);
    setShowSurveyModal(true);
  };

  const handleSurveyComplete = () => {
    // Mark survey as completed for the appointment
    if (selectedAppointment) {
      setAppointments(prev => 
        prev.map(apt => 
          apt.id === selectedAppointment.id 
            ? { ...apt, surveyCompleted: true }
            : apt
        )
      );
    }
    setSelectedAppointment(null);
  };

  const AppointmentCard = ({ appointment }) => {
    const isPast = new Date(appointment.date) < new Date();
    const isCompleted = appointment.status === 'completed';
    const canTakeSurvey = isCompleted && !appointment.surveyCompleted;

    return (
      <div className="bg-white rounded-lg border border-gray-200 p-6 hover:shadow-md transition-shadow">
        <div className="flex justify-between items-start mb-4">
          <div className="flex items-center space-x-3">
            <div className="w-12 h-12 bg-primary-100 rounded-full flex items-center justify-center">
              <User className="w-6 h-6 text-primary-600" />
            </div>
            <div>
              <h3 className="font-semibold text-gray-900">{appointment.doctor}</h3>
              <p className="text-sm text-gray-500">{appointment.specialty}</p>
            </div>
          </div>
          <div className="flex items-center space-x-2">
            <span className={`px-2 py-1 text-xs font-medium rounded-full border ${getStatusColor(appointment.status)}`}>
              {appointment.status}
            </span>
            {canTakeSurvey && (
              <button
                onClick={() => handleSurveyRequest(appointment)}
                className="flex items-center space-x-1 px-2 py-1 text-xs bg-blue-100 text-blue-700 rounded-full hover:bg-blue-200 transition-colors"
              >
                <MessageSquare className="w-3 h-3" />
                <span>Survey</span>
              </button>
            )}
            {appointment.surveyCompleted && (
              <div className="flex items-center space-x-1 px-2 py-1 text-xs bg-green-100 text-green-700 rounded-full">
                <CheckCircle className="w-3 h-3" />
                <span>Survey Complete</span>
              </div>
            )}
          </div>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4">
          <div className="flex items-center space-x-2">
            <Calendar className="w-4 h-4 text-gray-400" />
            <span className="text-sm text-gray-600">
              {new Date(appointment.date).toLocaleDateString('en-US', { 
                weekday: 'long', 
                year: 'numeric', 
                month: 'long', 
                day: 'numeric' 
              })}
            </span>
          </div>
          <div className="flex items-center space-x-2">
            <Clock className="w-4 h-4 text-gray-400" />
            <span className="text-sm text-gray-600">{appointment.time}</span>
          </div>
          <div className="flex items-center space-x-2">
            <MapPin className="w-4 h-4 text-gray-400" />
            <span className="text-sm text-gray-600">{appointment.location}</span>
          </div>
          <div className="flex items-center space-x-2">
            {React.createElement(getTypeIcon(appointment.appointmentType), { className: "w-4 h-4 text-gray-400" })}
            <span className="text-sm text-gray-600 capitalize">{appointment.appointmentType}</span>
          </div>
        </div>

        <div className="border-t border-gray-100 pt-4">
          <div className="flex justify-between items-center">
            <div>
              <h4 className="font-medium text-gray-900">{appointment.type}</h4>
              <p className="text-sm text-gray-600">{appointment.reason}</p>
            </div>
            <div className="flex items-center space-x-2">
              {appointment.canCancel && (
                <button
                  onClick={() => handleCancelAppointment(appointment.id)}
                  className="px-3 py-1 text-sm text-red-600 hover:bg-red-50 rounded-md transition-colors"
                >
                  Cancel
                </button>
              )}
              {appointment.canReschedule && (
                <button className="px-3 py-1 text-sm text-primary-600 hover:bg-primary-50 rounded-md transition-colors">
                  Reschedule
                </button>
              )}
              <ChevronRight className="w-4 h-4 text-gray-400" />
            </div>
          </div>
        </div>

        {appointment.instructions && (
          <div className="mt-4 p-3 bg-blue-50 rounded-lg">
            <p className="text-sm text-blue-800">
              <strong>Instructions:</strong> {appointment.instructions}
            </p>
          </div>
        )}

        {appointment.notes && (
          <div className="mt-4 p-3 bg-gray-50 rounded-lg">
            <p className="text-sm text-gray-700">
              <strong>Notes:</strong> {appointment.notes}
            </p>
          </div>
        )}

        {appointment.cancellationReason && (
          <div className="mt-4 p-3 bg-red-50 rounded-lg">
            <p className="text-sm text-red-700">
              <strong>Cancellation Reason:</strong> {appointment.cancellationReason}
            </p>
          </div>
        )}
      </div>
    );
  };

  const ScheduleModal = () => {
    const [formData, setFormData] = useState({
      doctor: '',
      specialty: '',
      date: '',
      time: '',
      type: '',
      reason: '',
      appointmentType: 'in-person'
    });

    const handleSubmit = (e) => {
      e.preventDefault();
      // Mock scheduling
      const newAppointment = {
        id: Date.now(),
        ...formData,
        status: 'confirmed',
        location: formData.appointmentType === 'telehealth' ? 'Telehealth' : 'Main Building',
        duration: 30,
        canCancel: true,
        canReschedule: true
      };
      setAppointments(prev => [...prev, newAppointment]);
      setShowScheduleModal(false);
    };

    return (
      <div className="fixed inset-0 z-50 overflow-y-auto">
        <div className="flex items-center justify-center min-h-screen pt-4 px-4 pb-20 text-center sm:block sm:p-0">
          <div className="fixed inset-0 bg-gray-500 bg-opacity-75 transition-opacity"></div>
          <div className="inline-block align-bottom bg-white rounded-lg text-left overflow-hidden shadow-xl transform transition-all sm:my-8 sm:align-middle sm:max-w-lg sm:w-full">
            <div className="bg-white px-4 pt-5 pb-4 sm:p-6 sm:pb-4">
              <div className="flex items-center justify-between mb-4">
                <h3 className="text-lg font-medium text-gray-900">Schedule Appointment</h3>
                <button
                  onClick={() => setShowScheduleModal(false)}
                  className="text-gray-400 hover:text-gray-600"
                >
                  <X className="w-6 h-6" />
                </button>
              </div>
              <form onSubmit={handleSubmit} className="space-y-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700">Doctor</label>
                  <input
                    type="text"
                    value={formData.doctor}
                    onChange={(e) => setFormData({...formData, doctor: e.target.value})}
                    className="mt-1 block w-full border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-primary-500 focus:border-primary-500"
                    required
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700">Specialty</label>
                  <input
                    type="text"
                    value={formData.specialty}
                    onChange={(e) => setFormData({...formData, specialty: e.target.value})}
                    className="mt-1 block w-full border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-primary-500 focus:border-primary-500"
                    required
                  />
                </div>
                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <label className="block text-sm font-medium text-gray-700">Date</label>
                    <input
                      type="date"
                      value={formData.date}
                      onChange={(e) => setFormData({...formData, date: e.target.value})}
                      className="mt-1 block w-full border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-primary-500 focus:border-primary-500"
                      required
                    />
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-gray-700">Time</label>
                    <input
                      type="time"
                      value={formData.time}
                      onChange={(e) => setFormData({...formData, time: e.target.value})}
                      className="mt-1 block w-full border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-primary-500 focus:border-primary-500"
                      required
                    />
                  </div>
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700">Appointment Type</label>
                  <select
                    value={formData.appointmentType}
                    onChange={(e) => setFormData({...formData, appointmentType: e.target.value})}
                    className="mt-1 block w-full border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-primary-500 focus:border-primary-500"
                  >
                    <option value="in-person">In-Person</option>
                    <option value="telehealth">Telehealth</option>
                  </select>
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700">Type</label>
                  <input
                    type="text"
                    value={formData.type}
                    onChange={(e) => setFormData({...formData, type: e.target.value})}
                    placeholder="e.g., Annual Physical, Follow-up"
                    className="mt-1 block w-full border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-primary-500 focus:border-primary-500"
                    required
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700">Reason</label>
                  <textarea
                    value={formData.reason}
                    onChange={(e) => setFormData({...formData, reason: e.target.value})}
                    rows={3}
                    className="mt-1 block w-full border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-primary-500 focus:border-primary-500"
                    required
                  />
                </div>
                <div className="flex justify-end space-x-3 pt-4">
                  <button
                    type="button"
                    onClick={() => setShowScheduleModal(false)}
                    className="px-4 py-2 text-sm font-medium text-gray-700 bg-gray-100 rounded-md hover:bg-gray-200 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-gray-500"
                  >
                    Cancel
                  </button>
                  <button
                    type="submit"
                    className="px-4 py-2 text-sm font-medium text-white bg-primary-600 rounded-md hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500"
                  >
                    Schedule
                  </button>
                </div>
              </form>
            </div>
          </div>
        </div>
      </div>
    );
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary-600"></div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">Appointments</h1>
          <p className="text-gray-600">Manage your healthcare appointments</p>
        </div>
        <button
          onClick={() => setShowScheduleModal(true)}
          className="flex items-center space-x-2 px-4 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700 transition-colors"
        >
          <Plus className="w-4 h-4" />
          <span>Schedule Appointment</span>
        </button>
      </div>

      {/* Tabs */}
      <div className="border-b border-gray-200">
        <nav className="-mb-px flex space-x-8">
          {[
            { id: 'upcoming', label: 'Upcoming', count: appointments.filter(apt => new Date(apt.date) >= new Date() && apt.status !== 'cancelled').length },
            { id: 'past', label: 'Past', count: appointments.filter(apt => new Date(apt.date) < new Date() || apt.status === 'completed').length },
            { id: 'cancelled', label: 'Cancelled', count: appointments.filter(apt => apt.status === 'cancelled').length }
          ].map((tab) => (
            <button
              key={tab.id}
              onClick={() => setActiveTab(tab.id)}
              className={`py-2 px-1 border-b-2 font-medium text-sm ${
                activeTab === tab.id
                  ? 'border-primary-500 text-primary-600'
                  : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
              }`}
            >
              {tab.label}
              <span className="ml-2 bg-gray-100 text-gray-900 py-0.5 px-2.5 rounded-full text-xs">
                {tab.count}
              </span>
            </button>
          ))}
        </nav>
      </div>

      {/* Filters */}
      <div className="flex flex-col sm:flex-row gap-4">
        <div className="flex-1">
          <div className="relative">
            <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-4 h-4" />
            <input
              type="text"
              placeholder="Search appointments..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
            />
          </div>
        </div>
        <div className="sm:w-48">
          <select
            value={filterDoctor}
            onChange={(e) => setFilterDoctor(e.target.value)}
            className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
          >
            <option value="all">All Doctors</option>
            {Array.from(new Set(appointments.map(apt => apt.doctor))).map(doctor => (
              <option key={doctor} value={doctor}>{doctor}</option>
            ))}
          </select>
        </div>
      </div>

      {/* Appointments List */}
      <div className="space-y-4">
        {filteredAppointments.length === 0 ? (
          <div className="text-center py-12">
            <Calendar className="w-12 h-12 text-gray-400 mx-auto mb-4" />
            <h3 className="text-lg font-medium text-gray-900 mb-2">No appointments found</h3>
            <p className="text-gray-600">Try adjusting your search or filters</p>
          </div>
        ) : (
          filteredAppointments.map(appointment => (
            <AppointmentCard key={appointment.id} appointment={appointment} />
          ))
        )}
      </div>

      {/* Modals */}
      {showScheduleModal && <ScheduleModal />}
      
      <SurveyModal
        isOpen={showSurveyModal}
        onClose={() => setShowSurveyModal(false)}
        surveyType="visit"
        appointmentId={selectedAppointment?.id}
        onComplete={handleSurveyComplete}
      />
    </div>
  );
};

export default EnhancedAppointments;