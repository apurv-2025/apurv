import React, { useState, useEffect } from 'react';
import { Search, Filter, Clock, User, AlertCircle, CheckCircle, XCircle, Play, Pause } from 'lucide-react';
import { claimsService } from '../services/claimsService';
import { formatDate, formatCurrency } from '../utils/helpers';
import LoadingSpinner from '../components/ui/LoadingSpinner';
import StatusBadge from '../components/ui/StatusBadge';
import ClaimTypeBadge from '../components/ui/ClaimTypeBadge';

const WorkQueuePage = () => {
  const [workQueueItems, setWorkQueueItems] = useState([]);
  const [summary, setSummary] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [searchTerm, setSearchTerm] = useState('');
  const [statusFilter, setStatusFilter] = useState('');
  const [assigneeFilter, setAssigneeFilter] = useState('');
  const [priorityFilter, setPriorityFilter] = useState('');
  const [showAssignmentModal, setShowAssignmentModal] = useState(false);
  const [showAgentAssignmentModal, setShowAgentAssignmentModal] = useState(false);
  const [selectedClaim, setSelectedClaim] = useState(null);
  const [selectedWorkQueueItem, setSelectedWorkQueueItem] = useState(null);
  const [availableAgents, setAvailableAgents] = useState([]);

  useEffect(() => {
    fetchWorkQueueData();
    fetchAvailableAgents();
  }, []);

  const fetchAvailableAgents = async () => {
    try {
      const data = await claimsService.getAvailableAgents();
      setAvailableAgents(data.agents || []);
    } catch (error) {
      console.error('Error fetching available agents:', error);
    }
  };

  const fetchWorkQueueData = async () => {
    try {
      setLoading(true);
      setError(null);
      
      const [itemsData, summaryData] = await Promise.all([
        claimsService.getWorkQueue(),
        claimsService.getWorkQueueSummary()
      ]);
      
      setWorkQueueItems(itemsData);
      setSummary(summaryData);
    } catch (error) {
      console.error('Error fetching work queue data:', error);
      setError(error.message);
    } finally {
      setLoading(false);
    }
  };

  const handleAssignClaim = async (claimId, assignment) => {
    try {
      await claimsService.assignClaimToWorkQueue(claimId, assignment);
      await fetchWorkQueueData(); // Refresh data
      setShowAssignmentModal(false);
      setSelectedClaim(null);
    } catch (error) {
      console.error('Error assigning claim:', error);
      alert('Failed to assign claim: ' + error.message);
    }
  };

  const handleUpdateWorkQueueItem = async (workQueueId, update) => {
    try {
      await claimsService.updateWorkQueueItem(workQueueId, update);
      await fetchWorkQueueData(); // Refresh data
    } catch (error) {
      console.error('Error updating work queue item:', error);
      alert('Failed to update work queue item: ' + error.message);
    }
  };

  const handleAssignToAgent = async (workQueueId, agentId, taskType) => {
    try {
      await claimsService.assignWorkQueueToAgent(workQueueId, agentId, taskType);
      await fetchWorkQueueData(); // Refresh data
      setShowAgentAssignmentModal(false);
      setSelectedWorkQueueItem(null);
      alert('Successfully assigned to agent!');
    } catch (error) {
      console.error('Error assigning to agent:', error);
      alert('Failed to assign to agent: ' + error.message);
    }
  };

  const getStatusIcon = (status) => {
    switch (status) {
      case 'PENDING':
        return <Clock className="w-4 h-4 text-yellow-500" />;
      case 'ASSIGNED':
        return <User className="w-4 h-4 text-blue-500" />;
      case 'IN_PROGRESS':
        return <Play className="w-4 h-4 text-green-500" />;
      case 'COMPLETED':
        return <CheckCircle className="w-4 h-4 text-green-600" />;
      case 'FAILED':
        return <XCircle className="w-4 h-4 text-red-500" />;
      case 'CANCELLED':
        return <XCircle className="w-4 h-4 text-gray-500" />;
      default:
        return <AlertCircle className="w-4 h-4 text-gray-500" />;
    }
  };

  const getPriorityColor = (priority) => {
    switch (priority) {
      case 'URGENT':
        return 'bg-red-100 text-red-800 border-red-200';
      case 'HIGH':
        return 'bg-orange-100 text-orange-800 border-orange-200';
      case 'MEDIUM':
        return 'bg-yellow-100 text-yellow-800 border-yellow-200';
      case 'LOW':
        return 'bg-green-100 text-green-800 border-green-200';
      default:
        return 'bg-gray-100 text-gray-800 border-gray-200';
    }
  };

  const filteredItems = workQueueItems.filter(item => {
    const matchesSearch = item.patient_name.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         item.claim_number.toLowerCase().includes(searchTerm.toLowerCase());
    const matchesStatus = !statusFilter || item.status === statusFilter;
    const matchesAssignee = !assigneeFilter || item.assigned_to === assigneeFilter;
    const matchesPriority = !priorityFilter || item.priority === priorityFilter;
    
    return matchesSearch && matchesStatus && matchesAssignee && matchesPriority;
  });

  if (loading) {
    return <LoadingSpinner fullPage text="Loading work queue..." />;
  }

  if (error) {
    return (
      <div className="text-center py-12">
        <div className="text-red-600 mb-4">Error loading work queue</div>
        <p className="text-gray-600">{error}</p>
        <button 
          onClick={fetchWorkQueueData} 
          className="mt-4 px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600"
        >
          Retry
        </button>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex justify-between items-center">
        <h1 className="text-2xl font-bold text-gray-900">Work Queue</h1>
        <button
          onClick={() => setShowAssignmentModal(true)}
          className="px-4 py-2 bg-blue-500 text-white rounded-md hover:bg-blue-600 transition-colors"
        >
          Assign Claim
        </button>
      </div>

      {/* Summary Cards */}
      {summary && (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
          <div className="bg-white p-4 rounded-lg shadow">
            <div className="text-sm font-medium text-gray-500">Total Items</div>
            <div className="text-2xl font-bold text-gray-900">{summary.total_items}</div>
          </div>
          <div className="bg-white p-4 rounded-lg shadow">
            <div className="text-sm font-medium text-gray-500">In Progress</div>
            <div className="text-2xl font-bold text-blue-600">{summary.in_progress}</div>
          </div>
          <div className="bg-white p-4 rounded-lg shadow">
            <div className="text-sm font-medium text-gray-500">Pending</div>
            <div className="text-2xl font-bold text-yellow-600">{summary.pending}</div>
          </div>
          <div className="bg-white p-4 rounded-lg shadow">
            <div className="text-sm font-medium text-gray-500">Completed</div>
            <div className="text-2xl font-bold text-green-600">{summary.completed}</div>
          </div>
        </div>
      )}

      {/* Filters */}
      <div className="bg-white p-6 rounded-lg shadow">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
          <div>
            <div className="relative">
              <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-4 h-4" />
              <input
                type="text"
                placeholder="Search by patient or claim..."
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                className="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              />
            </div>
          </div>
          <div>
            <select
              value={statusFilter}
              onChange={(e) => setStatusFilter(e.target.value)}
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            >
              <option value="">All Statuses</option>
              <option value="PENDING">Pending</option>
              <option value="ASSIGNED">Assigned</option>
              <option value="IN_PROGRESS">In Progress</option>
              <option value="COMPLETED">Completed</option>
              <option value="FAILED">Failed</option>
              <option value="CANCELLED">Cancelled</option>
            </select>
          </div>
          <div>
            <select
              value={priorityFilter}
              onChange={(e) => setPriorityFilter(e.target.value)}
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            >
              <option value="">All Priorities</option>
              <option value="URGENT">Urgent</option>
              <option value="HIGH">High</option>
              <option value="MEDIUM">Medium</option>
              <option value="LOW">Low</option>
            </select>
          </div>
          <div>
            <select
              value={assigneeFilter}
              onChange={(e) => setAssigneeFilter(e.target.value)}
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            >
              <option value="">All Assignees</option>
              {summary?.by_assignee && Object.keys(summary.by_assignee).map(assignee => (
                <option key={assignee} value={assignee}>{assignee}</option>
              ))}
            </select>
          </div>
        </div>
      </div>

      {/* Work Queue Table */}
      <div className="bg-white shadow rounded-lg overflow-hidden">
        <div className="overflow-x-auto">
          <table className="min-w-full divide-y divide-gray-200">
            <thead className="bg-gray-50">
              <tr>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Status
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Claim
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Patient
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Assigned To
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Priority
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Assigned
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Est. Completion
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Actions
                </th>
              </tr>
            </thead>
            <tbody className="bg-white divide-y divide-gray-200">
              {filteredItems.map((item) => (
                <tr key={item.id} className="hover:bg-gray-50">
                  <td className="px-6 py-4 whitespace-nowrap">
                    <div className="flex items-center">
                      {getStatusIcon(item.status)}
                      <span className="ml-2 text-sm font-medium text-gray-900 capitalize">
                        {item.status.replace('_', ' ')}
                      </span>
                    </div>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap">
                    <div className="flex items-center">
                      <div>
                        <div className="text-sm font-medium text-gray-900">
                          {item.claim_number}
                        </div>
                        <div className="flex items-center mt-1">
                          <ClaimTypeBadge type={item.claim_type} />
                          <StatusBadge status={item.claim_status} className="ml-2" />
                        </div>
                      </div>
                    </div>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap">
                    <div className="text-sm text-gray-900">{item.patient_name}</div>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap">
                    <div className="text-sm text-gray-900">{item.assigned_to}</div>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap">
                    <span className={`inline-flex px-2 py-1 text-xs font-semibold rounded-full border ${getPriorityColor(item.priority)}`}>
                      {item.priority}
                    </span>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                    {formatDate(item.assigned_at)}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                    {item.estimated_completion ? formatDate(item.estimated_completion) : 'Not set'}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm font-medium">
                    <button
                      onClick={() => {
                        setSelectedClaim(item);
                        setShowAssignmentModal(true);
                      }}
                      className="text-blue-600 hover:text-blue-900 mr-3"
                    >
                      Update
                    </button>
                                         <button
                       onClick={() => handleUpdateWorkQueueItem(item.id, { status: 'IN_PROGRESS' })}
                       className="text-green-600 hover:text-green-900 mr-2"
                     >
                       Start
                     </button>
                     <button
                       onClick={() => {
                         setSelectedWorkQueueItem(item);
                         setShowAgentAssignmentModal(true);
                       }}
                       className="text-purple-600 hover:text-purple-900"
                       disabled={item.assigned_to.startsWith('agent-') || item.assigned_to.startsWith('ai-')}
                     >
                       Assign
                     </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
        
        {filteredItems.length === 0 && (
          <div className="text-center py-12">
            <div className="text-gray-500">No work queue items found</div>
          </div>
        )}
      </div>

      {/* Assignment Modal */}
      {showAssignmentModal && (
        <AssignmentModal
          claim={selectedClaim}
          onAssign={handleAssignClaim}
          onUpdate={handleUpdateWorkQueueItem}
          onClose={() => {
            setShowAssignmentModal(false);
            setSelectedClaim(null);
          }}
        />
      )}

      {/* Agent Assignment Modal */}
      {showAgentAssignmentModal && (
        <AgentAssignmentModal
          workQueueItem={selectedWorkQueueItem}
          availableAgents={availableAgents}
          onAssign={handleAssignToAgent}
          onClose={() => {
            setShowAgentAssignmentModal(false);
            setSelectedWorkQueueItem(null);
          }}
        />
      )}
    </div>
  );
};

// Assignment Modal Component
const AssignmentModal = ({ claim, onAssign, onUpdate, onClose }) => {
  const [formData, setFormData] = useState({
         assigned_to: claim?.assigned_to || '',
     priority: claim?.priority || 'MEDIUM',
     estimated_completion: claim?.estimated_completion ? new Date(claim.estimated_completion).toISOString().split('T')[0] : '',
     work_notes: claim?.work_notes || '',
     status: claim?.status || 'ASSIGNED'
  });

  const handleSubmit = (e) => {
    e.preventDefault();
    
    if (claim) {
      // Update existing work queue item
      onUpdate(claim.id, formData);
    } else {
      // Assign new claim to work queue
      onAssign(1, formData); // TODO: Get claim ID from selection
    }
  };

  return (
    <div className="fixed inset-0 bg-gray-600 bg-opacity-50 overflow-y-auto h-full w-full z-50">
      <div className="relative top-20 mx-auto p-5 border w-96 shadow-lg rounded-md bg-white">
        <div className="mt-3">
          <h3 className="text-lg font-medium text-gray-900 mb-4">
            {claim ? 'Update Work Queue Item' : 'Assign Claim to Work Queue'}
          </h3>
          
          <form onSubmit={handleSubmit} className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-gray-700">Assigned To</label>
              <input
                type="text"
                value={formData.assigned_to}
                onChange={(e) => setFormData({...formData, assigned_to: e.target.value})}
                className="mt-1 block w-full border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-blue-500 focus:border-blue-500"
                required
              />
            </div>
            
            <div>
              <label className="block text-sm font-medium text-gray-700">Priority</label>
              <select
                value={formData.priority}
                onChange={(e) => setFormData({...formData, priority: e.target.value})}
                className="mt-1 block w-full border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-blue-500 focus:border-blue-500"
              >
                                 <option value="LOW">Low</option>
                 <option value="MEDIUM">Medium</option>
                 <option value="HIGH">High</option>
                 <option value="URGENT">Urgent</option>
              </select>
            </div>
            
            <div>
              <label className="block text-sm font-medium text-gray-700">Status</label>
              <select
                value={formData.status}
                onChange={(e) => setFormData({...formData, status: e.target.value})}
                className="mt-1 block w-full border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-blue-500 focus:border-blue-500"
              >
                                 <option value="PENDING">Pending</option>
                 <option value="ASSIGNED">Assigned</option>
                 <option value="IN_PROGRESS">In Progress</option>
                 <option value="COMPLETED">Completed</option>
                 <option value="FAILED">Failed</option>
                 <option value="CANCELLED">Cancelled</option>
              </select>
            </div>
            
            <div>
              <label className="block text-sm font-medium text-gray-700">Estimated Completion</label>
              <input
                type="date"
                value={formData.estimated_completion}
                onChange={(e) => setFormData({...formData, estimated_completion: e.target.value})}
                className="mt-1 block w-full border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-blue-500 focus:border-blue-500"
              />
            </div>
            
            <div>
              <label className="block text-sm font-medium text-gray-700">Work Notes</label>
              <textarea
                value={formData.work_notes}
                onChange={(e) => setFormData({...formData, work_notes: e.target.value})}
                rows={3}
                className="mt-1 block w-full border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-blue-500 focus:border-blue-500"
              />
            </div>
            
            <div className="flex justify-end space-x-3 pt-4">
              <button
                type="button"
                onClick={onClose}
                className="px-4 py-2 text-sm font-medium text-gray-700 bg-gray-100 border border-gray-300 rounded-md hover:bg-gray-200"
              >
                Cancel
              </button>
              <button
                type="submit"
                className="px-4 py-2 text-sm font-medium text-white bg-blue-600 border border-transparent rounded-md hover:bg-blue-700"
              >
                {claim ? 'Update' : 'Assign'}
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  );
};

// Agent Assignment Modal Component
const AgentAssignmentModal = ({ workQueueItem, availableAgents, onAssign, onClose }) => {
  const [selectedAgent, setSelectedAgent] = useState('');
  const [selectedTaskType, setSelectedTaskType] = useState('process_claim');

  const handleSubmit = (e) => {
    e.preventDefault();
    if (selectedAgent && workQueueItem) {
      onAssign(workQueueItem.id, selectedAgent, selectedTaskType);
    }
  };

  const taskTypes = [
    { value: 'process_claim', label: 'Process Claim' },
    { value: 'validate_claim', label: 'Validate Claim' },
    { value: 'analyze_rejection', label: 'Analyze Rejection' },
    { value: 'reconcile_payment', label: 'Reconcile Payment' },
    { value: 'generate_report', label: 'Generate Report' }
  ];

  return (
    <div className="fixed inset-0 bg-gray-600 bg-opacity-50 overflow-y-auto h-full w-full z-50">
      <div className="relative top-20 mx-auto p-5 border w-96 shadow-lg rounded-md bg-white">
        <div className="mt-3">
          <h3 className="text-lg font-medium text-gray-900 mb-4">
            Assign to Agent
          </h3>
          
          {workQueueItem && (
            <div className="mb-4 p-3 bg-gray-50 rounded">
              <p className="text-sm text-gray-600">
                <strong>Claim:</strong> {workQueueItem.claim_number}
              </p>
              <p className="text-sm text-gray-600">
                <strong>Patient:</strong> {workQueueItem.patient_name}
              </p>
              <p className="text-sm text-gray-600">
                <strong>Priority:</strong> {workQueueItem.priority}
              </p>
            </div>
          )}
          
          <form onSubmit={handleSubmit} className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-gray-700">Select Agent</label>
              <select
                value={selectedAgent}
                onChange={(e) => setSelectedAgent(e.target.value)}
                className="mt-1 block w-full border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-blue-500 focus:border-blue-500"
                required
              >
                <option value="">Choose an agent...</option>
                {availableAgents.map(agent => (
                  <option key={agent.id} value={agent.id}>
                    {agent.name} - {agent.description}
                  </option>
                ))}
              </select>
            </div>
            
            <div>
              <label className="block text-sm font-medium text-gray-700">Task Type</label>
              <select
                value={selectedTaskType}
                onChange={(e) => setSelectedTaskType(e.target.value)}
                className="mt-1 block w-full border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-blue-500 focus:border-blue-500"
              >
                {taskTypes.map(taskType => (
                  <option key={taskType.value} value={taskType.value}>
                    {taskType.label}
                  </option>
                ))}
              </select>
            </div>
            
            <div className="flex justify-end space-x-3 pt-4">
              <button
                type="button"
                onClick={onClose}
                className="px-4 py-2 text-sm font-medium text-gray-700 bg-gray-100 border border-gray-300 rounded-md hover:bg-gray-200"
              >
                Cancel
              </button>
                             <button
                 type="submit"
                 className="px-4 py-2 text-sm font-medium text-white bg-purple-600 border border-transparent rounded-md hover:bg-purple-700"
               >
                 Assign
               </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  );
};

export default WorkQueuePage; 