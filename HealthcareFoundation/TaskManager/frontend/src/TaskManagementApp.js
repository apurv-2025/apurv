import React, { useState, useEffect } from 'react';
import { 
  CheckSquare, 
  Users, 
  Calendar, 
  Settings, 
  BarChart3,
  Search,
  Bell,
  Plus,
  Menu,
  X,
  Edit,
  Trash2,
  Upload,
  FileText,
  ChevronDown,
  MoreVertical,
  Circle,
  CheckCircle,
  Clock,
  User,
  Paperclip
} from 'lucide-react';

// Mock data and state management
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

const TaskManagementApp = () => {
  const [activeView, setActiveView] = useState('tasks');
  const [sidebarCollapsed, setSidebarCollapsed] = useState(false);
  const [isCreateModalOpen, setIsCreateModalOpen] = useState(false);
  const [searchQuery, setSearchQuery] = useState('');
  const [tasks, setTasks] = useState(mockTasks);
  const [clients, setClients] = useState(mockClients);
  const [selectedTask, setSelectedTask] = useState(null);
  const [notifications, setNotifications] = useState([]);

  // Sidebar component
  const Sidebar = () => {
    const navigationItems = [
      { id: 'tasks', label: 'Tasks', icon: CheckSquare },
      { id: 'clients', label: 'Clients', icon: Users },
      { id: 'calendar', label: 'Calendar', icon: Calendar },
      { id: 'analytics', label: 'Analytics', icon: BarChart3 },
      { id: 'settings', label: 'Settings', icon: Settings },
    ];

    return (
      <div className={`bg-white border-r border-gray-200 flex flex-col transition-all duration-300 ${
        sidebarCollapsed ? 'w-16' : 'w-64'
      }`}>
        <div className="p-4 border-b border-gray-200">
          <div className="flex items-center justify-between">
            {!sidebarCollapsed && (
              <div className="flex items-center space-x-2">
                <div className="w-8 h-8 bg-blue-600 rounded flex items-center justify-center">
                  <CheckSquare className="w-5 h-5 text-white" />
                </div>
                <span className="font-semibold text-gray-900">TaskManager</span>
              </div>
            )}
            <button
              onClick={() => setSidebarCollapsed(!sidebarCollapsed)}
              className="p-1 hover:bg-gray-100 rounded"
            >
              {sidebarCollapsed ? <Menu className="w-4 h-4" /> : <X className="w-4 h-4" />}
            </button>
          </div>
        </div>

        <nav className="flex-1 p-4">
          <ul className="space-y-2">
            {navigationItems.map((item) => {
              const Icon = item.icon;
              const isActive = activeView === item.id;
              
              return (
                <li key={item.id}>
                  <button
                    onClick={() => setActiveView(item.id)}
                    className={`w-full flex items-center space-x-3 px-3 py-2 rounded-lg text-sm font-medium transition-colors ${
                      isActive
                        ? 'bg-blue-50 text-blue-700'
                        : 'text-gray-600 hover:bg-gray-50'
                    }`}
                    title={sidebarCollapsed ? item.label : undefined}
                  >
                    <Icon className="w-5 h-5 flex-shrink-0" />
                    {!sidebarCollapsed && <span>{item.label}</span>}
                  </button>
                </li>
              );
            })}
          </ul>
        </nav>
      </div>
    );
  };

  // Header component
  const Header = () => (
    <header className="bg-white border-b border-gray-200 px-6 py-4">
      <div className="flex items-center justify-between">
        <div className="flex items-center space-x-4">
          <h1 className="text-2xl font-semibold text-gray-900 capitalize">
            {activeView}
          </h1>
        </div>

        <div className="flex items-center space-x-4">
          <div className="relative">
            <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 w-4 h-4 text-gray-400" />
            <input
              type="text"
              placeholder="Search..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 w-64"
            />
          </div>

          <button className="relative p-2 hover:bg-gray-100 rounded-lg">
            <Bell className="w-5 h-5 text-gray-600" />
            {notifications.length > 0 && (
              <span className="absolute top-1 right-1 w-2 h-2 bg-red-500 rounded-full"></span>
            )}
          </button>

          <div className="w-8 h-8 bg-blue-600 rounded-full flex items-center justify-center">
            <span className="text-white text-sm font-medium">JD</span>
          </div>
        </div>
      </div>
    </header>
  );

  // Task Card component
  const TaskCard = ({ task }) => {
    const getClientName = (clientId) => {
      const client = clients.find(c => c.id === clientId);
      return client ? client.name : null;
    };

    const getPriorityColor = (priority) => {
      const colors = {
        high: 'bg-red-100 text-red-600',
        medium: 'bg-yellow-100 text-yellow-600',
        low: 'bg-green-100 text-green-600',
        none: 'bg-gray-100 text-gray-600'
      };
      return colors[priority] || colors.none;
    };

    const handleStatusToggle = () => {
      setTasks(prev => prev.map(t => 
        t.id === task.id 
          ? { ...t, status: t.status === 'completed' ? 'todo' : 'completed' }
          : t
      ));
      
      addNotification(
        `Task "${task.name}" marked as ${task.status === 'completed' ? 'incomplete' : 'complete'}`,
        'success'
      );
    };

    const isOverdue = task.dueDate && new Date(`${task.dueDate}T${task.dueTime || '23:59'}`) < new Date() && task.status !== 'completed';

    return (
      <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-4 hover:shadow-md transition-shadow">
        <div className="flex items-start justify-between mb-3">
          <div className="flex items-start space-x-3 flex-1">
            <button
              onClick={handleStatusToggle}
              className="mt-0.5 text-gray-400 hover:text-blue-600 transition-colors"
            >
              {task.status === 'completed' ? (
                <CheckCircle className="w-5 h-5 text-green-600" />
              ) : (
                <Circle className="w-5 h-5" />
              )}
            </button>

            <div className="flex-1 min-w-0">
              <h3 className={`font-medium text-gray-900 truncate ${
                task.status === 'completed' ? 'line-through text-gray-500' : ''
              }`}>
                {task.name}
              </h3>
              
              {task.description && (
                <p className="text-sm text-gray-600 mt-1 line-clamp-2">
                  {task.description}
                </p>
              )}
            </div>
          </div>

          <div className="relative">
            <button className="p-1 hover:bg-gray-100 rounded">
              <MoreVertical className="w-4 h-4 text-gray-500" />
            </button>
          </div>
        </div>

        {task.priority !== 'none' && (
          <div className="mb-3">
            <span className={`inline-flex items-center px-2 py-1 rounded-full text-xs font-medium ${getPriorityColor(task.priority)}`}>
              {task.priority}
            </span>
          </div>
        )}

        <div className="space-y-2 text-sm text-gray-600">
          {task.dueDate && (
            <div className="flex items-center space-x-2">
              <Calendar className="w-4 h-4" />
              <span className={isOverdue ? 'text-red-600 font-medium' : ''}>
                {new Date(task.dueDate).toLocaleDateString()}
                {task.dueTime && ` at ${task.dueTime}`}
              </span>
              {isOverdue && <Clock className="w-4 h-4 text-red-600" />}
            </div>
          )}

          {getClientName(task.clientId) && (
            <div className="flex items-center space-x-2">
              <User className="w-4 h-4" />
              <span>{getClientName(task.clientId)}</span>
            </div>
          )}

          {task.attachments && task.attachments.length > 0 && (
            <div className="flex items-center space-x-2">
              <Paperclip className="w-4 h-4" />
              <span>{task.attachments.length} attachment{task.attachments.length !== 1 ? 's' : ''}</span>
            </div>
          )}
        </div>
      </div>
    );
  };

  // Create Task Modal component
  const CreateTaskModal = () => {
    const [taskData, setTaskData] = useState({
      name: '',
      description: '',
      dueDate: '',
      dueTime: '',
      priority: 'none',
      clientId: ''
    });

    const handleSave = () => {
      if (!taskData.name.trim()) {
        addNotification('Task name is required', 'error');
        return;
      }

      const newTask = {
        id: tasks.length + 1,
        ...taskData,
        status: 'todo',
        attachments: []
      };

      setTasks(prev => [newTask, ...prev]);
      setIsCreateModalOpen(false);
      setTaskData({
        name: '',
        description: '',
        dueDate: '',
        dueTime: '',
        priority: 'none',
        clientId: ''
      });
      
      addNotification('Task created successfully', 'success');
    };

    if (!isCreateModalOpen) return null;

    return (
      <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-end z-50">
        <div className="bg-white h-full w-96 overflow-y-auto">
          <div className="flex items-center justify-between p-6 border-b border-gray-200">
            <h2 className="text-lg font-semibold text-gray-900">Create task</h2>
            <button
              onClick={() => setIsCreateModalOpen(false)}
              className="p-1 hover:bg-gray-100 rounded"
            >
              <X className="w-5 h-5" />
            </button>
          </div>

          <div className="p-6 space-y-6">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Task name
              </label>
              <input
                value={taskData.name}
                onChange={(e) => setTaskData(prev => ({ ...prev, name: e.target.value }))}
                placeholder="Write a task"
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Description
              </label>
              <textarea
                value={taskData.description}
                onChange={(e) => setTaskData(prev => ({ ...prev, description: e.target.value }))}
                placeholder="Add task description"
                rows={4}
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Due on
              </label>
              <div className="flex space-x-2">
                <input
                  type="date"
                  value={taskData.dueDate}
                  onChange={(e) => setTaskData(prev => ({ ...prev, dueDate: e.target.value }))}
                  className="flex-1 px-3 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                />
                <input
                  type="time"
                  value={taskData.dueTime}
                  onChange={(e) => setTaskData(prev => ({ ...prev, dueTime: e.target.value }))}
                  className="flex-1 px-3 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                />
              </div>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Priority
              </label>
              <div className="relative">
                <select
                  value={taskData.priority}
                  onChange={(e) => setTaskData(prev => ({ ...prev, priority: e.target.value }))}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-blue-500 appearance-none"
                >
                  <option value="none">None</option>
                  <option value="low">Low</option>
                  <option value="medium">Medium</option>
                  <option value="high">High</option>
                  <option value="urgent">Urgent</option>
                </select>
                <ChevronDown className="absolute right-3 top-1/2 transform -translate-y-1/2 w-4 h-4 text-gray-500 pointer-events-none" />
              </div>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Client
              </label>
              <div className="relative">
                <select
                  value={taskData.clientId}
                  onChange={(e) => setTaskData(prev => ({ ...prev, clientId: e.target.value }))}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-blue-500 appearance-none"
                >
                  <option value="">Select client</option>
                  {clients.map(client => (
                    <option key={client.id} value={client.id}>
                      {client.name}
                    </option>
                  ))}
                </select>
                <ChevronDown className="absolute right-3 top-1/2 transform -translate-y-1/2 w-4 h-4 text-gray-500 pointer-events-none" />
              </div>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Attachments
              </label>
              <div className="border-2 border-dashed border-gray-300 rounded-lg p-6 text-center hover:border-gray-400 cursor-pointer">
                <Upload className="w-8 h-8 text-gray-400 mx-auto mb-2" />
                <p className="text-sm text-gray-600">
                  <span className="text-blue-600 hover:text-blue-700 font-medium">Choose file</span>
                  {' '}or drag and drop file
                </p>
                <p className="text-xs text-gray-500 mt-1">
                  Max number of attachments: 20<br />
                  Max upload size: 50MB
                </p>
              </div>
            </div>
          </div>

          <div className="border-t border-gray-200 p-6 flex justify-end space-x-3">
            <button
              onClick={() => setIsCreateModalOpen(false)}
              className="px-4 py-2 text-sm font-medium text-gray-700 bg-gray-100 rounded-lg hover:bg-gray-200"
            >
              Cancel
            </button>
            <button
              onClick={handleSave}
              className="px-4 py-2 text-sm font-medium text-white bg-blue-600 rounded-lg hover:bg-blue-700"
            >
              Save
            </button>
          </div>
        </div>
      </div>
    );
  };

  // Tasks View component
  const TasksView = () => {
    const filteredTasks = tasks.filter(task =>
      task.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
      task.description.toLowerCase().includes(searchQuery.toLowerCase())
    );

    if (tasks.length === 0) {
      return (
        <div className="flex-1 flex items-center justify-center p-12">
          <div className="text-center max-w-md">
            <div className="w-24 h-24 bg-blue-100 rounded-full flex items-center justify-center mx-auto mb-6">
              <CheckSquare className="w-12 h-12 text-blue-600" />
            </div>
            <h2 className="text-xl font-semibold text-gray-900 mb-3">
              Stay organized with Tasks
            </h2>
            <p className="text-gray-600 mb-8 leading-relaxed">
              Keep track of your to-dos by creating tasks, setting due dates, and assigning priority levels
            </p>
            <button
              onClick={() => setIsCreateModalOpen(true)}
              className="bg-blue-600 text-white px-6 py-3 rounded-lg hover:bg-blue-700 font-medium"
            >
              Add task
            </button>
          </div>
        </div>
      );
    }

    return (
      <div className="p-6">
        <div className="flex justify-between items-center mb-6">
          <div className="flex items-center space-x-4">
            <span className="text-sm text-gray-600">
              {filteredTasks.length} task{filteredTasks.length !== 1 ? 's' : ''}
            </span>
          </div>
          <button
            onClick={() => setIsCreateModalOpen(true)}
            className="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 flex items-center space-x-2"
          >
            <Plus className="w-4 h-4" />
            <span>Add task</span>
          </button>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {filteredTasks.map((task) => (
            <TaskCard key={task.id} task={task} />
          ))}
        </div>
      </div>
    );
  };

  // Notification system
  const addNotification = (message, type = 'info') => {
    const notification = {
      id: Date.now(),
      message,
      type
    };
    
    setNotifications(prev => [...prev, notification]);
    
    setTimeout(() => {
      setNotifications(prev => prev.filter(n => n.id !== notification.id));
    }, 5000);
  };

  const Toast = () => {
    if (notifications.length === 0) return null;

    return (
      <div className="fixed top-4 right-4 z-50 space-y-2">
        {notifications.map((notification) => (
          <div
            key={notification.id}
            className={`flex items-center p-4 rounded-lg shadow-lg border ${
              notification.type === 'success' ? 'bg-green-50 border-green-200' :
              notification.type === 'error' ? 'bg-red-50 border-red-200' :
              'bg-blue-50 border-blue-200'
            }`}
          >
            <div className="flex items-center space-x-3">
              {notification.type === 'success' && <CheckCircle className="w-5 h-5 text-green-500" />}
              {notification.type === 'error' && <X className="w-5 h-5 text-red-500" />}
              {notification.type === 'info' && <Bell className="w-5 h-5 text-blue-500" />}
              <p className="text-sm font-medium text-gray-900">{notification.message}</p>
              <button
                onClick={() => setNotifications(prev => prev.filter(n => n.id !== notification.id))}
                className="ml-4 hover:bg-gray-100 rounded p-1"
              >
                <X className="w-4 h-4 text-gray-500" />
              </button>
            </div>
          </div>
        ))}
      </div>
    );
  };

  // Main render
  return (
    <div className="flex h-screen bg-gray-50">
      <Sidebar />
      
      <div className="flex-1 flex flex-col overflow-hidden">
        <Header />
        
        <main className="flex-1 overflow-auto">
          {activeView === 'tasks' && <TasksView />}
          {activeView === 'clients' && (
            <div className="p-6">
              <h2 className="text-xl font-semibold mb-4">Clients</h2>
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                {clients.map(client => (
                  <div key={client.id} className="bg-white p-4 rounded-lg shadow-sm border">
                    <h3 className="font-medium text-gray-900">{client.name}</h3>
                    <p className="text-sm text-gray-600">{client.email}</p>
                    <p className="text-sm text-gray-600">{client.company}</p>
                  </div>
                ))}
              </div>
            </div>
          )}
          {activeView === 'calendar' && (
            <div className="p-6 text-center">
              <h2 className="text-xl font-semibold mb-4">Calendar View</h2>
              <p className="text-gray-600">Calendar integration coming soon...</p>
            </div>
          )}
          {activeView === 'analytics' && (
            <div className="p-6 text-center">
              <h2 className="text-xl font-semibold mb-4">Analytics</h2>
              <p className="text-gray-600">Analytics dashboard coming soon...</p>
            </div>
          )}
          {activeView === 'settings' && (
            <div className="p-6 text-center">
              <h2 className="text-xl font-semibold mb-4">Settings</h2>
              <p className="text-gray-600">Settings panel coming soon...</p>
            </div>
          )}
        </main>
      </div>

      <CreateTaskModal />
      <Toast />
    </div>
  );
};

export default TaskManagementApp;
