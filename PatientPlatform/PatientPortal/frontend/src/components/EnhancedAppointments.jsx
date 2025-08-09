import React, { useState, useEffect } from 'react';
import { 
  Calendar, Clock, User, MapPin, Video, Phone, Plus, X, CheckCircle, 
  AlertCircle, Search, Filter, Download, Edit, Trash2, ChevronRight
} from 'lucide-react';


const EnhancedAppointments = () => {
  const [activeTab, setActiveTab] = useState('upcoming');
  const [appointments, setAppointments] = useState([]);
  const [filteredAppointments, setFilteredAppointments] = useState([]);
  const [showScheduleModal, setShowScheduleModal] = useState(false);
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
        canReschedule: false
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
    switch (status) {
      case 'confirmed': return 'bg-green-100 text-green-800';
      case 'pending': return 'bg-yellow-100 text-yellow-800';
      case 'cancelled': return 'bg-red-100 text-red-800';
      case 'completed': return 'bg-blue-100 text-blue-800';
      default: return 'bg-gray-100 text-gray-800';
    }
  };

  const getTypeIcon = (type) => {
    switch (type) {
      case 'telehealth': return Video;
      case 'phone': return Phone;
      default: return MapPin;
    }
  };

  const handleCancelAppointment = async (appointmentId) => {
    if (window.confirm('Are you sure you want to cancel this appointment?')) {
      try {
        // API call would go here
        setAppointments(prev => 
          prev.map(apt => 
            apt.id === appointmentId 
              ? { ...apt, status: 'cancelled', cancellationReason: 'Patient request' }
              : apt
          )
        );
      } catch (error) {
        console.error('Error cancelling appointment:', error);
      }
    }
  };

  const AppointmentCard = ({ appointment }) => {
    const StatusIcon = getTypeIcon(appointment.appointmentType);
    
    return (
      <div className="bg-white border border-gray-200 rounded-lg p-6 hover:shadow-md transition-shadow">
        <div className="flex items-start justify-between">
          <div className="flex-1">
            <div className="flex items-center space-x-3 mb-2">
              <h3 className="text-lg font-semibold text-gray-900">{appointment.doctor}</h3>
              <span className={`px-2 py-1 rounded-full text-xs font-medium ${getStatusColor(appointment.status)}`}>
                {appointment.status}
              </span>
            </div>
            
            <p className="text-sm text-gray-600 mb-2">{appointment.specialty}</p>
            
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4">
              <div className="flex items-center space-x-2 text-sm text-gray-600">
                <Calendar className="w-4 h-4" />
                <span>{appointment.date} at {appointment.time}</span>
              </div>
              <div className="flex items-center space-x-2 text-sm text-gray-600">
                <StatusIcon className="w-4 h-4" />
                <span>{appointment.location}</span>
              </div>
              <div className="flex items-center space-x-2 text-sm text-gray-600">
                <Clock className="w-4 h-4" />
                <span>{appointment.duration} minutes</span>
              </div>
              <div className="flex items-center space-x-2 text-sm text-gray-600">
                <User className="w-4 h-4" />
                <span>{appointment.type}</span>
              </div>
            </div>

            <div className="mb-4">
              <p className="text-sm font-medium text-gray-700">Reason:</p>
              <p className="text-sm text-gray-600">{appointment.reason}</p>
            </div>

            {appointment.instructions && (
              <div className="mb-4 p-3 bg-blue-50 border border-blue-200 rounded-lg">
                <p className="text-sm font-medium text-blue-800">Instructions:</p>
                <p className="text-sm text-blue-700">{appointment.instructions}</p>
              </div>
            )}

            {appointment.notes && (
              <div className="mb-4 p-3 bg-gray-50 border border-gray-200 rounded-lg">
                <p className="text-sm font-medium text-gray-800">Notes:</p>
                <p className="text-sm text-gray-600">{appointment.notes}</p>
              </div>
            )}

            {appointment.cancellationReason && (
              <div className="mb-4 p-3 bg-red-50 border border-red-200 rounded-lg">
                <p className="text-sm font-medium text-red-800">Cancellation Reason:</p>
                <p className="text-sm text-red-700">{appointment.cancellationReason}</p>
              </div>
            )}
          </div>

          <div className="flex flex-col space-y-2 ml-4">
            {appointment.appointmentType === 'telehealth' && appointment.status === 'confirmed' && (
              <button className="px-3 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors text-sm">
                Join Call
              </button>
            )}
            
            {appointment.canReschedule && (
              <button className="px-3 py-2 border border-gray-300 text-gray-700 rounded-lg hover:bg-gray-50 transition-colors text-sm">
                Reschedule
              </button>
            )}
            
            {appointment.canCancel && (
              <button 
                onClick={() => handleCancelAppointment(appointment.id)}
                className="px-3 py-2 border border-red-300 text-red-700 rounded-lg hover:bg-red-50 transition-colors text-sm"
              >
                Cancel
              </button>
            )}

            {appointment.status === 'completed' && (
              <button className="px-3 py-2 border border-gray-300 text-gray-700 rounded-lg hover:bg-gray-50 transition-colors text-sm flex items-center">
                <Download className="w-4 h-4 mr-1" />
                Summary
              </button>
            )}
          </div>
        </div>
      </div>
    );
  };

  const ScheduleModal = () => {
    const [formData, setFormData] = useState({
      doctor: '',
      specialty: '',
      appointmentType: 'in-person',
      preferredDate: '',
      preferredTime: '',
      reason: '',
      urgency: 'routine'
    });

    const doctors = [
      { name: 'Dr. Sarah Johnson', specialty: 'Cardiology' },
      { name: 'Dr. Michael Chen', specialty: 'Internal Medicine' },
      { name: 'Dr. Emily Davis', specialty: 'Dermatology' },
      { name: 'Dr. Robert Wilson', specialty: 'Orthopedics' }
    ];

    const handleSubmit = (e) => {
      e.preventDefault();
      // API call would go here
      console.log('Scheduling appointment:', formData);
      setShowScheduleModal(false);
    };

    if (!showScheduleModal) return null;

    return (
      <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
        <div className="bg-white rounded-lg max-w-2xl w-full max-h-[90vh] overflow-y-auto">
          <div className="p-6 border-b border-gray-200">
            <div className="flex items-center justify-between">
              <h2 className="text-xl font-semibold text-gray-900">Schedule New Appointment</h2>
              <button 
                onClick={() => setShowScheduleModal(false)}
                className="text-gray-400 hover:text-gray-600"
              >
                <X className="w-6 h-6" />
              </button>
            </div>
          </div>

          <form onSubmit={handleSubmit} className="p-6 space-y-6">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Doctor
                </label>
                <select
                  value={formData.doctor}
                  onChange={(e) => setFormData({...formData, doctor: e.target.value})}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  required
                >
                  <option value="">Select a doctor</option>
                  {doctors.map((doctor, index) => (
                    <option key={index} value={doctor.name}>{doctor.name} - {doctor.specialty}</option>
                  ))}
                </select>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Appointment Type
                </label>
                <select
                  value={formData.appointmentType}
                  onChange={(e) => setFormData({...formData, appointmentType: e.target.value})}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                >
                  <option value="in-person">In-Person</option>
                  <option value="telehealth">Telehealth</option>
                  <option value="phone">Phone Call</option>
                </select>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Preferred Date
                </label>
                <input
                  type="date"
                  value={formData.preferredDate}
                  onChange={(e) => setFormData({...formData, preferredDate: e.target.value})}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  required
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Preferred Time
                </label>
                <select
                  value={formData.preferredTime}
                  onChange={(e) => setFormData({...formData, preferredTime: e.target.value})}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  required
                >
                  <option value="">Select time</option>
                  <option value="8:00 AM">8:00 AM</option>
                  <option value="9:00 AM">9:00 AM</option>
                  <option value="10:00 AM">10:00 AM</option>
                  <option value="11:00 AM">11:00 AM</option>
                  <option value="1:00 PM">1:00 PM</option>
                  <option value="2:00 PM">2:00 PM</option>
                  <option value="3:00 PM">3:00 PM</option>
                  <option value="4:00 PM">4:00 PM</option>
                </select>
              </div>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Reason for Visit
              </label>
              <textarea
                value={formData.reason}
                onChange={(e) => setFormData({...formData, reason: e.target.value})}
                rows="3"
                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                placeholder="Please describe the reason for your visit..."
                required
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Urgency
              </label>
              <select
                value={formData.urgency}
                onChange={(e) => setFormData({...formData, urgency: e.target.value})}
                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              >
                <option value="routine">Routine</option>
                <option value="urgent">Urgent (within 1 week)</option>
                <option value="asap">ASAP (within 2 days)</option>
              </select>
            </div>

            <div className="flex space-x-4 pt-6">
              <button
                type="button"
                onClick={() => setShowScheduleModal(false)}
                className="flex-1 px-4 py-2 border border-gray-300 text-gray-700 rounded-lg hover:bg-gray-50 transition-colors"
              >
                Cancel
              </button>
              <button
                type="submit"
                className="flex-1 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
              >
                Schedule Appointment
              </button>
            </div>
          </form>
        </div>
      </div>
    );
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
      </div>
    );
  }

  const uniqueDoctors = [...new Set(appointments.map(apt => apt.doctor))];

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">Appointments</h1>
          <p className="text-gray-600">Manage your healthcare appointments</p>
        </div>
        <button
          onClick={() => setShowScheduleModal(true)}
          className="mt-4 sm:mt-0 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors flex items-center"
        >
          <Plus className="w-5 h-5 mr-2" />
          Schedule Appointment
        </button>
      </div>

      {/* Filters and Search */}
      <div className="bg-white rounded-lg shadow p-6">
        <div className="flex flex-col lg:flex-row lg:items-center lg:justify-between space-y-4 lg:space-y-0">
          <div className="flex space-x-4">
            <div className="relative">
              <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-5 h-5" />
              <input
                type="text"
                placeholder="Search appointments..."
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                className="pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              />
            </div>
            <select
              value={filterDoctor}
              onChange={(e) => setFilterDoctor(e.target.value)}
              className="px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            >
              <option value="all">All Doctors</option>
              {uniqueDoctors.map((doctor, index) => (
                <option key={index} value={doctor}>{doctor}</option>
              ))}
            </select>
          </div>
        </div>
      </div>

      {/* Tabs */}
      <div className="bg-white rounded-lg shadow">
        <div className="border-b border-gray-200">
          <nav className="flex space-x-8 px-6">
            {[
              { id: 'upcoming', label: 'Upcoming', count: appointments.filter(a => new Date(a.date) >= new Date() && a.status !== 'cancelled').length },
              { id: 'past', label: 'Past', count: appointments.filter(a => new Date(a.date) < new Date() || a.status === 'completed').length },
              { id: 'cancelled', label: 'Cancelled', count: appointments.filter(a => a.status === 'cancelled').length }
            ].map(tab => (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id)}
                className={`py-4 px-1 border-b-2 font-medium text-sm ${
                  activeTab === tab.id
                    ? 'border-blue-500 text-blue-600'
                    : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                }`}
              >
                {tab.label} ({tab.count})
              </button>
            ))}
          </nav>
        </div>

        {/* Appointments List */}
        <div className="p-6">
          {filteredAppointments.length === 0 ? (
            <div className="text-center py-12">
              <Calendar className="mx-auto h-12 w-12 text-gray-400" />
              <h3 className="mt-2 text-sm font-medium text-gray-900">No appointments found</h3>
              <p className="mt-1 text-sm text-gray-500">
                {activeTab === 'upcoming' ? 'Schedule your first appointment to get started.' : 'No appointments in this category.'}
              </p>
              {activeTab === 'upcoming' && (
                <div className="mt-6">
                  <button
                    onClick={() => setShowScheduleModal(true)}
                    className="inline-flex items-center px-4 py-2 border border-transparent shadow-sm text-sm font-medium rounded-md text-white bg-blue-600 hover:bg-blue-700"
                  >
                    <Plus className="w-5 h-5 mr-2" />
                    Schedule Appointment
                  </button>
                </div>
              )}
            </div>
          ) : (
            <div className="space-y-4">
              {filteredAppointments.map(appointment => (
                <AppointmentCard key={appointment.id} appointment={appointment} />
              ))}
            </div>
          )}
        </div>
      </div>

      {/* Schedule Modal */}
      <ScheduleModal />


    </div>
  );
};

export default EnhancedAppointments;