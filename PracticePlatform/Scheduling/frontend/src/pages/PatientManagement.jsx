import React, { useState, useEffect } from 'react';
import { Users, Plus, Search, Edit, Trash2, Eye, Filter, X } from 'lucide-react';
import { toast } from 'react-toastify';
import patientService from '../services/patientService';
import PatientForm from '../components/PatientForm';

const PatientManagement = () => {
  const [patients, setPatients] = useState([]);
  const [loading, setLoading] = useState(true);
  const [showForm, setShowForm] = useState(false);
  const [editingPatient, setEditingPatient] = useState(null);
  const [searchTerm, setSearchTerm] = useState('');
  const [filterActive, setFilterActive] = useState('all');
  const [currentPage, setCurrentPage] = useState(1);
  const [totalPages, setTotalPages] = useState(1);
  const [selectedPatient, setSelectedPatient] = useState(null);
  const [showDetails, setShowDetails] = useState(false);

  const fetchPatients = async () => {
    try {
      setLoading(true);
      const params = {
        skip: (currentPage - 1) * 10,
        limit: 10
      };
      
      if (filterActive !== 'all') {
        params.active = filterActive === 'active';
      }
      
      const data = await patientService.getPatients(params);
      setPatients(data);
      setTotalPages(Math.ceil(data.length / 10) + 1); // Simple pagination
    } catch (error) {
      console.error('Error fetching patients:', error);
      toast.error('Failed to fetch persons');
    } finally {
      setLoading(false);
    }
  };

  const searchPatients = async () => {
    if (!searchTerm.trim()) {
      fetchPatients();
      return;
    }

    try {
      setLoading(true);
      const data = await patientService.searchPatientsByName({
        family_name: searchTerm,
        limit: 20
      });
      setPatients(data);
    } catch (error) {
      console.error('Error searching patients:', error);
      toast.error('Failed to search persons');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchPatients();
  }, [currentPage, filterActive]);

  const handleCreatePatient = async (patientData) => {
    try {
      await patientService.createPatient(patientData);
      toast.success('Person created successfully');
      setShowForm(false);
      fetchPatients();
    } catch (error) {
      console.error('Error creating patient:', error);
      toast.error('Failed to create person');
    }
  };

  const handleUpdatePatient = async (patientData) => {
    try {
      await patientService.updatePatient(editingPatient.id, patientData);
      toast.success('Person updated successfully');
      setShowForm(false);
      setEditingPatient(null);
      fetchPatients();
    } catch (error) {
      console.error('Error updating patient:', error);
      toast.error('Failed to update person');
    }
  };

  const handleDeletePatient = async (patientId) => {
    if (window.confirm('Are you sure you want to delete this person?')) {
      try {
        await patientService.deletePatient(patientId);
        toast.success('Person deleted successfully');
        fetchPatients();
      } catch (error) {
        console.error('Error deleting patient:', error);
        toast.error('Failed to delete person');
      }
    }
  };

  const handleEditPatient = (patient) => {
    setEditingPatient(patient);
    setShowForm(true);
  };

  const handleViewPatient = async (patientId) => {
    try {
      const patient = await patientService.getPatientById(patientId);
      setSelectedPatient(patient);
      setShowDetails(true);
    } catch (error) {
      console.error('Error fetching patient details:', error);
      toast.error('Failed to fetch patient details');
    }
  };

  const formatDate = (dateString) => {
    if (!dateString) return 'N/A';
    return new Date(dateString).toLocaleDateString();
  };

  const formatName = (patient) => {
    const givenNames = patient.given_names?.join(' ') || '';
    const familyName = patient.family_name || '';
    const prefix = patient.prefix || '';
    const suffix = patient.suffix || '';
    
    return `${prefix} ${givenNames} ${familyName} ${suffix}`.trim();
  };

  const getGenderDisplay = (gender) => {
    const genderMap = {
      male: 'Male',
      female: 'Female',
      other: 'Other',
      unknown: 'Unknown'
    };
    return genderMap[gender] || gender;
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">Person Management</h1>
          <p className="text-gray-600">Manage persons and their information</p>
        </div>
        <button
          onClick={() => setShowForm(true)}
          className="bg-blue-600 text-white px-4 py-2 rounded-md hover:bg-blue-700 transition-colors flex items-center space-x-2"
        >
          <Plus className="h-4 w-4" />
          <span>Add Person</span>
        </button>
      </div>

      {/* Search and Filters */}
      <div className="bg-white rounded-lg shadow p-6">
        <div className="flex flex-col md:flex-row gap-4">
          <div className="flex-1">
            <div className="relative">
              <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 h-4 w-4" />
              <input
                type="text"
                placeholder="Search persons by name..."
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                className="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              />
            </div>
          </div>
          <div className="flex items-center space-x-2">
            <Filter className="h-4 w-4 text-gray-400" />
            <select
              value={filterActive}
              onChange={(e) => setFilterActive(e.target.value)}
              className="px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            >
              <option value="all">All Persons</option>
              <option value="active">Active Only</option>
              <option value="inactive">Inactive Only</option>
            </select>
            <button
              onClick={searchPatients}
              className="bg-gray-600 text-white px-4 py-2 rounded-md hover:bg-gray-700 transition-colors"
            >
              Search
            </button>
          </div>
        </div>
      </div>

      {/* Patients Table */}
      <div className="bg-white rounded-lg shadow overflow-hidden">
        {loading ? (
          <div className="p-8 text-center">
            <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600 mx-auto"></div>
            <p className="mt-2 text-gray-600">Loading persons...</p>
          </div>
        ) : patients.length === 0 ? (
          <div className="p-8 text-center">
            <Users className="h-12 w-12 text-gray-400 mx-auto mb-4" />
            <h3 className="text-lg font-medium text-gray-900 mb-2">No persons found</h3>
            <p className="text-gray-600">Get started by adding your first person.</p>
          </div>
        ) : (
          <div className="overflow-x-auto">
            <table className="min-w-full divide-y divide-gray-200">
              <thead className="bg-gray-50">
                <tr>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Person
                  </th>

                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Gender
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Birth Date
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Status
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Actions
                  </th>
                </tr>
              </thead>
              <tbody className="bg-white divide-y divide-gray-200">
                {patients.map((patient) => (
                  <tr key={patient.id} className="hover:bg-gray-50">
                    <td className="px-6 py-4 whitespace-nowrap">
                      <div className="flex items-center">
                        <div className="flex-shrink-0 h-10 w-10">
                          <div className="h-10 w-10 rounded-full bg-blue-100 flex items-center justify-center">
                            <Users className="h-5 w-5 text-blue-600" />
                          </div>
                        </div>
                        <div className="ml-4">
                          <div className="text-sm font-medium text-gray-900">
                            {formatName(patient)}
                          </div>
                        </div>
                      </div>
                    </td>

                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                      {getGenderDisplay(patient.gender)}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                      {formatDate(patient.birth_date)}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <span className={`inline-flex px-2 py-1 text-xs font-semibold rounded-full ${
                        patient.active
                          ? 'bg-green-100 text-green-800'
                          : 'bg-red-100 text-red-800'
                      }`}>
                        {patient.active ? 'Active' : 'Inactive'}
                      </span>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm font-medium">
                      <div className="flex space-x-2">
                        <button
                          onClick={() => handleViewPatient(patient.id)}
                          className="text-blue-600 hover:text-blue-900"
                          title="View Details"
                        >
                          <Eye className="h-4 w-4" />
                        </button>
                        <button
                          onClick={() => handleEditPatient(patient)}
                          className="text-indigo-600 hover:text-indigo-900"
                          title="Edit Patient"
                        >
                          <Edit className="h-4 w-4" />
                        </button>
                        <button
                          onClick={() => handleDeletePatient(patient.id)}
                          className="text-red-600 hover:text-red-900"
                          title="Delete Patient"
                        >
                          <Trash2 className="h-4 w-4" />
                        </button>
                      </div>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>

      {/* Pagination */}
      {totalPages > 1 && (
        <div className="flex justify-center space-x-2">
          <button
            onClick={() => setCurrentPage(prev => Math.max(1, prev - 1))}
            disabled={currentPage === 1}
            className="px-3 py-2 border border-gray-300 rounded-md disabled:opacity-50 disabled:cursor-not-allowed"
          >
            Previous
          </button>
          <span className="px-3 py-2 text-gray-700">
            Page {currentPage} of {totalPages}
          </span>
          <button
            onClick={() => setCurrentPage(prev => Math.min(totalPages, prev + 1))}
            disabled={currentPage === totalPages}
            className="px-3 py-2 border border-gray-300 rounded-md disabled:opacity-50 disabled:cursor-not-allowed"
          >
            Next
          </button>
        </div>
      )}

      {/* Patient Form Modal */}
      <PatientForm
        patient={editingPatient}
        onSubmit={editingPatient ? handleUpdatePatient : handleCreatePatient}
        onCancel={() => {
          setShowForm(false);
          setEditingPatient(null);
        }}
        isOpen={showForm}
      />

      {/* Patient Details Modal */}
      {showDetails && selectedPatient && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-white rounded-lg shadow-xl w-full max-w-2xl max-h-[90vh] overflow-y-auto">
            <div className="flex items-center justify-between p-6 border-b">
              <div className="flex items-center space-x-2">
                <Users className="h-5 w-5 text-blue-600" />
                <h2 className="text-xl font-semibold text-gray-900">Patient Details</h2>
              </div>
              <button
                onClick={() => {
                  setShowDetails(false);
                  setSelectedPatient(null);
                }}
                className="text-gray-400 hover:text-gray-600 transition-colors"
              >
                <X className="h-5 w-5" />
              </button>
            </div>
            <div className="p-6 space-y-4">
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700">Full Name</label>
                  <p className="text-sm text-gray-900">{formatName(selectedPatient)}</p>
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700">FHIR ID</label>
                  <p className="text-sm text-gray-900">{selectedPatient.fhir_id}</p>
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700">Gender</label>
                  <p className="text-sm text-gray-900">{getGenderDisplay(selectedPatient.gender)}</p>
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700">Birth Date</label>
                  <p className="text-sm text-gray-900">{formatDate(selectedPatient.birth_date)}</p>
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700">Status</label>
                  <span className={`inline-flex px-2 py-1 text-xs font-semibold rounded-full ${
                    selectedPatient.active
                      ? 'bg-green-100 text-green-800'
                      : 'bg-red-100 text-red-800'
                  }`}>
                    {selectedPatient.active ? 'Active' : 'Inactive'}
                  </span>
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700">Created</label>
                  <p className="text-sm text-gray-900">{formatDate(selectedPatient.created_at)}</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default PatientManagement; 