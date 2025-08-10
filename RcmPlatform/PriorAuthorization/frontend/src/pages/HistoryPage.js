// File: src/pages/HistoryPage.js - History and Request Tracking Page
import React, { useState } from 'react';
import { Clock, CheckCircle, Search, Filter, User, Phone, Mail } from 'lucide-react';
import Card from '../components/common/Card';
import Button from '../components/common/Button';
import FormField from '../components/common/FormField';
import { useAuthorization } from '../contexts/AuthorizationContext';

const HistoryPage = () => {
  const { requests, patients } = useAuthorization();
  const [activeSection, setActiveSection] = useState('requests');
  const [searchTerm, setSearchTerm] = useState('');
  const [statusFilter, setStatusFilter] = useState('all');

  const filteredRequests = requests.filter(request => {
    const matchesSearch = request.patient_name.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         request.member_id.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         request.id.toLowerCase().includes(searchTerm.toLowerCase());
    const matchesFilter = statusFilter === 'all' || request.status === statusFilter;
    return matchesSearch && matchesFilter;
  });

  const filteredPatients = patients.filter(patient => {
    const matchesSearch = `${patient.first_name} ${patient.last_name}`.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         patient.member_id_primary?.toLowerCase().includes(searchTerm.toLowerCase());
    return matchesSearch;
  });

  const statusOptions = [
    { value: 'all', label: 'All Status' },
    { value: 'submitted', label: 'Submitted' },
    { value: 'completed', label: 'Completed' },
    { value: 'pending', label: 'Pending' }
  ];

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">Request History</h1>
          <p className="text-gray-600">View and manage your prior authorization requests and patient records</p>
        </div>
      </div>

      {/* Section Tabs */}
      <div className="border-b border-gray-200">
        <nav className="-mb-px flex space-x-8">
          {[
            { id: 'requests', name: 'Authorization Requests', count: requests.length },
            { id: 'patients', name: 'Patient Records', count: patients.length }
          ].map(({ id, name, count }) => (
            <button
              key={id}
              onClick={() => setActiveSection(id)}
              className={`py-2 px-1 border-b-2 font-medium text-sm ${
                activeSection === id
                  ? 'border-purple-500 text-purple-600'
                  : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
              }`}
            >
              {name} ({count})
            </button>
          ))}
        </nav>
      </div>

      {/* Filters */}
      <Card>
        <div className="flex flex-col sm:flex-row gap-4">
          <div className="flex-1">
            <FormField
              label=""
              type="text"
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              placeholder={`Search ${activeSection === 'requests' ? 'requests by patient name, member ID, or request ID' : 'patients by name or member ID'}...`}
            />
          </div>
          {activeSection === 'requests' && (
            <div className="sm:w-48">
              <FormField
                label=""
                type="select"
                value={statusFilter}
                onChange={(e) => setStatusFilter(e.target.value)}
                options={statusOptions}
              />
            </div>
          )}
        </div>
      </Card>

      {/* Content based on active section */}
      {activeSection === 'requests' ? (
        <Card title="Prior Authorization Requests">
          {filteredRequests.length === 0 ? (
            <div className="text-center py-12">
              <Clock className="h-12 w-12 text-gray-300 mx-auto mb-4" />
              <p className="text-gray-500">
                {requests.length === 0 ? 'No authorization requests found' : 'No requests match your filters'}
              </p>
            </div>
          ) : (
            <div className="space-y-4">
              {filteredRequests.map((request) => (
                <div key={request.id} className="border border-gray-200 rounded-lg p-4 hover:shadow-md transition-shadow">
                  <div className="flex items-center justify-between">
                    <div className="flex items-center space-x-3">
                      <div className={`h-3 w-3 rounded-full ${
                        request.result?.response_code === 'A1' ? 'bg-green-400' : 
                        request.status === 'submitted' ? 'bg-yellow-400' : 'bg-gray-400'
                      }`}></div>
                      <div>
                        <h3 className="text-sm font-medium text-gray-900">
                          {request.patient_name}
                        </h3>
                        <p className="text-sm text-gray-500">
                          Request ID: {request.id} | Member ID: {request.member_id}
                        </p>
                        <p className="text-xs text-gray-400">
                          Provider NPI: {request.provider_npi} | Priority: {request.priority}
                        </p>
                      </div>
                    </div>
                    
                    <div className="text-right">
                      <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${
                        request.result?.response_code === 'A1'
                          ? 'bg-green-100 text-green-800'
                          : request.status === 'submitted'
                          ? 'bg-yellow-100 text-yellow-800'
                          : 'bg-gray-100 text-gray-800'
                      }`}>
                        {request.result?.response_code === 'A1' ? (
                          <>
                            <CheckCircle className="h-3 w-3 mr-1" />
                            Approved
                          </>
                        ) : request.status === 'submitted' ? (
                          <>
                            <Clock className="h-3 w-3 mr-1" />
                            Pending
                          </>
                        ) : (
                          'Processing'
                        )}
                      </span>
                      <p className="text-xs text-gray-500 mt-1">
                        {new Date(request.timestamp).toLocaleString()}
                      </p>
                    </div>
                  </div>

                  {request.result && (
                    <div className="mt-4 pt-4 border-t border-gray-100">
                      <div className="grid grid-cols-1 md:grid-cols-3 gap-4 text-sm">
                        <div>
                          <span className="font-medium text-gray-700">Authorization #:</span>
                          <span className="ml-2 text-gray-600">
                            {request.result.authorization_number || 'N/A'}
                          </span>
                        </div>
                        <div>
                          <span className="font-medium text-gray-700">Decision:</span>
                          <span className={`ml-2 ${
                            request.result.response_code === 'A1' ? 'text-green-600' : 'text-red-600'
                          }`}>
                            {request.result.decision_reason || 'Approved'}
                          </span>
                        </div>
                        <div>
                          <span className="font-medium text-gray-700">Processed:</span>
                          <span className="ml-2 text-gray-600">
                            {new Date(request.result.processed_at).toLocaleString()}
                          </span>
                        </div>
                      </div>
                    </div>
                  )}
                </div>
              ))}
            </div>
          )}
        </Card>
      ) : (
        <Card title="Patient Information Records">
          {filteredPatients.length === 0 ? (
            <div className="text-center py-12">
              <User className="h-12 w-12 text-gray-300 mx-auto mb-4" />
              <p className="text-gray-500">
                {patients.length === 0 ? 'No patient records found' : 'No patients match your search'}
              </p>
            </div>
          ) : (
            <div className="space-y-4">
              {filteredPatients.map((patient) => (
                <div key={patient.id} className="border border-gray-200 rounded-lg p-4 hover:shadow-md transition-shadow">
                  <div className="flex items-center justify-between">
                    <div className="flex items-center space-x-3">
                      <div className="h-10 w-10 rounded-full bg-blue-100 flex items-center justify-center">
                        <User className="h-5 w-5 text-blue-600" />
                      </div>
                      <div>
                        <h4 className="text-sm font-medium text-gray-900">
                          {patient.first_name} {patient.last_name}
                        </h4>
                        <p className="text-sm text-gray-500">
                          Member ID: {patient.member_id_primary} | DOB: {patient.date_of_birth}
                        </p>
                        <p className="text-xs text-gray-400">
                          Gender: {patient.gender} | PCP: {patient.primary_care_provider || 'Not specified'}
                        </p>
                      </div>
                    </div>
                    
                    <div className="text-right">
                      <div className="flex items-center space-x-4 text-sm text-gray-500 mb-2">
                        {patient.phone_home && (
                          <div className="flex items-center">
                            <Phone className="h-4 w-4 mr-1" />
                            {patient.phone_home}
                          </div>
                        )}
                        {patient.email && (
                          <div className="flex items-center">
                            <Mail className="h-4 w-4 mr-1" />
                            {patient.email}
                          </div>
                        )}
                      </div>
                      <p className="text-xs text-gray-500">
                        Created: {new Date(patient.created_at).toLocaleDateString()}
                      </p>
                    </div>
                  </div>

                  {(patient.address_line1 || patient.city) && (
                    <div className="mt-3 pt-3 border-t border-gray-100">
                      <p className="text-sm text-gray-600">
                        <span className="font-medium">Address:</span> {' '}
                        {[patient.address_line1, patient.city, patient.state, patient.zip_code]
                          .filter(Boolean)
                          .join(', ')}
                      </p>
                    </div>
                  )}
                </div>
              ))}
            </div>
          )}
        </Card>
      )}
    </div>
  );
};

export default HistoryPage;
