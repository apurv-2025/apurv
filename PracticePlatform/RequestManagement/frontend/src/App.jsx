import React, { useState, useEffect } from 'react';
import { Calendar, Clock, User, CheckCircle, XCircle, AlertCircle, Plus } from 'lucide-react';
import api from './api';

const RequestManagementApp = () => {
  const [activeTab, setActiveTab] = useState('client'); // 'client' or 'practitioner'
  const [appointmentRequests, setAppointmentRequests] = useState([]);
  const [practitioners, setPractitioners] = useState([]);
  const [clients, setClients] = useState([]);
  const [appointments, setAppointments] = useState([]);

  // Load data from API
  useEffect(() => {
    const loadData = async () => {
      try {
        const [practitionersData, appointmentRequestsData] = await Promise.all([
          api.getPractitioners(),
          api.getAppointmentRequests()
        ]);
        
        setPractitioners(practitionersData);
        setAppointmentRequests(appointmentRequestsData);
      } catch (error) {
        console.error('Error loading data:', error);
        // Fall back to mock data if API is not available
        setPractitioners([
          { id: 1, name: 'Dr. Sarah Johnson', specialization: 'General Practice', email: 'sarah@clinic.com' },
          { id: 2, name: 'Dr. Michael Chen', specialization: 'Cardiology', email: 'michael@clinic.com' },
          { id: 3, name: 'Dr. Emily Rodriguez', specialization: 'Dermatology', email: 'emily@clinic.com' }
        ]);
        
        setAppointmentRequests([
          {
            id: 1,
            client_id: 1,
            client_name: 'John Smith',
            practitioner_id: 1,
            practitioner_name: 'Dr. Sarah Johnson',
            requested_datetime: '2025-07-15T10:00:00',
            status: 'pending',
            notes: 'Annual checkup needed',
            created_at: '2025-07-10T08:30:00'
          }
        ]);
      }
    };

    loadData();
  }, []);

  const handleRequestAction = async (requestId, action) => {
    try {
      await api.updateAppointmentRequest(requestId, action);
      setAppointmentRequests(prev => 
        prev.map(request => 
          request.id === requestId 
            ? { ...request, status: action }
            : request
        )
      );
    } catch (error) {
      console.error('Error updating request:', error);
      alert('Failed to update request. Please try again.');
    }
  };

  const ClientPortal = () => {
    const [newRequest, setNewRequest] = useState({
      clientId: 1, // Mock logged-in client
      practitionerId: '',
      requestedDateTime: '',
      source: 'client_portal',
      notes: ''
    });

    const handleSubmitRequest = async () => {
      if (!newRequest.practitionerId || !newRequest.requestedDateTime) return;
      
      try {
        const requestData = {
          client_id: newRequest.clientId,
          practitioner_id: parseInt(newRequest.practitionerId),
          requested_datetime: newRequest.requestedDateTime,
          source: newRequest.source,
          notes: newRequest.notes
        };
        
        await api.createAppointmentRequest(requestData);
        
        // Reload appointment requests to get the updated list
        const updatedRequests = await api.getAppointmentRequests();
        setAppointmentRequests(updatedRequests);
        
        setNewRequest({ clientId: 1, practitionerId: '', requestedDateTime: '', source: 'client_portal', notes: '' });
        alert('Appointment request submitted successfully!');
      } catch (error) {
        console.error('Error creating request:', error);
        alert('Failed to submit request. Please try again.');
      }
    };

    const userRequests = appointmentRequests.filter(req => req.client_id === 1);

    return (
      <div className="max-w-4xl mx-auto p-6">
        <h1 className="text-3xl font-bold text-gray-800 mb-8">Client Portal - Request Appointment</h1>
        
        {/* New Request Form */}
        <div className="bg-white rounded-lg shadow-md p-6 mb-8">
          <h2 className="text-xl font-semibold mb-4 flex items-center">
            <Plus className="mr-2" size={20} />
            Request New Appointment
          </h2>
          
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Select Practitioner
              </label>
              <select
                value={newRequest.practitionerId}
                onChange={(e) => setNewRequest(prev => ({ ...prev, practitionerId: e.target.value }))}
                className="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              >
                <option value="">Choose a practitioner...</option>
                {practitioners.map(practitioner => (
                  <option key={practitioner.id} value={practitioner.id}>
                    {practitioner.name} - {practitioner.specialization}
                  </option>
                ))}
              </select>
            </div>
            
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Preferred Date & Time
              </label>
              <input
                type="datetime-local"
                value={newRequest.requestedDateTime}
                onChange={(e) => setNewRequest(prev => ({ ...prev, requestedDateTime: e.target.value }))}
                className="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              />
            </div>
            
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Request Source
              </label>
              <select
                value={newRequest.source}
                onChange={(e) => setNewRequest(prev => ({ ...prev, source: e.target.value }))}
                className="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              >
                <option value="client_portal">Client Portal</option>
                <option value="website">Website</option>
                <option value="ai_agent">AI Agent</option>
              </select>
            </div>
            
            <div className="md:col-span-2">
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Notes (Optional)
              </label>
              <textarea
                value={newRequest.notes}
                onChange={(e) => setNewRequest(prev => ({ ...prev, notes: e.target.value }))}
                placeholder="Describe your symptoms or reason for visit..."
                className="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                rows={3}
              />
            </div>
            
            <div className="md:col-span-2">
              <button
                onClick={handleSubmitRequest}
                className="w-full bg-blue-600 text-white py-3 px-6 rounded-lg hover:bg-blue-700 transition duration-200 font-medium"
              >
                Submit Request
              </button>
            </div>
          </div>
        </div>

        {/* Request History */}
        <div className="bg-white rounded-lg shadow-md p-6">
          <h2 className="text-xl font-semibold mb-4">Your Appointment Requests</h2>
          
          {userRequests.length === 0 ? (
            <p className="text-gray-500 text-center py-8">No appointment requests yet.</p>
          ) : (
            <div className="space-y-4">
              {userRequests.map(request => (
                <div key={request.id} className="border border-gray-200 rounded-lg p-4">
                  <div className="flex justify-between items-start">
                    <div className="flex-1">
                      <div className="flex items-center mb-2">
                        <User className="mr-2" size={16} />
                        <span className="font-medium">{request.practitioner_name}</span>
                      </div>
                      <div className="flex items-center mb-2 text-gray-600">
                        <Calendar className="mr-2" size={16} />
                        <span>{new Date(request.requested_datetime).toLocaleDateString()}</span>
                        <Clock className="ml-4 mr-2" size={16} />
                        <span>{new Date(request.requested_datetime).toLocaleTimeString()}</span>
                      </div>
                      {request.notes && (
                        <p className="text-gray-600 text-sm">{request.notes}</p>
                      )}
                      <div className="text-xs text-gray-500 mt-1">
                        Source: <span className="capitalize">{request.source?.replace('_', ' ')}</span>
                      </div>
                    </div>
                    <div className="ml-4">
                      <span className={`px-3 py-1 rounded-full text-xs font-medium ${
                        request.status === 'pending' ? 'bg-yellow-100 text-yellow-800' :
                        request.status === 'approved' ? 'bg-green-100 text-green-800' :
                        'bg-red-100 text-red-800'
                      }`}>
                        {request.status.charAt(0).toUpperCase() + request.status.slice(1)}
                      </span>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>
    );
  };

  const PractitionerDashboard = () => {
    const pendingRequests = appointmentRequests.filter(req => req.status === 'pending');
    const approvedRequests = appointmentRequests.filter(req => req.status === 'approved');

    return (
      <div className="max-w-6xl mx-auto p-6">
        <h1 className="text-3xl font-bold text-gray-800 mb-8">Practitioner Dashboard</h1>
        
        {/* Stats Cards */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
          <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-6">
            <div className="flex items-center">
              <AlertCircle className="text-yellow-600 mr-3" size={24} />
              <div>
                <p className="text-sm text-yellow-600">Pending Requests</p>
                <p className="text-2xl font-bold text-yellow-800">{pendingRequests.length}</p>
              </div>
            </div>
          </div>
          
          <div className="bg-green-50 border border-green-200 rounded-lg p-6">
            <div className="flex items-center">
              <CheckCircle className="text-green-600 mr-3" size={24} />
              <div>
                <p className="text-sm text-green-600">Approved Today</p>
                <p className="text-2xl font-bold text-green-800">{approvedRequests.length}</p>
              </div>
            </div>
          </div>
          
          <div className="bg-blue-50 border border-blue-200 rounded-lg p-6">
            <div className="flex items-center">
              <Calendar className="text-blue-600 mr-3" size={24} />
              <div>
                <p className="text-sm text-blue-600">Total Requests</p>
                <p className="text-2xl font-bold text-blue-800">{appointmentRequests.length}</p>
              </div>
            </div>
          </div>
        </div>

        {/* Pending Requests */}
        <div className="bg-white rounded-lg shadow-md p-6 mb-8">
          <h2 className="text-xl font-semibold mb-4">Pending Appointment Requests</h2>
          
          {pendingRequests.length === 0 ? (
            <p className="text-gray-500 text-center py-8">No pending requests.</p>
          ) : (
            <div className="space-y-4">
              {pendingRequests.map(request => (
                <div key={request.id} className="border border-gray-200 rounded-lg p-4">
                  <div className="flex justify-between items-start">
                    <div className="flex-1">
                      <div className="flex items-center mb-2">
                        <User className="mr-2" size={16} />
                        <span className="font-medium">{request.client_name}</span>
                      </div>
                      <div className="flex items-center mb-2 text-gray-600">
                        <Calendar className="mr-2" size={16} />
                        <span>{new Date(request.requested_datetime).toLocaleDateString()}</span>
                        <Clock className="ml-4 mr-2" size={16} />
                        <span>{new Date(request.requested_datetime).toLocaleTimeString()}</span>
                      </div>
                      <div className="text-gray-600 text-sm mb-2">
                        Practitioner: {request.practitioner_name}
                      </div>
                      {request.notes && (
                        <p className="text-gray-600 text-sm">{request.notes}</p>
                      )}
                      <div className="text-xs text-gray-500 mt-1">
                        Source: <span className="capitalize">{request.source?.replace('_', ' ')}</span>
                      </div>
                      <p className="text-xs text-gray-400 mt-2">
                        Requested: {new Date(request.created_at).toLocaleString()}
                      </p>
                    </div>
                    <div className="ml-4 flex gap-2">
                      <button
                        onClick={() => handleRequestAction(request.id, 'approved')}
                        className="bg-green-600 text-white px-4 py-2 rounded-lg hover:bg-green-700 transition duration-200 flex items-center gap-1"
                      >
                        <CheckCircle size={16} />
                        Approve
                      </button>
                      <button
                        onClick={() => handleRequestAction(request.id, 'denied')}
                        className="bg-red-600 text-white px-4 py-2 rounded-lg hover:bg-red-700 transition duration-200 flex items-center gap-1"
                      >
                        <XCircle size={16} />
                        Deny
                      </button>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>

        {/* All Requests */}
        <div className="bg-white rounded-lg shadow-md p-6">
          <h2 className="text-xl font-semibold mb-4">All Appointment Requests</h2>
          
          <div className="overflow-x-auto">
            <table className="w-full text-sm">
              <thead>
                <tr className="border-b border-gray-200">
                  <th className="text-left py-3 px-4">Client</th>
                  <th className="text-left py-3 px-4">Practitioner</th>
                  <th className="text-left py-3 px-4">Requested Time</th>
                  <th className="text-left py-3 px-4">Status</th>
                  <th className="text-left py-3 px-4">Source</th>
                  <th className="text-left py-3 px-4">Notes</th>
                </tr>
              </thead>
              <tbody>
                {appointmentRequests.map(request => (
                  <tr key={request.id} className="border-b border-gray-100">
                    <td className="py-3 px-4">{request.client_name}</td>
                    <td className="py-3 px-4">{request.practitioner_name}</td>
                    <td className="py-3 px-4">
                      {new Date(request.requested_datetime).toLocaleDateString()} {' '}
                      {new Date(request.requested_datetime).toLocaleTimeString()}
                    </td>
                    <td className="py-3 px-4">
                      <span className={`px-2 py-1 rounded-full text-xs font-medium ${
                        request.status === 'pending' ? 'bg-yellow-100 text-yellow-800' :
                        request.status === 'approved' ? 'bg-green-100 text-green-800' :
                        'bg-red-100 text-red-800'
                      }`}>
                        {request.status.charAt(0).toUpperCase() + request.status.slice(1)}
                      </span>
                    </td>
                    <td className="py-3 px-4">
                      <span className={`px-2 py-1 rounded-full text-xs font-medium ${
                        request.source === 'client_portal' ? 'bg-blue-100 text-blue-800' :
                        request.source === 'website' ? 'bg-purple-100 text-purple-800' :
                        'bg-green-100 text-green-800'
                      }`}>
                        {request.source?.replace('_', ' ').charAt(0).toUpperCase() + request.source?.replace('_', ' ').slice(1)}
                      </span>
                    </td>
                    <td className="py-3 px-4 text-gray-600">{request.notes || '-'}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      </div>
    );
  };

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Navigation */}
      <nav className="bg-white shadow-sm border-b border-gray-200">
        <div className="max-w-6xl mx-auto px-6">
          <div className="flex justify-between items-center h-16">
            <div className="flex items-center">
              <h1 className="text-xl font-bold text-gray-800">Practice Management</h1>
            </div>
            <div className="flex space-x-4">
              <button
                onClick={() => setActiveTab('client')}
                className={`px-4 py-2 rounded-lg font-medium transition duration-200 ${
                  activeTab === 'client'
                    ? 'bg-blue-600 text-white'
                    : 'text-gray-600 hover:text-gray-800'
                }`}
              >
                Client Portal
              </button>
              <button
                onClick={() => setActiveTab('practitioner')}
                className={`px-4 py-2 rounded-lg font-medium transition duration-200 ${
                  activeTab === 'practitioner'
                    ? 'bg-blue-600 text-white'
                    : 'text-gray-600 hover:text-gray-800'
                }`}
              >
                Practitioner Dashboard
              </button>
            </div>
          </div>
        </div>
      </nav>

      {/* Main Content */}
      {activeTab === 'client' ? <ClientPortal /> : <PractitionerDashboard />}
    </div>
  );
};

export default RequestManagementApp;
