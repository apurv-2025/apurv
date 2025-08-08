import React, { useState, useEffect } from 'react';
import { Clock, Plus, Search, Edit, Trash2, Eye, Filter, X, Calendar, Users, Activity, BarChart3 } from 'lucide-react';
import { toast } from 'react-toastify';
import waitlistService from '../services/waitlistService';
import WaitlistForm from '../components/WaitlistForm';

const WaitlistManagement = () => {
  const [waitlistEntries, setWaitlistEntries] = useState([]);
  const [loading, setLoading] = useState(true);
  const [showForm, setShowForm] = useState(false);
  const [editingEntry, setEditingEntry] = useState(null);
  const [searchTerm, setSearchTerm] = useState('');
  const [filterStatus, setFilterStatus] = useState('all');
  const [filterPriority, setFilterPriority] = useState('all');
  const [filterServiceType, setFilterServiceType] = useState('all');
  const [currentPage, setCurrentPage] = useState(1);
  const [totalPages, setTotalPages] = useState(1);
  const [selectedEntry, setSelectedEntry] = useState(null);
  const [showDetails, setShowDetails] = useState(false);
  const [stats, setStats] = useState(null);
  const [showStats, setShowStats] = useState(false);

  const fetchWaitlistEntries = async () => {
    try {
      setLoading(true);
      const params = {
        skip: (currentPage - 1) * 10,
        limit: 10
      };
      
      if (filterStatus !== 'all') {
        params.status = filterStatus;
      }
      if (filterPriority !== 'all') {
        params.priority = filterPriority;
      }
      if (filterServiceType !== 'all') {
        params.service_type = filterServiceType;
      }
      
      const data = await waitlistService.getWaitlistEntries(params);
      setWaitlistEntries(data);
      setTotalPages(Math.ceil(data.length / 10) + 1);
    } catch (error) {
      console.error('Error fetching waitlist entries:', error);
      toast.error('Failed to fetch waitlist entries');
    } finally {
      setLoading(false);
    }
  };

  const fetchStats = async () => {
    try {
      const data = await waitlistService.getWaitlistStats();
      setStats(data);
    } catch (error) {
      console.error('Error fetching stats:', error);
    }
  };

  useEffect(() => {
    fetchWaitlistEntries();
    fetchStats();
  }, [currentPage, filterStatus, filterPriority, filterServiceType]);

  const handleCreateEntry = async (entryData) => {
    try {
      await waitlistService.createWaitlistEntry(entryData);
      toast.success('Waitlist entry created successfully');
      setShowForm(false);
      fetchWaitlistEntries();
      fetchStats();
    } catch (error) {
      console.error('Error creating waitlist entry:', error);
      toast.error('Failed to create waitlist entry');
    }
  };

  const handleUpdateEntry = async (entryData) => {
    try {
      await waitlistService.updateWaitlistEntry(editingEntry.id, entryData);
      toast.success('Waitlist entry updated successfully');
      setShowForm(false);
      setEditingEntry(null);
      fetchWaitlistEntries();
      fetchStats();
    } catch (error) {
      console.error('Error updating waitlist entry:', error);
      toast.error('Failed to update waitlist entry');
    }
  };

  const handleDeleteEntry = async (entryId) => {
    if (window.confirm('Are you sure you want to delete this waitlist entry?')) {
      try {
        await waitlistService.deleteWaitlistEntry(entryId);
        toast.success('Waitlist entry deleted successfully');
        fetchWaitlistEntries();
        fetchStats();
      } catch (error) {
        console.error('Error deleting waitlist entry:', error);
        toast.error('Failed to delete waitlist entry');
      }
    }
  };

  const handleEditEntry = (entry) => {
    setEditingEntry(entry);
    setShowForm(true);
  };

  const handleViewEntry = async (entryId) => {
    try {
      const entry = await waitlistService.getWaitlistEntryById(entryId);
      setSelectedEntry(entry);
      setShowDetails(true);
    } catch (error) {
      console.error('Error fetching waitlist entry details:', error);
      toast.error('Failed to fetch waitlist entry details');
    }
  };

  const handleScheduleEntry = async (entryId) => {
    try {
      await waitlistService.scheduleFromWaitlist(entryId);
      toast.success('Waitlist entry marked as scheduled');
      fetchWaitlistEntries();
      fetchStats();
    } catch (error) {
      console.error('Error scheduling from waitlist:', error);
      toast.error('Failed to schedule from waitlist');
    }
  };

  const formatDate = (dateString) => {
    if (!dateString) return 'N/A';
    return new Date(dateString).toLocaleDateString();
  };

  const formatTime = (timeString) => {
    if (!timeString) return 'N/A';
    return timeString;
  };

  const getPriorityColor = (priority) => {
    const colors = {
      LOW: 'bg-gray-100 text-gray-800',
      NORMAL: 'bg-blue-100 text-blue-800',
      HIGH: 'bg-yellow-100 text-yellow-800',
      URGENT: 'bg-red-100 text-red-800'
    };
    return colors[priority] || 'bg-gray-100 text-gray-800';
  };

  const getStatusColor = (status) => {
    const colors = {
      ACTIVE: 'bg-green-100 text-green-800',
      CONTACTED: 'bg-blue-100 text-blue-800',
      SCHEDULED: 'bg-purple-100 text-purple-800',
      REMOVED: 'bg-gray-100 text-gray-800'
    };
    return colors[status] || 'bg-gray-100 text-gray-800';
  };

  const getServiceTypeDisplay = (serviceType) => {
    const displayMap = {
      THERAPY: 'Therapy',
      CONSULTATION: 'Consultation',
      ASSESSMENT: 'Assessment',
      MEDICAL: 'Medical',
      MENTAL_HEALTH: 'Mental Health',
      FOLLOW_UP: 'Follow-up',
      EMERGENCY: 'Emergency'
    };
    return displayMap[serviceType] || serviceType;
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">Waitlist Management</h1>
          <p className="text-gray-600">Manage waitlist entries and priorities</p>
        </div>
        <div className="flex space-x-3">
          <button
            onClick={() => setShowStats(!showStats)}
            className="bg-purple-600 text-white px-4 py-2 rounded-md hover:bg-purple-700 transition-colors flex items-center space-x-2"
          >
            <BarChart3 className="h-4 w-4" />
            <span>Stats</span>
          </button>
          <button
            onClick={() => setShowForm(true)}
            className="bg-orange-600 text-white px-4 py-2 rounded-md hover:bg-orange-700 transition-colors flex items-center space-x-2"
          >
            <Plus className="h-4 w-4" />
            <span>Add Entry</span>
          </button>
        </div>
      </div>

      {/* Statistics Panel */}
      {showStats && stats && (
        <div className="bg-white rounded-lg shadow p-6">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Waitlist Statistics</h3>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            <div className="text-center">
              <div className="text-2xl font-bold text-blue-600">{stats.total_entries}</div>
              <div className="text-sm text-gray-600">Total Entries</div>
            </div>
            <div className="text-center">
              <div className="text-2xl font-bold text-green-600">{stats.active_entries}</div>
              <div className="text-sm text-gray-600">Active</div>
            </div>
            <div className="text-center">
              <div className="text-2xl font-bold text-blue-600">{stats.contacted_entries}</div>
              <div className="text-sm text-gray-600">Contacted</div>
            </div>
            <div className="text-center">
              <div className="text-2xl font-bold text-purple-600">{stats.scheduled_entries}</div>
              <div className="text-sm text-gray-600">Scheduled</div>
            </div>
          </div>
          
          <div className="mt-6 grid grid-cols-1 md:grid-cols-2 gap-6">
            <div>
              <h4 className="font-medium text-gray-900 mb-2">Priority Distribution</h4>
              <div className="space-y-2">
                {Object.entries(stats.priority_distribution).map(([priority, count]) => (
                  <div key={priority} className="flex justify-between">
                    <span className="text-sm text-gray-600">{priority}</span>
                    <span className="text-sm font-medium">{count}</span>
                  </div>
                ))}
              </div>
            </div>
            <div>
              <h4 className="font-medium text-gray-900 mb-2">Service Type Distribution</h4>
              <div className="space-y-2">
                {Object.entries(stats.service_type_distribution).map(([serviceType, count]) => (
                  <div key={serviceType} className="flex justify-between">
                    <span className="text-sm text-gray-600">{getServiceTypeDisplay(serviceType)}</span>
                    <span className="text-sm font-medium">{count}</span>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Search and Filters */}
      <div className="bg-white rounded-lg shadow p-6">
        <div className="flex flex-col md:flex-row gap-4">
          <div className="flex-1">
            <div className="relative">
              <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 h-4 w-4" />
              <input
                type="text"
                placeholder="Search waitlist entries..."
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                className="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-orange-500"
              />
            </div>
          </div>
          <div className="flex items-center space-x-2">
            <Filter className="h-4 w-4 text-gray-400" />
            <select
              value={filterStatus}
              onChange={(e) => setFilterStatus(e.target.value)}
              className="px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-orange-500"
            >
              <option value="all">All Status</option>
              <option value="ACTIVE">Active</option>
              <option value="CONTACTED">Contacted</option>
              <option value="SCHEDULED">Scheduled</option>
              <option value="REMOVED">Removed</option>
            </select>
            <select
              value={filterPriority}
              onChange={(e) => setFilterPriority(e.target.value)}
              className="px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-orange-500"
            >
              <option value="all">All Priorities</option>
              <option value="LOW">Low</option>
              <option value="NORMAL">Normal</option>
              <option value="HIGH">High</option>
              <option value="URGENT">Urgent</option>
            </select>
            <select
              value={filterServiceType}
              onChange={(e) => setFilterServiceType(e.target.value)}
              className="px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-orange-500"
            >
              <option value="all">All Services</option>
              <option value="THERAPY">Therapy</option>
              <option value="CONSULTATION">Consultation</option>
              <option value="ASSESSMENT">Assessment</option>
              <option value="MEDICAL">Medical</option>
              <option value="MENTAL_HEALTH">Mental Health</option>
              <option value="FOLLOW_UP">Follow-up</option>
              <option value="EMERGENCY">Emergency</option>
            </select>
          </div>
        </div>
      </div>

      {/* Waitlist Table */}
      <div className="bg-white rounded-lg shadow overflow-hidden">
        {loading ? (
          <div className="p-8 text-center">
            <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-orange-600 mx-auto"></div>
            <p className="mt-2 text-gray-600">Loading waitlist entries...</p>
          </div>
        ) : waitlistEntries.length === 0 ? (
          <div className="p-8 text-center">
            <Clock className="h-12 w-12 text-gray-400 mx-auto mb-4" />
            <h3 className="text-lg font-medium text-gray-900 mb-2">No waitlist entries found</h3>
            <p className="text-gray-600">Get started by adding your first waitlist entry.</p>
          </div>
        ) : (
          <div className="overflow-x-auto">
            <table className="min-w-full divide-y divide-gray-200">
              <thead className="bg-gray-50">
                <tr>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Patient/Practitioner
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Service Type
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Priority
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Status
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Created
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Actions
                  </th>
                </tr>
              </thead>
              <tbody className="bg-white divide-y divide-gray-200">
                {waitlistEntries.map((entry) => (
                  <tr key={entry.id} className="hover:bg-gray-50">
                    <td className="px-6 py-4 whitespace-nowrap">
                      <div className="flex items-center">
                        <div className="flex-shrink-0 h-10 w-10">
                          <div className="h-10 w-10 rounded-full bg-orange-100 flex items-center justify-center">
                            <Clock className="h-5 w-5 text-orange-600" />
                          </div>
                        </div>
                        <div className="ml-4">
                          <div className="text-sm font-medium text-gray-900">
                            {entry.patient_name || 'No Patient'}
                          </div>
                          <div className="text-sm text-gray-500">
                            {entry.practitioner_name || 'No Practitioner'}
                          </div>
                        </div>
                      </div>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                      {getServiceTypeDisplay(entry.service_type)}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <span className={`inline-flex px-2 py-1 text-xs font-semibold rounded-full ${getPriorityColor(entry.priority)}`}>
                        {entry.priority}
                      </span>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <span className={`inline-flex px-2 py-1 text-xs font-semibold rounded-full ${getStatusColor(entry.status)}`}>
                        {entry.status}
                      </span>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                      {formatDate(entry.created_at)}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm font-medium">
                      <div className="flex space-x-2">
                        <button
                          onClick={() => handleViewEntry(entry.id)}
                          className="text-blue-600 hover:text-blue-900"
                          title="View Details"
                        >
                          <Eye className="h-4 w-4" />
                        </button>
                        <button
                          onClick={() => handleEditEntry(entry)}
                          className="text-indigo-600 hover:text-indigo-900"
                          title="Edit Entry"
                        >
                          <Edit className="h-4 w-4" />
                        </button>
                        {entry.status === 'ACTIVE' && (
                          <button
                            onClick={() => handleScheduleEntry(entry.id)}
                            className="text-green-600 hover:text-green-900"
                            title="Schedule"
                          >
                            <Calendar className="h-4 w-4" />
                          </button>
                        )}
                        <button
                          onClick={() => handleDeleteEntry(entry.id)}
                          className="text-red-600 hover:text-red-900"
                          title="Delete Entry"
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

      {/* Waitlist Form Modal */}
      <WaitlistForm
        entry={editingEntry}
        onSubmit={editingEntry ? handleUpdateEntry : handleCreateEntry}
        onCancel={() => {
          setShowForm(false);
          setEditingEntry(null);
        }}
        isOpen={showForm}
      />

      {/* Waitlist Details Modal */}
      {showDetails && selectedEntry && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-white rounded-lg shadow-xl w-full max-w-2xl max-h-[90vh] overflow-y-auto">
            <div className="flex items-center justify-between p-6 border-b">
              <div className="flex items-center space-x-2">
                <Clock className="h-5 w-5 text-orange-600" />
                <h2 className="text-xl font-semibold text-gray-900">Waitlist Entry Details</h2>
              </div>
              <button
                onClick={() => {
                  setShowDetails(false);
                  setSelectedEntry(null);
                }}
                className="text-gray-400 hover:text-gray-600 transition-colors"
              >
                <X className="h-5 w-5" />
              </button>
            </div>
            <div className="p-6 space-y-4">
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700">Patient</label>
                  <p className="text-sm text-gray-900">{selectedEntry.patient_name || 'Not specified'}</p>
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700">Practitioner</label>
                  <p className="text-sm text-gray-900">{selectedEntry.practitioner_name || 'Not specified'}</p>
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700">Service Type</label>
                  <p className="text-sm text-gray-900">{getServiceTypeDisplay(selectedEntry.service_type)}</p>
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700">Priority</label>
                  <span className={`inline-flex px-2 py-1 text-xs font-semibold rounded-full ${getPriorityColor(selectedEntry.priority)}`}>
                    {selectedEntry.priority}
                  </span>
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700">Status</label>
                  <span className={`inline-flex px-2 py-1 text-xs font-semibold rounded-full ${getStatusColor(selectedEntry.status)}`}>
                    {selectedEntry.status}
                  </span>
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700">Created</label>
                  <p className="text-sm text-gray-900">{formatDate(selectedEntry.created_at)}</p>
                </div>
              </div>
              
              {/* Preferred Dates */}
              {selectedEntry.preferred_dates && selectedEntry.preferred_dates.length > 0 && (
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">Preferred Dates</label>
                  <div className="flex flex-wrap gap-2">
                    {selectedEntry.preferred_dates.map((date, index) => (
                      <span key={index} className="px-2 py-1 bg-blue-100 text-blue-800 text-xs rounded">
                        {formatDate(date)}
                      </span>
                    ))}
                  </div>
                </div>
              )}
              
              {/* Preferred Times */}
              {selectedEntry.preferred_times && selectedEntry.preferred_times.length > 0 && (
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">Preferred Times</label>
                  <div className="flex flex-wrap gap-2">
                    {selectedEntry.preferred_times.map((time, index) => (
                      <span key={index} className="px-2 py-1 bg-green-100 text-green-800 text-xs rounded">
                        {formatTime(time)}
                      </span>
                    ))}
                  </div>
                </div>
              )}
              
              {/* Notes */}
              {selectedEntry.notes && (
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">Notes</label>
                  <p className="text-sm text-gray-900 bg-gray-50 p-3 rounded">{selectedEntry.notes}</p>
                </div>
              )}
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default WaitlistManagement; 