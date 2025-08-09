import React, { useState, useRef, useEffect } from 'react';
import { 
  User, Bell, Search, Bot, Settings, LogOut, ChevronDown, 
  X, Calendar, MessageSquare, Activity, AlertCircle, CheckCircle,
  Clock, Heart, FileText, Pill, TestTube, Shield, Mail
} from 'lucide-react';
import { useAuth } from '../contexts/AuthContext';

const Header = ({ activeTab, onTabChange, onSearchChange }) => {
  const { user, logout } = useAuth();
  const [showNotifications, setShowNotifications] = useState(false);
  const [showUserMenu, setShowUserMenu] = useState(false);
  const [showSearch, setShowSearch] = useState(false);
  const [showAIAssistant, setShowAIAssistant] = useState(false);
  const [searchTerm, setSearchTerm] = useState('');
  const [notifications, setNotifications] = useState([]);
  
  const notificationRef = useRef(null);
  const userMenuRef = useRef(null);
  const searchRef = useRef(null);

  // Mock notifications data
  useEffect(() => {
    const mockNotifications = [
      {
        id: 1,
        type: 'appointment',
        title: 'Upcoming Appointment',
        message: 'Dr. Sarah Johnson appointment tomorrow at 2:00 PM',
        time: '10 minutes ago',
        read: false,
        icon: Calendar,
        color: 'text-blue-600 bg-blue-100'
      },
      {
        id: 2,
        type: 'message',
        title: 'New Message',
        message: 'You have a new message from your healthcare provider',
        time: '1 hour ago',
        read: false,
        icon: MessageSquare,
        color: 'text-green-600 bg-green-100'
      },
      {
        id: 3,
        type: 'results',
        title: 'Lab Results Available',
        message: 'Your blood work results are now available for review',
        time: '2 hours ago',
        read: false,
        icon: TestTube,
        color: 'text-purple-600 bg-purple-100'
      },
      {
        id: 4,
        type: 'prescription',
        title: 'Prescription Refill',
        message: 'Your prescription refill request has been approved',
        time: '1 day ago',
        read: true,
        icon: Pill,
        color: 'text-orange-600 bg-orange-100'
      },
      {
        id: 5,
        type: 'health',
        title: 'Health Reminder',
        message: 'Time for your daily medication reminder',
        time: '2 days ago',
        read: true,
        icon: Heart,
        color: 'text-red-600 bg-red-100'
      }
    ];
    setNotifications(mockNotifications);
  }, []);

  // Close dropdowns when clicking outside
  useEffect(() => {
    const handleClickOutside = (event) => {
      if (notificationRef.current && !notificationRef.current.contains(event.target)) {
        setShowNotifications(false);
      }
      if (userMenuRef.current && !userMenuRef.current.contains(event.target)) {
        setShowUserMenu(false);
      }
      if (searchRef.current && !searchRef.current.contains(event.target)) {
        setShowSearch(false);
      }
    };

    document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, []);

  const unreadCount = notifications.filter(n => !n.read).length;

  const handleSearch = (e) => {
    e.preventDefault();
    if (onSearchChange) {
      onSearchChange(searchTerm);
    }
    setShowSearch(false);
  };

  const markNotificationAsRead = (notificationId) => {
    setNotifications(prev => 
      prev.map(n => n.id === notificationId ? { ...n, read: true } : n)
    );
  };

  const markAllAsRead = () => {
    setNotifications(prev => prev.map(n => ({ ...n, read: true })));
  };

  const handleLogout = () => {
    logout();
    setShowUserMenu(false);
  };

  return (
    <div className="bg-white shadow-sm border-b border-gray-200 px-6 py-4 sticky top-0 z-50">
      <div className="flex items-center justify-between">
        {/* Left Side - Title and Welcome */}
        <div className="flex-1">
          <h2 className="text-2xl font-bold text-gray-800 capitalize">
            {activeTab.replace('-', ' ')}
          </h2>
          <p className="text-gray-600">Welcome back, {user?.first_name || 'User'}</p>
        </div>

        {/* Right Side - Actions */}
        <div className="flex items-center space-x-2">
          {/* Search */}
          <div className="relative" ref={searchRef}>
            <button
              onClick={() => setShowSearch(!showSearch)}
              className="p-2 text-gray-600 hover:text-gray-800 hover:bg-gray-100 rounded-full transition-colors"
              title="Search"
            >
              <Search className="w-5 h-5" />
            </button>
            
            {showSearch && (
              <div className="absolute right-0 top-12 w-80 bg-white border border-gray-200 rounded-lg shadow-lg z-50">
                <form onSubmit={handleSearch} className="p-4">
                  <div className="flex items-center space-x-2">
                    <div className="flex-1 relative">
                      <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-4 h-4" />
                      <input
                        type="text"
                        value={searchTerm}
                        onChange={(e) => setSearchTerm(e.target.value)}
                        placeholder="Search appointments, messages, records..."
                        className="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                        autoFocus
                      />
                    </div>
                    <button
                      type="submit"
                      className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
                    >
                      Search
                    </button>
                  </div>
                  <div className="mt-3 text-sm text-gray-600">
                    <p>Quick search across:</p>
                    <div className="mt-1 flex flex-wrap gap-1">
                      <span className="px-2 py-1 bg-gray-100 rounded text-xs">Appointments</span>
                      <span className="px-2 py-1 bg-gray-100 rounded text-xs">Messages</span>
                      <span className="px-2 py-1 bg-gray-100 rounded text-xs">Records</span>
                      <span className="px-2 py-1 bg-gray-100 rounded text-xs">Prescriptions</span>
                    </div>
                  </div>
                </form>
              </div>
            )}
          </div>

          {/* AI Assistant */}
          <button
            onClick={() => {
              if (onTabChange) {
                onTabChange('agent');
              }
              setShowAIAssistant(!showAIAssistant);
            }}
            className="p-2 text-gray-600 hover:text-gray-800 hover:bg-gray-100 rounded-full transition-colors relative"
            title="AI Assistant"
          >
            <Bot className="w-5 h-5" />
            <span className="absolute -top-1 -right-1 w-2 h-2 bg-green-500 rounded-full"></span>
          </button>

          {/* Notifications */}
          <div className="relative" ref={notificationRef}>
            <button
              onClick={() => setShowNotifications(!showNotifications)}
              className="relative p-2 text-gray-600 hover:text-gray-800 hover:bg-gray-100 rounded-full transition-colors"
              title="Notifications"
            >
              <Bell className="w-5 h-5" />
              {unreadCount > 0 && (
                <span className="absolute -top-1 -right-1 min-w-[18px] h-[18px] bg-red-500 text-white text-xs rounded-full flex items-center justify-center">
                  {unreadCount > 9 ? '9+' : unreadCount}
                </span>
              )}
            </button>

            {showNotifications && (
              <div className="absolute right-0 top-12 w-96 bg-white border border-gray-200 rounded-lg shadow-lg z-50">
                <div className="p-4 border-b border-gray-200">
                  <div className="flex items-center justify-between">
                    <h3 className="font-semibold text-gray-900">Notifications</h3>
                    {unreadCount > 0 && (
                      <button
                        onClick={markAllAsRead}
                        className="text-sm text-blue-600 hover:text-blue-700"
                      >
                        Mark all as read
                      </button>
                    )}
                  </div>
                </div>
                
                <div className="max-h-96 overflow-y-auto">
                  {notifications.length === 0 ? (
                    <div className="p-4 text-center text-gray-500">
                      <Bell className="w-8 h-8 mx-auto mb-2 text-gray-300" />
                      <p>No notifications</p>
                    </div>
                  ) : (
                    notifications.map(notification => {
                      const IconComponent = notification.icon;
                      return (
                        <div
                          key={notification.id}
                          className={`p-4 border-b border-gray-100 hover:bg-gray-50 cursor-pointer ${
                            !notification.read ? 'bg-blue-50' : ''
                          }`}
                          onClick={() => markNotificationAsRead(notification.id)}
                        >
                          <div className="flex items-start space-x-3">
                            <div className={`p-2 rounded-full ${notification.color}`}>
                              <IconComponent className="w-4 h-4" />
                            </div>
                            <div className="flex-1 min-w-0">
                              <p className={`text-sm font-medium ${!notification.read ? 'text-gray-900' : 'text-gray-700'}`}>
                                {notification.title}
                              </p>
                              <p className="text-sm text-gray-600 mt-1">{notification.message}</p>
                              <p className="text-xs text-gray-500 mt-2">{notification.time}</p>
                            </div>
                            {!notification.read && (
                              <div className="w-2 h-2 bg-blue-600 rounded-full mt-2"></div>
                            )}
                          </div>
                        </div>
                      );
                    })
                  )}
                </div>
                
                <div className="p-3 border-t border-gray-200">
                  <button className="w-full text-sm text-blue-600 hover:text-blue-700 font-medium">
                    View all notifications
                  </button>
                </div>
              </div>
            )}
          </div>

          {/* User Menu */}
          <div className="relative" ref={userMenuRef}>
            <button
              onClick={() => setShowUserMenu(!showUserMenu)}
              className="flex items-center space-x-2 p-2 text-gray-600 hover:text-gray-800 hover:bg-gray-100 rounded-lg transition-colors"
              title="User Menu"
            >
              <div className="w-8 h-8 bg-gradient-to-r from-blue-500 to-purple-600 rounded-full flex items-center justify-center">
                <User className="w-5 h-5 text-white" />
              </div>
              <ChevronDown className="w-4 h-4" />
            </button>

            {showUserMenu && (
              <div className="absolute right-0 top-12 w-64 bg-white border border-gray-200 rounded-lg shadow-lg z-50">
                <div className="p-4 border-b border-gray-200">
                  <div className="flex items-center space-x-3">
                    <div className="w-12 h-12 bg-gradient-to-r from-blue-500 to-purple-600 rounded-full flex items-center justify-center">
                      <User className="w-6 h-6 text-white" />
                    </div>
                    <div>
                      <p className="font-semibold text-gray-900">
                        {user?.first_name} {user?.last_name}
                      </p>
                      <p className="text-sm text-gray-600">{user?.email}</p>
                    </div>
                  </div>
                </div>

                <div className="py-2">
                  <button
                    onClick={() => {
                      if (onTabChange) {
                        onTabChange('profile');
                      }
                      setShowUserMenu(false);
                    }}
                    className="w-full px-4 py-2 text-left text-sm text-gray-700 hover:bg-gray-100 flex items-center space-x-2"
                  >
                    <User className="w-4 h-4" />
                    <span>View Profile</span>
                  </button>
                  
                  <button
                    onClick={() => {
                      if (onTabChange) {
                        onTabChange('settings');
                      }
                      setShowUserMenu(false);
                    }}
                    className="w-full px-4 py-2 text-left text-sm text-gray-700 hover:bg-gray-100 flex items-center space-x-2"
                  >
                    <Settings className="w-4 h-4" />
                    <span>Settings</span>
                  </button>

                  <div className="border-t border-gray-100 my-2"></div>
                  
                  <button
                    onClick={() => {
                      if (onTabChange) {
                        onTabChange('help');
                      }
                      setShowUserMenu(false);
                    }}
                    className="w-full px-4 py-2 text-left text-sm text-gray-700 hover:bg-gray-100 flex items-center space-x-2"
                  >
                    <Shield className="w-4 h-4" />
                    <span>Help & Support</span>
                  </button>

                  <div className="border-t border-gray-100 my-2"></div>
                  
                  <button
                    onClick={handleLogout}
                    className="w-full px-4 py-2 text-left text-sm text-red-600 hover:bg-red-50 flex items-center space-x-2"
                  >
                    <LogOut className="w-4 h-4" />
                    <span>Sign Out</span>
                  </button>
                </div>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default Header; 