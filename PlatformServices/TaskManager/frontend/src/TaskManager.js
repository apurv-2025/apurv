import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Clock, Play, Trash2, Plus, RefreshCw, CheckCircle, XCircle, AlertCircle, Calendar, User, Mail, MessageSquare, Webhook } from 'lucide-react';

const TaskManager = () => {
  const [tasks, setTasks] = useState([]);
  const [executions, setExecutions] = useState([]);
  const [loading, setLoading] = useState(false);
  const [selectedTask, setSelectedTask] = useState(null);
  const [showCreateForm, setShowCreateForm] = useState(false);
  const [error, setError] = useState(null);
  const [newTask, setNewTask] = useState({
    name: '',
    description: '',
    task_type: 'email',
    scheduled_time: '',
    payload: '{}',
    callback_url: ''
  });

  // API base URL - in production, this would come from env
  const API_BASE = process.env.REACT_APP_API_URL || 'http://localhost:8000/api';

  // Fetch tasks
  const fetchTasks = async () => {
    try {
      setLoading(true);
      setError(null);
      const response = await axios.get(`${API_BASE}/tasks/`);
      setTasks(response.data);
    } catch (error) {
      console.error('Error fetching tasks:', error);
      setError('Failed to fetch tasks. Please check if the API server is running.');
    } finally {
      setLoading(false);
    }
  };

  // Fetch executions for selected task
  const fetchExecutions = async (taskId) => {
    try {
      const response = await axios.get(`${API_BASE}/tasks/${taskId}/executions`);
      setExecutions(response.data);
    } catch (error) {
      console.error('Error fetching executions:', error);
      setError('Failed to fetch execution history.');
    }
  };

  // Create new task
  const createTask = async () => {
    try {
      setError(null);
      let payload;
      try {
        payload = JSON.parse(newTask.payload);
      } catch (e) {
        setError('Invalid JSON in payload');
        return;
      }

      const taskData = {
        ...newTask,
        payload,
        scheduled_time: new Date(newTask.scheduled_time).toISOString()
      };

      const response = await axios.post(`${API_BASE}/tasks/`, taskData);

      setShowCreateForm(false);
      setNewTask({
        name: '',
        description: '',
        task_type: 'email',
        scheduled_time: '',
        payload: '{}',
        callback_url: ''
      });
      fetchTasks();
    } catch (error) {
      console.error('Error creating task:', error);
      setError(error.message);
    }
  };

  // Execute task now
  const executeTask = async (taskId) => {
    try {
      setError(null);
      await axios.post(`${API_BASE}/tasks/${taskId}/execute`);
      fetchTasks();
    } catch (error) {
      console.error('Error executing task:', error);
      setError('Failed to execute task.');
    }
  };

  // Delete task
  const deleteTask = async (taskId) => {
    try {
      setError(null);
      await axios.delete(`${API_BASE}/tasks/${taskId}`);
      fetchTasks();
      if (selectedTask?.id === taskId) {
        setSelectedTask(null);
        setExecutions([]);
      }
    } catch (error) {
      console.error('Error deleting task:', error);
      setError('Failed to delete task.');
    }
  };

  // Get status icon
  const getStatusIcon = (status) => {
    switch (status) {
      case 'completed':
        return <CheckCircle className="w-5 h-5 text-green-500" />;
      case 'failed':
        return <XCircle className="w-5 h-5 text-red-500" />;
      case 'running':
        return <RefreshCw className="w-5 h-5 text-blue-500 animate-spin" />;
      default:
        return <Clock className="w-5 h-5 text-yellow-500" />;
    }
  };

  // Get task type icon
  const getTaskTypeIcon = (taskType) => {
    switch (taskType) {
      case 'email':
        return <Mail className="w-4 h-4" />;
      case 'sms':
        return <MessageSquare className="w-4 h-4" />;
      case 'webhook':
        return <Webhook className="w-4 h-4" />;
      case 'reminder':
        return <AlertCircle className="w-4 h-4" />;
      default:
        return <Clock className="w-4 h-4" />;
    }
  };

  // Get status color
  const getStatusColor = (status) => {
    switch (status) {
      case 'completed':
        return 'bg-green-100 text-green-800';
      case 'failed':
        return 'bg-red-100 text-red-800';
      case 'running':
        return 'bg-blue-100 text-blue-800';
      default:
        return 'bg-yellow-100 text-yellow-800';
    }
  };

  // Sample payload templates
  const payloadTemplates = {
    email: {
      to_email: "patient@example.com",
      subject: "Appointment Reminder",
      body: "Dear Patient, this is a reminder of your appointment tomorrow at 2:00 PM with Dr. Smith. Please arrive 15 minutes early."
    },
    sms: {
      phone_number: "+1234567890",
      message: "Reminder: You have an appointment tomorrow at 2:00 PM with Dr. Smith."
    },
    webhook: {
      url: "https://api.example.com/notify",
      method: "POST",
      data: { 
        message: "Task completed",
        patient_id: "12345",
        appointment_date: "2024-12-25"
      },
      headers: {
        "Authorization": "Bearer your-token"
      }
    },
    reminder: {
      type: "email",
      recipient: "patient@example.com",
      message: "Your lab results are ready for pickup. Please call us at (555) 123-4567 to schedule a time."
    }
  };

  // Format date for datetime-local input
  const formatDateForInput = () => {
    const now = new Date();
    now.setMinutes(now.getMinutes() - now.getTimezoneOffset());
    return now.toISOString().slice(0, 16);
  };

  useEffect(() => {
    fetchTasks();
  }, []);

  useEffect(() => {
    if (selectedTask) {
      fetchExecutions(selectedTask.id);
    }
  }, [selectedTask]);

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="max-w-7xl mx-auto px-4 py-8">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900">Task Manager</h1>
          <p className="text-gray-600 mt-2">Schedule and monitor task execution for medical practices and AI agents</p>
        </div>

        {/* Error Banner */}
        {error && (
          <div className="mb-6 bg-red-50 border border-red-200 rounded-lg p-4">
            <div className="flex">
              <XCircle className="w-5 h-5 text-red-400 mt-0.5 mr-3" />
              <div>
                <h3 className="text-sm font-medium text-red-800">Error</h3>
                <p className="text-sm text-red-700 mt-1">{error}</p>
                <button 
                  onClick={() => setError(null)}
                  className="text-sm text-red-600 underline mt-2"
                >
                  Dismiss
                </button>
              </div>
            </div>
          </div>
        )}

        {/* Stats Cards */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
          <div className="bg-white rounded-lg shadow-sm border p-6">
            <div className="flex items-center">
              <div className="p-2 bg-blue-100 rounded-lg">
                <Calendar className="w-6 h-6 text-blue-600" />
              </div>
              <div className="ml-4">
                <p className="text-sm font-medium text-gray-600">Total Tasks</p>
                <p className="text-2xl font-semibold text-gray-900">{tasks.length}</p>
              </div>
            </div>
          </div>
          
          <div className="bg-white rounded-lg shadow-sm border p-6">
            <div className="flex items-center">
              <div className="p-2 bg-yellow-100 rounded-lg">
                <Clock className="w-6 h-6 text-yellow-600" />
              </div>
              <div className="ml-4">
                <p className="text-sm font-medium text-gray-600">Pending</p>
                <p className="text-2xl font-semibold text-gray-900">
                  {tasks.filter(t => t.status === 'pending').length}
                </p>
              </div>
            </div>
          </div>
          
          <div className="bg-white rounded-lg shadow-sm border p-6">
            <div className="flex items-center">
              <div className="p-2 bg-green-100 rounded-lg">
                <CheckCircle className="w-6 h-6 text-green-600" />
              </div>
              <div className="ml-4">
                <p className="text-sm font-medium text-gray-600">Completed</p>
                <p className="text-2xl font-semibold text-gray-900">
                  {tasks.filter(t => t.status === 'completed').length}
                </p>
              </div>
            </div>
          </div>
          
          <div className="bg-white rounded-lg shadow-sm border p-6">
            <div className="flex items-center">
              <div className="p-2 bg-red-100 rounded-lg">
                <XCircle className="w-6 h-6 text-red-600" />
              </div>
              <div className="ml-4">
                <p className="text-sm font-medium text-gray-600">Failed</p>
                <p className="text-2xl font-semibold text-gray-900">
                  {tasks.filter(t => t.status === 'failed').length}
                </p>
              </div>
            </div>
          </div>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Tasks List */}
          <div className="lg:col-span-2">
            <div className="bg-white rounded-lg shadow-sm border">
              <div className="px-6 py-4 border-b border-gray-200 flex justify-between items-center">
                <h2 className="text-xl font-semibold text-gray-900">Tasks</h2>
                <div className="flex space-x-3">
                  <button
                    onClick={fetchTasks}
                    className="inline-flex items-center px-3 py-2 border border-gray-300 rounded-lg text-sm font-medium text-gray-700 bg-white hover:bg-gray-50"
                  >
                    <RefreshCw className="w-4 h-4 mr-2" />
                    Refresh
                  </button>
                  <button
                    onClick={() => setShowCreateForm(true)}
                    className="inline-flex items-center px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700"
                  >
                    <Plus className="w-4 h-4 mr-2" />
                    New Task
                  </button>
                </div>
              </div>

              <div className="divide-y divide-gray-200">
                {loading ? (
                  <div className="p-6 text-center">
                    <RefreshCw className="w-6 h-6 animate-spin mx-auto mb-2 text-blue-500" />
                    <p>Loading tasks...</p>
                  </div>
                ) : tasks.length === 0 ? (
                  <div className="p-6 text-center text-gray-500">
                    <Calendar className="w-12 h-12 mx-auto mb-4 text-gray-300" />
                    <p className="text-lg font-medium">No tasks found</p>
                    <p>Create your first task to get started!</p>
                  </div>
                ) : (
                  tasks.map((task) => (
                    <div
                      key={task.id}
                      className={`p-6 cursor-pointer hover:bg-gray-50 task-card ${
                        selectedTask?.id === task.id ? 'bg-blue-50 border-l-4 border-blue-500' : ''
                      }`}
                      onClick={() => setSelectedTask(task)}
                    >
                      <div className="flex items-center justify-between">
                        <div className="flex items-center space-x-3">
                          {getStatusIcon(task.status)}
                          <div className="flex items-center space-x-2">
                            {getTaskTypeIcon(task.task_type)}
                            <div>
                              <h3 className="text-lg font-medium text-gray-900">{task.name}</h3>
                              <p className="text-sm text-gray-500">{task.description}</p>
                            </div>
                          </div>
                        </div>
                        <div className="flex items-center space-x-2">
                          <span className={`px-2 py-1 rounded-full text-xs font-medium ${getStatusColor(task.status)}`}>
                            {task.status}
                          </span>
                          <button
                            onClick={(e) => {
                              e.stopPropagation();
                              executeTask(task.id);
                            }}
                            className="p-1 text-blue-600 hover:text-blue-800 hover:bg-blue-100 rounded"
                            title="Execute Now"
                          >
                            <Play className="w-4 h-4" />
                          </button>
                          <button
                            onClick={(e) => {
                              e.stopPropagation();
                              if (window.confirm('Are you sure you want to delete this task?')) {
                                deleteTask(task.id);
                              }
                            }}
                            className="p-1 text-red-600 hover:text-red-800 hover:bg-red-100 rounded"
                            title="Delete"
                          >
                            <Trash2 className="w-4 h-4" />
                          </button>
                        </div>
                      </div>
                      <div className="mt-3 grid grid-cols-2 gap-4 text-sm text-gray-600">
                        <div>
                          <span className="font-medium">Type:</span> {task.task_type}
                        </div>
                        <div>
                          <span className="font-medium">Scheduled:</span> {new Date(task.scheduled_time).toLocaleString()}
                        </div>
                        <div>
                          <span className="font-medium">Created:</span> {new Date(task.created_at).toLocaleString()}
                        </div>
                        <div>
                          <span className="font-medium">Retries:</span> {task.retry_count}/{task.max_retries}
                        </div>
                      </div>
                    </div>
                  ))
                )}
              </div>
            </div>
          </div>

          {/* Task Details & Executions */}
          <div className="space-y-6">
            {selectedTask ? (
              <>
                <div className="bg-white rounded-lg shadow-sm border">
                  <div className="px-6 py-4 border-b border-gray-200">
                    <h3 className="text-lg font-semibold text-gray-900">Task Details</h3>
                  </div>
                  <div className="p-6 space-y-4">
                    <div>
                      <label className="block text-sm font-medium text-gray-700">Name</label>
                      <p className="text-gray-900">{selectedTask.name}</p>
                    </div>
                    <div>
                      <label className="block text-sm font-medium text-gray-700">Type</label>
                      <div className="flex items-center space-x-2">
                        {getTaskTypeIcon(selectedTask.task_type)}
                        <span className="text-gray-900">{selectedTask.task_type}</span>
                      </div>
                    </div>
                    <div>
                      <label className="block text-sm font-medium text-gray-700">Status</label>
                      <span className={`px-2 py-1 rounded-full text-xs font-medium ${getStatusColor(selectedTask.status)}`}>
                        {selectedTask.status}
                      </span>
                    </div>
                    <div>
                      <label className="block text-sm font-medium text-gray-700">Payload</label>
                      <pre className="text-sm bg-gray-100 p-3 rounded overflow-auto">
                        {JSON.stringify(selectedTask.payload, null, 2)}
                      </pre>
                    </div>
                    <div>
                      <label className="block text-sm font-medium text-gray-700">Retry Count</label>
                      <p className="text-gray-900">{selectedTask.retry_count} / {selectedTask.max_retries}</p>
                    </div>
                    {selectedTask.callback_url && (
                      <div>
                        <label className="block text-sm font-medium text-gray-700">Callback URL</label>
                        <p className="text-gray-900 text-sm break-all">{selectedTask.callback_url}</p>
                      </div>
                    )}
                  </div>
                </div>

                <div className="bg-white rounded-lg shadow-sm border">
                  <div className="px-6 py-4 border-b border-gray-200">
                    <h3 className="text-lg font-semibold text-gray-900">Execution History</h3>
                  </div>
                  <div className="divide-y divide-gray-200">
                    {executions.length === 0 ? (
                      <div className="p-6 text-center text-gray-500">
                        <AlertCircle className="w-8 h-8 mx-auto mb-2 text-gray-300" />
                        <p>No executions yet</p>
                      </div>
                    ) : (
                      executions.map((execution) => (
                        <div key={execution.id} className="p-4">
                          <div className="flex items-center justify-between mb-2">
                            <div className="flex items-center space-x-2">
                              {getStatusIcon(execution.status)}
                              <span className={`px-2 py-1 rounded-full text-xs font-medium ${getStatusColor(execution.status)}`}>
                                {execution.status}
                              </span>
                            </div>
                            <div className="text-sm text-gray-500">
                              {new Date(execution.started_at).toLocaleString()}
                            </div>
                          </div>
                          {execution.error_message && (
                            <div className="mt-2 p-2 bg-red-50 border border-red-200 rounded text-red-700 text-sm">
                              <strong>Error:</strong> {execution.error_message}
                            </div>
                          )}
                          {execution.result && (
                            <div className="mt-2">
                              <label className="block text-xs font-medium text-gray-600">Result:</label>
                              <pre className="text-xs bg-gray-100 p-2 rounded overflow-auto">
                                {JSON.stringify(execution.result, null, 2)}
                              </pre>
                            </div>
                          )}
                          {execution.completed_at && (
                            <div className="mt-2 text-xs text-gray-500">
                              Completed: {new Date(execution.completed_at).toLocaleString()}
                            </div>
                          )}
                        </div>
                      ))
                    )}
                  </div>
                </div>
              </>
            ) : (
              <div className="bg-white rounded-lg shadow-sm border p-6 text-center text-gray-500">
                <User className="w-12 h-12 mx-auto mb-4 text-gray-300" />
                <p className="text-lg font-medium">Select a task</p>
                <p>Choose a task from the list to view details and execution history</p>
              </div>
            )}
          </div>
        </div>

        {/* Create Task Modal */}
        {showCreateForm && (
          <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
            <div className="bg-white rounded-lg max-w-2xl w-full max-h-[90vh] overflow-y-auto">
              <div className="px-6 py-4 border-b border-gray-200">
                <h3 className="text-lg font-semibold text-gray-900">Create New Task</h3>
              </div>
              <div className="p-6 space-y-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Name</label>
                  <input
                    type="text"
                    value={newTask.name}
                    onChange={(e) => setNewTask({ ...newTask, name: e.target.value })}
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                    placeholder="e.g., Send appointment reminder"
                    required
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Description</label>
                  <textarea
                    value={newTask.description}
                    onChange={(e) => setNewTask({ ...newTask, description: e.target.value })}
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                    rows="3"
                    placeholder="Optional description"
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Task Type</label>
                  <select
                    value={newTask.task_type}
                    onChange={(e) => {
                      const type = e.target.value;
                      setNewTask({ 
                        ...newTask, 
                        task_type: type,
                        payload: JSON.stringify(payloadTemplates[type], null, 2)
                      });
                    }}
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  >
                    <option value="email">📧 Email</option>
                    <option value="sms">📱 SMS</option>
                    <option value="webhook">🔗 Webhook</option>
                    <option value="reminder">⏰ Reminder</option>
                  </select>
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Scheduled Time</label>
                  <input
                    type="datetime-local"
                    value={newTask.scheduled_time || formatDateForInput()}
                    onChange={(e) => setNewTask({ ...newTask, scheduled_time: e.target.value })}
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                    required
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Payload (JSON)
                    <span className="text-gray-500 text-xs ml-2">
                      Template loaded based on task type
                    </span>
                  </label>
                  <textarea
                    value={newTask.payload}
                    onChange={(e) => setNewTask({ ...newTask, payload: e.target.value })}
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent font-mono text-sm"
                    rows="8"
                    placeholder="Enter JSON payload"
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Callback URL (Optional)
                  </label>
                  <input
                    type="url"
                    value={newTask.callback_url}
                    onChange={(e) => setNewTask({ ...newTask, callback_url: e.target.value })}
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                    placeholder="https://your-api.com/callback"
                  />
                </div>
              </div>

              <div className="px-6 py-4 border-t border-gray-200 flex justify-end space-x-3">
                <button
                  onClick={() => setShowCreateForm(false)}
                  className="px-4 py-2 text-gray-700 bg-gray-100 rounded-lg hover:bg-gray-200"
                >
                  Cancel
                </button>
                <button
                  onClick={createTask}
                  className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700"
                  disabled={!newTask.name || !newTask.scheduled_time}
                >
                  Create Task
                </button>
              </div>
            </div>
          </div>
        )}

        {/* API Usage Examples */}
        <div className="mt-12 bg-white rounded-lg shadow-sm border">
          <div className="px-6 py-4 border-b border-gray-200">
            <h3 className="text-lg font-semibold text-gray-900">API Usage Examples</h3>
          </div>
          <div className="p-6">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div>
                <h4 className="font-medium text-gray-900 mb-2">Create Email Reminder Task</h4>
                <pre className="text-sm bg-gray-900 text-gray-100 p-4 rounded overflow-auto">
{`POST /api/tasks/
{
  "name": "Appointment Reminder",
  "description": "Send email reminder to patient",
  "task_type": "email",
  "scheduled_time": "2024-12-25T09:00:00Z",
  "payload": {
    "to_email": "patient@example.com",
    "subject": "Appointment Reminder",
    "body": "Your appointment is tomorrow at 2 PM"
  },
  "callback_url": "https://your-api.com/callback"
}`}
                </pre>
              </div>

              <div>
                <h4 className="font-medium text-gray-900 mb-2">AI Agent Task Creation</h4>
                <pre className="text-sm bg-gray-900 text-gray-100 p-4 rounded overflow-auto">
{`# Python example for AI Agent
import requests
from datetime import datetime, timedelta

# Schedule a task 1 hour from now
scheduled_time = datetime.utcnow() + timedelta(hours=1)

task_data = {
    "name": "Patient Follow-up",
    "task_type": "sms",
    "scheduled_time": scheduled_time.isoformat() + "Z",
    "payload": {
        "phone_number": "+1234567890",
        "message": "How are you feeling after yesterday's visit?"
    },
    "callback_url": "https://ai-agent.com/task-complete"
}

response = requests.post(
    "${API_BASE}/tasks/",
    json=task_data
)`}
                </pre>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default TaskManager;
