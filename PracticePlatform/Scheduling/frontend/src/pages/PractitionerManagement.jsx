import React, { useState, useEffect } from 'react';
import { Activity, Plus, Search, Edit, Trash2, Eye, Filter, X, Calendar } from 'lucide-react';
import { toast } from 'react-toastify';
import practitionerService from '../services/practitionerService';
import PractitionerForm from '../components/PractitionerForm';
import PractitionerAvailabilityManager from '../components/PractitionerAvailability/PractitionerAvailabilityManager';

const PractitionerManagement = () => {
  const [practitioners, setPractitioners] = useState([]);
  const [loading, setLoading] = useState(true);
  const [showForm, setShowForm] = useState(false);
  const [editingPractitioner, setEditingPractitioner] = useState(null);
  const [searchTerm, setSearchTerm] = useState('');
  const [filterActive, setFilterActive] = useState('all');
  const [currentPage, setCurrentPage] = useState(1);
  const [totalPages, setTotalPages] = useState(1);
  const [selectedPractitioner, setSelectedPractitioner] = useState(null);
  const [showDetails, setShowDetails] = useState(false);
  const [showAvailabilityManager, setShowAvailabilityManager] = useState(false);

  const fetchPractitioners = async () => {
    try {
      setLoading(true);
      const params = {
        skip: (currentPage - 1) * 10,
        limit: 10
      };
      
      if (filterActive !== 'all') {
        params.active = filterActive === 'active';
      }
      
      // Fetch practitioners and count in parallel
      const [data, countResponse] = await Promise.all([
        practitionerService.getPractitioners(params),
        fetch(`http://localhost:8000/practitioners/count?${filterActive !== 'all' ? `active=${filterActive === 'active'}` : ''}`)
      ]);
      
      const countData = await countResponse.json();
      const total = countData.total || 0;
      
      setPractitioners(data);
      setTotalPages(Math.ceil(total / 10));
    } catch (error) {
      console.error('Error fetching practitioners:', error);
      toast.error('Failed to fetch practitioners');
    } finally {
      setLoading(false);
    }
  };

  const searchPractitioners = async () => {
    if (!searchTerm.trim()) {
      fetchPractitioners();
      return;
    }

    try {
      setLoading(true);
      const data = await practitionerService.searchPractitionersByName({
        family_name: searchTerm,
        limit: 20
      });
      setPractitioners(data);
    } catch (error) {
      console.error('Error searching practitioners:', error);
      toast.error('Failed to search practitioners');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchPractitioners();
  }, [currentPage, filterActive]);

  const handleCreatePractitioner = async (practitionerData) => {
    try {
      await practitionerService.createPractitioner(practitionerData);
      toast.success('Practitioner created successfully');
      setShowForm(false);
      fetchPractitioners();
    } catch (error) {
      console.error('Error creating practitioner:', error);
      toast.error('Failed to create practitioner');
    }
  };

  const handleUpdatePractitioner = async (practitionerData) => {
    try {
      await practitionerService.updatePractitioner(editingPractitioner.id, practitionerData);
      toast.success('Practitioner updated successfully');
      setShowForm(false);
      setEditingPractitioner(null);
      fetchPractitioners();
    } catch (error) {
      console.error('Error updating practitioner:', error);
      toast.error('Failed to update practitioner');
    }
  };

  const handleDeletePractitioner = async (practitionerId) => {
    if (window.confirm('Are you sure you want to delete this practitioner?')) {
      try {
        await practitionerService.deletePractitioner(practitionerId);
        toast.success('Practitioner deleted successfully');
        fetchPractitioners();
      } catch (error) {
        console.error('Error deleting practitioner:', error);
        toast.error('Failed to delete practitioner');
      }
    }
  };

  const handleEditPractitioner = (practitioner) => {
    setEditingPractitioner(practitioner);
    setShowForm(true);
  };

  const handleViewPractitioner = async (practitionerId) => {
    try {
      const practitioner = await practitionerService.getPractitionerById(practitionerId);
      setSelectedPractitioner(practitioner);
      setShowDetails(true);
    } catch (error) {
      console.error('Error fetching practitioner details:', error);
      toast.error('Failed to fetch practitioner details');
    }
  };

  const handleSetAvailability = (practitioner) => {
    setSelectedPractitioner(practitioner);
    setShowAvailabilityManager(true);
  };

  const handleCloseAvailabilityManager = () => {
    setShowAvailabilityManager(false);
    setSelectedPractitioner(null);
  };

  const handleAvailabilityUpdate = () => {
    // Refresh practitioners list if needed
    fetchPractitioners();
  };

  const formatDate = (dateString) => {
    if (!dateString) return 'N/A';
    return new Date(dateString).toLocaleDateString();
  };

  const formatName = (practitioner) => {
    // If name field exists and is not null, use it
    if (practitioner.name) {
      return practitioner.name;
    }
    
    // Otherwise, construct name from individual components (like patient page)
    const givenNames = practitioner.given_names?.join(' ') || '';
    const familyName = practitioner.family_name || '';
    const prefix = practitioner.prefix || '';
    const suffix = practitioner.suffix || '';
    
    return `${prefix} ${givenNames} ${familyName} ${suffix}`.trim();
  };

  const getGenderDisplay = (gender) => {
    if (!gender) return 'Not specified';
    
    const genderMap = {
      male: 'Male',
      female: 'Female',
      other: 'Other',
      unknown: 'Unknown'
    };
    return genderMap[gender] || gender;
  };

  const getSpecialtyDisplay = (specialty) => {
    return specialty || 'Not specified';
  };

  const formatQualifications = (qualifications) => {
    if (!qualifications || qualifications.length === 0) return 'None';
    return qualifications.map(q => q.code?.text || 'Unknown').join(', ');
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">Practitioner Management</h1>
          <p className="text-gray-600">Manage healthcare practitioners and their profiles</p>
        </div>
        <button
          onClick={() => setShowForm(true)}
          className="bg-green-600 text-white px-4 py-2 rounded-md hover:bg-green-700 transition-colors flex items-center space-x-2"
        >
          <Plus className="h-4 w-4" />
          <span>Add Practitioner</span>
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
                placeholder="Search practitioners by name..."
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                className="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-green-500"
              />
            </div>
          </div>
          <div className="flex items-center space-x-2">
            <Filter className="h-4 w-4 text-gray-400" />
            <select
              value={filterActive}
              onChange={(e) => setFilterActive(e.target.value)}
              className="px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-green-500"
            >
              <option value="all">All Practitioners</option>
              <option value="active">Active Only</option>
              <option value="inactive">Inactive Only</option>
            </select>
            <button
              onClick={searchPractitioners}
              className="bg-gray-600 text-white px-4 py-2 rounded-md hover:bg-gray-700 transition-colors"
            >
              Search
            </button>
          </div>
        </div>
      </div>

      {/* Practitioners Table */}
      <div className="bg-white rounded-lg shadow overflow-hidden">
        {loading ? (
          <div className="p-8 text-center">
            <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-green-600 mx-auto"></div>
            <p className="mt-2 text-gray-600">Loading practitioners...</p>
          </div>
        ) : practitioners.length === 0 ? (
          <div className="p-8 text-center">
            <Activity className="h-12 w-12 text-gray-400 mx-auto mb-4" />
            <h3 className="text-lg font-medium text-gray-900 mb-2">No practitioners found</h3>
            <p className="text-gray-600">Get started by adding your first practitioner.</p>
          </div>
        ) : (
          <div className="overflow-x-auto">
            <table className="min-w-full divide-y divide-gray-200">
              <thead className="bg-gray-50">
                <tr>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Practitioner
                  </th>

                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Specialty
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
                {practitioners.map((practitioner) => (
                  <tr key={practitioner.id} className="hover:bg-gray-50">
                    <td className="px-6 py-4 whitespace-nowrap">
                      <div className="flex items-center">
                        <div className="flex-shrink-0 h-10 w-10">
                          <div className="h-10 w-10 rounded-full bg-green-100 flex items-center justify-center">
                            <Activity className="h-5 w-5 text-green-600" />
                          </div>
                        </div>
                        <div className="ml-4">
                          <div className="text-sm font-medium text-gray-900">
                            {formatName(practitioner)}
                          </div>
                        </div>
                      </div>
                    </td>

                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                      {getSpecialtyDisplay(practitioner.specialty)}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <span className={`inline-flex px-2 py-1 text-xs font-semibold rounded-full ${
                        practitioner.active
                          ? 'bg-green-100 text-green-800'
                          : 'bg-red-100 text-red-800'
                      }`}>
                        {practitioner.active ? 'Active' : 'Inactive'}
                      </span>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm font-medium">
                      <div className="flex space-x-2">
                        <button
                          onClick={() => handleViewPractitioner(practitioner.id)}
                          className="text-blue-600 hover:text-blue-900"
                          title="View Details"
                        >
                          <Eye className="h-4 w-4" />
                        </button>
                        <button
                          onClick={() => handleSetAvailability(practitioner)}
                          className="text-green-600 hover:text-green-900"
                          title="Set Availability"
                        >
                          <Calendar className="h-4 w-4" />
                        </button>
                        <button
                          onClick={() => handleEditPractitioner(practitioner)}
                          className="text-indigo-600 hover:text-indigo-900"
                          title="Edit Practitioner"
                        >
                          <Edit className="h-4 w-4" />
                        </button>
                        <button
                          onClick={() => handleDeletePractitioner(practitioner.id)}
                          className="text-red-600 hover:text-red-900"
                          title="Delete Practitioner"
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

      {/* Practitioner Form Modal */}
      <PractitionerForm
        practitioner={editingPractitioner}
        onSubmit={editingPractitioner ? handleUpdatePractitioner : handleCreatePractitioner}
        onCancel={() => {
          setShowForm(false);
          setEditingPractitioner(null);
        }}
        isOpen={showForm}
      />

      {/* Practitioner Details Modal */}
      {showDetails && selectedPractitioner && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-white rounded-lg shadow-xl w-full max-w-2xl max-h-[90vh] overflow-y-auto">
            <div className="flex items-center justify-between p-6 border-b">
              <div className="flex items-center space-x-2">
                <Activity className="h-5 w-5 text-green-600" />
                <h2 className="text-xl font-semibold text-gray-900">Practitioner Details</h2>
              </div>
              <button
                onClick={() => {
                  setShowDetails(false);
                  setSelectedPractitioner(null);
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
                  <p className="text-sm text-gray-900">{formatName(selectedPractitioner)}</p>
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700">FHIR ID</label>
                  <p className="text-sm text-gray-900">{selectedPractitioner.fhir_id}</p>
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700">Specialty</label>
                  <p className="text-sm text-gray-900">{getSpecialtyDisplay(selectedPractitioner.specialty)}</p>
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700">Status</label>
                  <span className={`inline-flex px-2 py-1 text-xs font-semibold rounded-full ${
                    selectedPractitioner.active
                      ? 'bg-green-100 text-green-800'
                      : 'bg-red-100 text-red-800'
                  }`}>
                    {selectedPractitioner.active ? 'Active' : 'Inactive'}
                  </span>
                </div>
              </div>
              

            </div>
          </div>
        </div>
      )}

      {/* Availability Manager Modal */}
      {showAvailabilityManager && selectedPractitioner && (
        <PractitionerAvailabilityManager
          practitioner={selectedPractitioner}
          onClose={handleCloseAvailabilityManager}
          onUpdate={handleAvailabilityUpdate}
        />
      )}
    </div>
  );
};

export default PractitionerManagement; 