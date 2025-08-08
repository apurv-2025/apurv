// src/components/Tasks/TasksView.jsx
import React, { useState, useEffect } from 'react';
import { Plus, Search } from 'lucide-react';
import TaskList from './TaskList';
import CreateTaskModal from './CreateTaskModal';
import TaskEmptyState from './TaskEmptyState';

// Mock data for development
const mockTasks = [
  {
    id: 1,
    name: 'Complete project proposal',
    description: 'Draft and finalize the Q4 project proposal for the new client',
    dueDate: '2024-12-25',
    dueTime: '14:00',
    priority: 'high',
    status: 'todo',
    clientId: 1,
    attachments: []
  },
  {
    id: 2,
    name: 'Review client feedback',
    description: 'Go through all client feedback and prepare response',
    dueDate: '2024-12-24',
    dueTime: '10:00',
    priority: 'medium',
    status: 'in_progress',
    clientId: 2,
    attachments: [{ id: 1, fileName: 'feedback.pdf' }]
  }
];

const mockClients = [
  { id: 1, name: 'John Doe', email: 'john@example.com', company: 'Acme Corp' },
  { id: 2, name: 'Jane Smith', email: 'jane@example.com', company: 'Tech Solutions' }
];

const TasksView = () => {
  const [isCreateModalOpen, setIsCreateModalOpen] = useState(false);
  const [searchQuery, setSearchQuery] = useState('');
  const [tasks, setTasks] = useState(mockTasks);
  const [clients] = useState(mockClients);
  const [selectedTask, setSelectedTask] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleCreateTask = async (taskData) => {
    setLoading(true);
    try {
      // Simulate API call
      const newTask = {
        id: tasks.length + 1,
        ...taskData,
        status: 'todo',
        attachments: []
      };
      setTasks(prev => [newTask, ...prev]);
      setIsCreateModalOpen(false);
    } catch (error) {
      console.error('Failed to create task:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleEditTask = async (taskData) => {
    setLoading(true);
    try {
      setTasks(prev => prev.map(task => 
        task.id === selectedTask.id ? { ...task, ...taskData } : task
      ));
      setIsCreateModalOpen(false);
      setSelectedTask(null);
    } catch (error) {
      console.error('Failed to update task:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleTaskEdit = (task) => {
    setSelectedTask(task);
    setIsCreateModalOpen(true);
  };

  const handleTaskDelete = async (taskId) => {
    if (window.confirm('Are you sure you want to delete this task?')) {
      setTasks(prev => prev.filter(task => task.id !== taskId));
    }
  };

  const handleTaskStatusChange = (taskId, updates) => {
    setTasks(prev => prev.map(task => 
      task.id === taskId ? { ...task, ...updates } : task
    ));
  };

  const handleModalClose = () => {
    setIsCreateModalOpen(false);
    setSelectedTask(null);
  };

  const filteredTasks = tasks.filter(task =>
    task.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
    task.description.toLowerCase().includes(searchQuery.toLowerCase())
  );

  const showEmptyState = !loading && tasks.length === 0;

  return (
    <div className="h-full flex flex-col bg-gray-50">
      {/* Header */}
      <div className="bg-white border-b border-gray-200 px-6 py-4">
        <div className="flex items-center justify-between">
          <h1 className="text-2xl font-semibold text-gray-900">Tasks</h1>
          
          <div className="flex items-center space-x-4">
            <div className="relative">
              <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 w-4 h-4 text-gray-400" />
              <input
                type="text"
                placeholder="Search tasks"
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                className="pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 w-64"
              />
            </div>
            
            {tasks.length > 0 && (
              <button
                onClick={() => setIsCreateModalOpen(true)}
                className="btn-primary flex items-center space-x-2"
              >
                <Plus className="w-4 h-4" />
                <span>Add task</span>
              </button>
            )}
          </div>
        </div>
      </div>

      {/* Content */}
      <div className="flex-1 overflow-auto">
        {showEmptyState ? (
          <TaskEmptyState onAddTask={() => setIsCreateModalOpen(true)} />
        ) : (
          <TaskList
            tasks={filteredTasks}
            loading={loading}
            clients={clients}
            onTaskEdit={handleTaskEdit}
            onTaskDelete={handleTaskDelete}
            onTaskStatusChange={handleTaskStatusChange}
          />
        )}
      </div>

      {/* Create/Edit Task Modal */}
      <CreateTaskModal
        isOpen={isCreateModalOpen}
        onClose={handleModalClose}
        onSave={selectedTask ? handleEditTask : handleCreateTask}
        clients={clients}
        initialTask={selectedTask}
        loading={loading}
      />
    </div>
  );
};

export default TasksView;
