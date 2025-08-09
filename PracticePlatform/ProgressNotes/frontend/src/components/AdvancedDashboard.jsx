import React, { useState, useEffect } from 'react';
import { 
  BarChart3, 
  TrendingUp, 
  Users, 
  FileText, 
  Calendar, 
  Clock,
  AlertTriangle,
  CheckCircle,
  XCircle,
  Search,
  Filter,
  Download,
  Settings,
  Plus,
  Edit,
  Trash2,
  Eye,
  UserPlus,
  Shield,
  Activity,
  Database,
  Bell,
  Mail,
  Phone
} from 'lucide-react';

// Advanced Dashboard Component
const Dashboard = () => {
  const [stats, setStats] = useState(null);
  const [recentNotes, setRecentNotes] = useState([]);
  const [loading, setLoading] = useState(true);
  const [timeRange, setTimeRange] = useState('30'); // days

  useEffect(() => {
    fetchDashboardData();
  }, [timeRange]);

  const fetchDashboardData = async () => {
    setLoading(true);
    try {
      const [statsData, notesData] = await Promise.all([
        APIService.getDashboardStats(),
        APIService.getNotes({ page_size: 10, page: 1 })
      ]);
      setStats(statsData);
      setRecentNotes(notesData.items || []);
    } catch (error) {
      console.error('Error fetching dashboard data:', error);
    } finally {
      setLoading(false);
    }
  };

  const StatCard = ({ title, value, change, icon: Icon, color = "blue" }) => (
    <div className="bg-white rounded-lg shadow p-6">
      <div className="flex items-center justify-between">
        <div>
          <p className="text-sm font-medium text-gray-600">{title}</p>
          <p className="text-3xl font-bold text-gray-900">{value}</p>
          {change && (
            <p className={`text-sm ${change > 0 ? 'text-green-600' : 'text-red-600'} flex items-center mt-2`}>
              <TrendingUp className="h-4 w-4 mr-1" />
              {change > 0 ? '+' : ''}{change}% from last month
            </p>
          )}
        </div>
        <div className={`p-3 rounded-full bg-${color}-100`}>
          <Icon className={`h-6 w-6 text-${color}-600`} />
        </div>
      </div>
    </div>
  );

  const ActivityItem = ({ note }) => (
    <div className="flex items-center space-x-3 p-3 hover:bg-gray-50 rounded-lg">
      <div className="flex-shrink-0">
        <div className="h-8 w-8 bg-blue-100 rounded-full flex items-center justify-center">
          <FileText className="h-4 w-4 text-blue-600" />
        </div>
      </div>
      <div className="flex-1 min-w-0">
        <p className="text-sm font-medium text-gray-900 truncate">
          {note.patient?.first_name} {note.patient?.last_name}
        </p>
        <div className="flex items-center space-x-2 text-xs text-gray-500">
          <span>{note.note_type}</span>
          <span>•</span>
          <span>{new Date(note.session_date).toLocaleDateString()}</span>
          {note.is_signed && (
            <>
              <span>•</span>
              <span className="text-green-600">Signed</span>
            </>
          )}
        </div>
      </div>
      <div className="flex-shrink-0">
        <span className={`inline-flex items-center px-2 py-1 text-xs rounded-full ${
          note.is_draft ? 'bg-yellow-100 text-yellow-800' : 'bg-green-100 text-green-800'
        }`}>
          {note.is_draft ? 'Draft' : 'Complete'}
        </span>
      </div>
    </div>
  );

  if (loading) {
    return (
      <div className="p-6">
        <div className="animate-pulse">
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
            {[...Array(4)].map((_, i) => (
              <div key={i} className="bg-gray-200 h-32 rounded-lg"></div>
            ))}
          </div>
          <div className="bg-gray-200 h-64 rounded-lg"></div>
        </div>
      </div>
    );
  }

  return (
    <div className="p-6">
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-2xl font-bold text-gray-900">Dashboard</h1>
        <div className="flex items-center space-x-3">
          <select
            value={timeRange}
            onChange={(e) => setTimeRange(e.target.value)}
            className="px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
          >
            <option value="7">Last 7 days</option>
            <option value="30">Last 30 days</option>
            <option value="90">Last 90 days</option>
          </select>
          <button className="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700">
            <Download className="h-4 w-4 mr-2 inline" />
            Export
          </button>
        </div>
      </div>

      {/* Stats Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
        <StatCard
          title="Total Notes"
          value={stats?.total_notes || 0}
          change={12}
          icon={FileText}
          color="blue"
        />
        <StatCard
          title="Draft Notes"
          value={stats?.draft_notes || 0}
          change={-5}
          icon={Edit}
          color="yellow"
        />
        <StatCard
          title="Signed Notes"
          value={stats?.signed_notes || 0}
          change={8}
          icon={CheckCircle}
          color="green"
        />
        <StatCard
          title="This Week"
          value={stats?.notes_this_week || 0}
          change={15}
          icon={Calendar}
          color="purple"
        />
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Recent Activity */}
        <div className="lg:col-span-2 bg-white rounded-lg shadow">
          <div className="px-6 py-4 border-b border-gray-200">
            <h2 className="text-lg font-medium text-gray-900">Recent Activity</h2>
          </div>
          <div className="p-6">
            {recentNotes.length > 0 ? (
              <div className="space-y-2">
                {recentNotes.slice(0, 8).map((note) => (
                  <ActivityItem key={note.id} note={note} />
                ))}
              </div>
            ) : (
              <p className="text-gray-500 text-center py-8">No recent activity</p>
            )}
          </div>
        </div>

        {/* Quick Actions */}
        <div className="bg-white rounded-lg shadow">
          <div className="px-6 py-4 border-b border-gray-200">
            <h2 className="text-lg font-medium text-gray-900">Quick Actions</h2>
          </div>
          <div className="p-6 space-y-3">
            <button className="w-full flex items-center px-4 py-3 text-left text-gray-700 hover:bg-gray-50 rounded-lg">
              <Plus className="h-5 w-5 mr-3 text-blue-600" />
              Create New Note
            </button>
            <button className="w-full flex items-center px-4 py-3 text-left text-gray-700 hover:bg-gray-50 rounded-lg">
              <UserPlus className="h-5 w-5 mr-3 text-green-600" />
              Add New Patient
            </button>
            <button className="w-full flex items-center px-4 py-3 text-left text-gray-700 hover:bg-gray-50 rounded-lg">
              <Search className="h-5 w-5 mr-3 text-purple-600" />
              Search Notes
            </button>
            <button className="w-full flex items-center px-4 py-3 text-left text-gray-700 hover:bg-gray-50 rounded-lg">
              <BarChart3 className="h-5 w-5 mr-3 text-orange-600" />
              View Reports
            </button>
          </div>
        </div>
      </div>

      {/* Alerts/Notifications */}
      <div className="mt-6 bg-white rounded-lg shadow">
        <div className="px-6 py-4 border-b border-gray-200">
          <h2 className="text-lg font-medium text-gray-900">System Alerts</h2>
        </div>
        <div className="p-6">
          <div className="space-y-3">
            <div className="flex items-center p-3 bg-yellow-50 border border-yellow-200 rounded-lg">
              <AlertTriangle className="h-5 w-5 text-yellow-600 mr-3" />
              <div>
                <p className="text-sm font-medium text-yellow-800">5 draft notes need attention</p>
                <p className="text-xs text-yellow-600">These drafts have been pending for over 24 hours</p>
              </div>
            </div>
            <div className="flex items-center p-3 bg-blue-50 border border-blue-200 rounded-lg">
              <Bell className="h-5 w-5 text-blue-600 mr-3" />
              <div>
                <p className="text-sm font-medium text-blue-800">System maintenance scheduled</p>
                <p className="text-xs text-blue-600">Maintenance window: Tonight 2:00 AM - 4:00 AM</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

// Advanced Search and Filter Component
const AdvancedSearch = ({ onSearch, onClose }) => {
  const [filters, setFilters] = useState({
    search_query: '',
    note_type: '',
    patient_name: '',
    clinician_name: '',
    date_from: '',
    date_to: '',
    is_signed: '',
    is_draft: '',
    content_search: ''
  });

  const [savedSearches, setSavedSearches] = useState([]);

  const handleFilterChange = (key, value) => {
    setFilters(prev => ({ ...prev, [key]: value }));
  };

  const handleSearch = () => {
    onSearch(filters);
  };

  const handleReset = () => {
    setFilters({
      search_query: '',
      note_type: '',
      patient_name: '',
      clinician_name: '',
      date_from: '',
      date_to: '',
      is_signed: '',
      is_draft: '',
      content_search: ''
    });
  };

  const saveSearch = () => {
    const searchName = prompt('Enter a name for this search:');
    if (searchName) {
      const newSearch = { name: searchName, filters: { ...filters } };
      setSavedSearches(prev => [...prev, newSearch]);
    }
  };

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div className="bg-white rounded-lg shadow-xl w-full max-w-4xl max-h-[90vh] overflow-y-auto">
        <div className="px-6 py-4 border-b border-gray-200 flex justify-between items-center">
          <h2 className="text-xl font-bold text-gray-900">Advanced Search</h2>
          <button
            onClick={onClose}
            className="text-gray-400 hover:text-gray-600"
          >
            <XCircle className="h-6 w-6" />
          </button>
        </div>

        <div className="p-6">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {/* Basic Search */}
            <div>
              <h3 className="text-lg font-medium text-gray-900 mb-4">Basic Search</h3>
              <div className="space-y-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    General Search
                  </label>
                  <input
                    type="text"
                    value={filters.search_query}
                    onChange={(e) => handleFilterChange('search_query', e.target.value)}
                    placeholder="Search across all fields..."
                    className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Note Type
                  </label>
                  <select
                    value={filters.note_type}
                    onChange={(e) => handleFilterChange('note_type', e.target.value)}
                    className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                  >
                    <option value="">All Types</option>
                    <option value="SOAP">SOAP</option>
                    <option value="DAP">DAP</option>
                    <option value="BIRP">BIRP</option>
                    <option value="PAIP">PAIP</option>
                  </select>
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Patient Name
                  </label>
                  <input
                    type="text"
                    value={filters.patient_name}
                    onChange={(e) => handleFilterChange('patient_name', e.target.value)}
                    placeholder="Patient first or last name..."
                    className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Status
                  </label>
                  <div className="grid grid-cols-2 gap-2">
                    <select
                      value={filters.is_draft}
                      onChange={(e) => handleFilterChange('is_draft', e.target.value)}
                      className="px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                    >
                      <option value="">All Drafts</option>
                      <option value="true">Drafts Only</option>
                      <option value="false">Not Drafts</option>
                    </select>
                    <select
                      value={filters.is_signed}
                      onChange={(e) => handleFilterChange('is_signed', e.target.value)}
                      className="px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                    >
                      <option value="">All Signed</option>
                      <option value="true">Signed Only</option>
                      <option value="false">Not Signed</option>
                    </select>
                  </div>
                </div>
              </div>
            </div>

            {/* Advanced Filters */}
            <div>
              <h3 className="text-lg font-medium text-gray-900 mb-4">Advanced Filters</h3>
              <div className="space-y-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Date Range
                  </label>
                  <div className="grid grid-cols-2 gap-2">
                    <input
                      type="date"
                      value={filters.date_from}
                      onChange={(e) => handleFilterChange('date_from', e.target.value)}
                      className="px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                    />
                    <input
                      type="date"
                      value={filters.date_to}
                      onChange={(e) => handleFilterChange('date_to', e.target.value)}
                      className="px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                    />
                  </div>
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Clinician Name
                  </label>
                  <input
                    type="text"
                    value={filters.clinician_name}
                    onChange={(e) => handleFilterChange('clinician_name', e.target.value)}
                    placeholder="Clinician first or last name..."
                    className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Content Search
                  </label>
                  <textarea
                    value={filters.content_search}
                    onChange={(e) => handleFilterChange('content_search', e.target.value)}
                    placeholder="Search within note content..."
                    rows={3}
                    className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                  />
                </div>
              </div>
            </div>
          </div>

          {/* Saved Searches */}
          {savedSearches.length > 0 && (
            <div className="mt-6">
              <h3 className="text-lg font-medium text-gray-900 mb-4">Saved Searches</h3>
              <div className="flex flex-wrap gap-2">
                {savedSearches.map((search, index) => (
                  <button
                    key={index}
                    onClick={() => setFilters(search.filters)}
                    className="px-3 py-1 bg-gray-100 text-gray-700 rounded-full text-sm hover:bg-gray-200"
                  >
                    {search.name}
                  </button>
                ))}
              </div>
            </div>
          )}

          {/* Actions */}
          <div className="flex justify-between items-center mt-8 pt-6 border-t border-gray-200">
            <div className="flex space-x-3">
              <button
                onClick={handleReset}
                className="px-4 py-2 text-gray-700 border border-gray-300 rounded-md hover:bg-gray-50"
              >
                Reset
              </button>
              <button
                onClick={saveSearch}
                className="px-4 py-2 text-blue-600 border border-blue-600 rounded-md hover:bg-blue-50"
              >
                Save Search
              </button>
            </div>
            <div className="flex space-x-3">
              <button
                onClick={onClose}
                className="px-4 py-2 text-gray-700 border border-gray-300 rounded-md hover:bg-gray-50"
              >
                Cancel
              </button>
              <button
                onClick={handleSearch}
                className="px-6 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700"
              >
                Search
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

// User Management Component (Admin only)
const UserManagement = () => {
  const [users, setUsers] = useState([]);
  const [loading, setLoading] = useState(true);
  const [showCreateModal, setShowCreateModal] = useState(false);
  const [selectedUser, setSelectedUser] = useState(null);
  const [searchTerm, setSearchTerm] = useState('');

  useEffect(() => {
    fetchUsers();
  }, []);

  const fetchUsers = async () => {
    setLoading(true);
    try {
      const data = await APIService.getUsers();
      setUsers(data);
    } catch (error) {
      console.error('Error fetching users:', error);
    } finally {
      setLoading(false);
    }
  };

  const UserCard = ({ user }) => (
    <div className="bg-white rounded-lg shadow p-6">
      <div className="flex items-center justify-between">
        <div className="flex items-center space-x-3">
          <div className="h-12 w-12 bg-blue-100 rounded-full flex items-center justify-center">
            <Users className="h-6 w-6 text-blue-600" />
          </div>
          <div>
            <h3 className="text-lg font-medium text-gray-900">
              {user.first_name} {user.last_name}
            </h3>
            <p className="text-sm text-gray-600">{user.email}</p>
            <div className="flex items-center space-x-2 mt-1">
              <span className={`px-2 py-1 text-xs rounded-full ${
                user.role === 'admin' ? 'bg-red-100 text-red-800' :
                user.role === 'supervisor' ? 'bg-purple-100 text-purple-800' :
                user.role === 'clinician' ? 'bg-blue-100 text-blue-800' :
                'bg-gray-100 text-gray-800'
              }`}>
                {user.role}
              </span>
              <span className={`px-2 py-1 text-xs rounded-full ${
                user.is_active ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'
              }`}>
                {user.is_active ? 'Active' : 'Inactive'}
              </span>
            </div>
          </div>
        </div>
        <div className="flex items-center space-x-2">
          <button
            onClick={() => setSelectedUser(user)}
            className="p-2 text-gray-400 hover:text-blue-600"
          >
            <Edit className="h-4 w-4" />
          </button>
          <button
            onClick={() => setSelectedUser(user)}
            className="p-2 text-gray-400 hover:text-gray-600"
          >
            <Eye className="h-4 w-4" />
          </button>
        </div>
      </div>
      {user.license_number && (
        <div className="mt-3 text-sm text-gray-600">
          <span className="font-medium">License:</span> {user.license_number}
        </div>
      )}
      <div className="mt-3 text-xs text-gray-500">
        Created: {new Date(user.created_at).toLocaleDateString()}
      </div>
    </div>
  );

  const filteredUsers = users.filter(user =>
    user.first_name.toLowerCase().includes(searchTerm.toLowerCase()) ||
    user.last_name.toLowerCase().includes(searchTerm.toLowerCase()) ||
    user.email.toLowerCase().includes(searchTerm.toLowerCase()) ||
    user.role.toLowerCase().includes(searchTerm.toLowerCase())
  );

  return (
    <div className="p-6">
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-2xl font-bold text-gray-900">User Management</h1>
        <button
          onClick={() => setShowCreateModal(true)}
          className="bg-blue-600 text-white px-4 py-2 rounded-md hover:bg-blue-700 flex items-center"
        >
          <UserPlus className="h-4 w-4 mr-2" />
          Add User
        </button>
      </div>

      {/* Search and Filters */}
      <div className="bg-white p-4 rounded-lg shadow mb-6">
        <div className="flex items-center space-x-4">
          <div className="flex-1 relative">
            <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 h-4 w-4" />
            <input
              type="text"
              placeholder="Search users by name, email, or role..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
          </div>
          <button className="px-4 py-2 text-gray-600 border border-gray-300 rounded-md hover:bg-gray-50">
            <Filter className="h-4 w-4 mr-2 inline" />
            Filters
          </button>
        </div>
      </div>

      {/* Users Grid */}
      {loading ? (
        <div className="text-center py-8">Loading users...</div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {filteredUsers.map((user) => (
            <UserCard key={user.id} user={user} />
          ))}
        </div>
      )}

      {/* Statistics */}
      <div className="mt-8 grid grid-cols-1 md:grid-cols-4 gap-6">
        <div className="bg-white rounded-lg shadow p-4">
          <div className="flex items-center">
            <Users className="h-8 w-8 text-blue-500 mr-3" />
            <div>
              <p className="text-sm text-gray-600">Total Users</p>
              <p className="text-2xl font-bold text-gray-900">{users.length}</p>
            </div>
          </div>
        </div>
        <div className="bg-white rounded-lg shadow p-4">
          <div className="flex items-center">
            <Shield className="h-8 w-8 text-green-500 mr-3" />
            <div>
              <p className="text-sm text-gray-600">Active Users</p>
              <p className="text-2xl font-bold text-gray-900">
                {users.filter(u => u.is_active).length}
              </p>
            </div>
          </div>
        </div>
        <div className="bg-white rounded-lg shadow p-4">
          <div className="flex items-center">
            <Activity className="h-8 w-8 text-purple-500 mr-3" />
            <div>
              <p className="text-sm text-gray-600">Clinicians</p>
              <p className="text-2xl font-bold text-gray-900">
                {users.filter(u => u.role === 'clinician').length}
              </p>
            </div>
          </div>
        </div>
        <div className="bg-white rounded-lg shadow p-4">
          <div className="flex items-center">
            <Settings className="h-8 w-8 text-orange-500 mr-3" />
            <div>
              <p className="text-sm text-gray-600">Admins</p>
              <p className="text-2xl font-bold text-gray-900">
                {users.filter(u => u.role === 'admin').length}
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

// Settings Component
const SystemSettings = () => {
  const [settings, setSettings] = useState({
    session_timeout: 15,
    auto_save_interval: 60,
    max_file_size: 10,
    password_policy: {
      min_length: 8,
      require_uppercase: true,
      require_lowercase: true,
      require_numbers: true,
      require_symbols: false
    },
    audit_retention_days: 2555, // 7 years
    email_notifications: true,
    system_maintenance_mode: false
  });

  const [saving, setSaving] = useState(false);

  const handleSettingChange = (path, value) => {
    setSettings(prev => {
      const newSettings = { ...prev };
      const keys = path.split('.');
      let current = newSettings;
      
      for (let i = 0; i < keys.length - 1; i++) {
        current = current[keys[i]];
      }
      current[keys[keys.length - 1]] = value;
      
      return newSettings;
    });
  };

  const saveSettings = async () => {
    setSaving(true);
    try {
      // API call to save settings
      await new Promise(resolve => setTimeout(resolve, 1000)); // Simulate API call
      alert('Settings saved successfully!');
    } catch (error) {
      alert('Failed to save settings');
    } finally {
      setSaving(false);
    }
  };

  return (
    <div className="p-6">
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-2xl font-bold text-gray-900">System Settings</h1>
        <button
          onClick={saveSettings}
          disabled={saving}
          className="bg-blue-600 text-white px-4 py-2 rounded-md hover:bg-blue-700 disabled:opacity-50 flex items-center"
        >
          <Settings className="h-4 w-4 mr-2" />
          {saving ? 'Saving...' : 'Save Settings'}
        </button>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Security Settings */}
        <div className="bg-white rounded-lg shadow">
          <div className="px-6 py-4 border-b border-gray-200">
            <h2 className="text-lg font-medium text-gray-900">Security Settings</h2>
          </div>
          <div className="p-6 space-y-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Session Timeout (minutes)
              </label>
              <input
                type="number"
                value={settings.session_timeout}
                onChange={(e) => handleSettingChange('session_timeout', parseInt(e.target.value))}
                min="5"
                max="120"
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Password Policy
              </label>
              <div className="space-y-2">
                <div className="flex items-center">
                  <input
                    type="checkbox"
                    checked={settings.password_policy.require_uppercase}
                    onChange={(e) => handleSettingChange('password_policy.require_uppercase', e.target.checked)}
                    className="mr-2"
                  />
                  <span className="text-sm text-gray-700">Require uppercase letters</span>
                </div>
                <div className="flex items-center">
                  <input
                    type="checkbox"
                    checked={settings.password_policy.require_lowercase}
                    onChange={(e) => handleSettingChange('password_policy.require_lowercase', e.target.checked)}
                    className="mr-2"
                  />
                  <span className="text-sm text-gray-700">Require lowercase letters</span>
                </div>
                <div className="flex items-center">
                  <input
                    type="checkbox"
                    checked={settings.password_policy.require_numbers}
                    onChange={(e) => handleSettingChange('password_policy.require_numbers', e.target.checked)}
                    className="mr-2"
                  />
                  <span className="text-sm text-gray-700">Require numbers</span>
                </div>
                <div className="flex items-center">
                  <input
                    type="checkbox"
                    checked={settings.password_policy.require_symbols}
                    onChange={(e) => handleSettingChange('password_policy.require_symbols', e.target.checked)}
                    className="mr-2"
                  />
                  <span className="text-sm text-gray-700">Require symbols</span>
                </div>
              </div>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Audit Log Retention (days)
              </label>
              <input
                type="number"
                value={settings.audit_retention_days}
                onChange={(e) => handleSettingChange('audit_retention_days', parseInt(e.target.value))}
                min="365"
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              />
              <p className="text-xs text-gray-500 mt-1">Recommended: 2555 days (7 years) for HIPAA compliance</p>
            </div>
          </div>
        </div>

        {/* Application Settings */}
        <div className="bg-white rounded-lg shadow">
          <div className="px-6 py-4 border-b border-gray-200">
            <h2 className="text-lg font-medium text-gray-900">Application Settings</h2>
          </div>
          <div className="p-6 space-y-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Auto-save Interval (seconds)
              </label>
              <input
                type="number"
                value={settings.auto_save_interval}
                onChange={(e) => handleSettingChange('auto_save_interval', parseInt(e.target.value))}
                min="30"
                max="300"
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Maximum File Size (MB)
              </label>
              <input
                type="number"
                value={settings.max_file_size}
                onChange={(e) => handleSettingChange('max_file_size', parseInt(e.target.value))}
                min="1"
                max="50"
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              />
            </div>

            <div className="flex items-center">
              <input
                type="checkbox"
                checked={settings.email_notifications}
                onChange={(e) => handleSettingChange('email_notifications', e.target.checked)}
                className="mr-2"
              />
              <span className="text-sm text-gray-700">Enable email notifications</span>
            </div>

            <div className="flex items-center">
              <input
                type="checkbox"
                checked={settings.system_maintenance_mode}
                onChange={(e) => handleSettingChange('system_maintenance_mode', e.target.checked)}
                className="mr-2"
              />
              <span className="text-sm text-gray-700">Maintenance mode</span>
            </div>
          </div>
        </div>
      </div>

      {/* System Information */}
      <div className="mt-6 bg-white rounded-lg shadow">
        <div className="px-6 py-4 border-b border-gray-200">
          <h2 className="text-lg font-medium text-gray-900">System Information</h2>
        </div>
        <div className="p-6">
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
            <div className="flex items-center">
              <Database className="h-5 w-5 text-gray-400 mr-2" />
              <div>
                <p className="text-sm text-gray-600">Database</p>
                <p className="text-sm font-medium text-gray-900">PostgreSQL 15</p>
              </div>
            </div>
            <div className="flex items-center">
              <Activity className="h-5 w-5 text-gray-400 mr-2" />
              <div>
                <p className="text-sm text-gray-600">Version</p>
                <p className="text-sm font-medium text-gray-900">v1.0.0</p>
              </div>
            </div>
            <div className="flex items-center">
              <Clock className="h-5 w-5 text-gray-400 mr-2" />
              <div>
                <p className="text-sm text-gray-600">Uptime</p>
                <p className="text-sm font-medium text-gray-900">5 days, 3 hours</p>
              </div>
            </div>
            <div className="flex items-center">
              <CheckCircle className="h-5 w-5 text-green-500 mr-2" />
              <div>
                <p className="text-sm text-gray-600">Status</p>
                <p className="text-sm font-medium text-green-600">Healthy</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export { Dashboard, AdvancedSearch, UserManagement, SystemSettings };
