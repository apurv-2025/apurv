import React, { useState, useEffect } from 'react';
import { Layout } from '../components/layout';
import { Card, Button, Input, Toggle } from '../components/ui';
import { SuccessMessage, ErrorMessage } from '../components/common';
import { useAuth } from '../hooks/useAuth';

const Settings = () => {
  const { user, updateProfile, changePassword } = useAuth();
  const [activeTab, setActiveTab] = useState('profile');
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState({ type: '', text: '' });
  
  // Profile form state
  const [profileData, setProfileData] = useState({
    firstName: user?.firstName || '',
    lastName: user?.lastName || '',
    email: user?.email || '',
    phone: user?.phone || '',
    company: user?.company || '',
    jobTitle: user?.jobTitle || ''
  });

  // Password form state
  const [passwordData, setPasswordData] = useState({
    currentPassword: '',
    newPassword: '',
    confirmPassword: ''
  });

  // Notification preferences
  const [notifications, setNotifications] = useState({
    emailNotifications: user?.preferences?.emailNotifications ?? true,
    pushNotifications: user?.preferences?.pushNotifications ?? false,
    weeklyReports: user?.preferences?.weeklyReports ?? true,
    securityAlerts: user?.preferences?.securityAlerts ?? true,
    marketingEmails: user?.preferences?.marketingEmails ?? false
  });

  // Update profile data when user changes
  useEffect(() => {
    console.log('User data received:', user);
    if (user) {
      console.log('Setting profile data with:', {
        firstName: user.firstName || 'MISSING',
        lastName: user.lastName || 'MISSING',
        email: user.email || 'MISSING',
        phone: user.phone || 'MISSING',
        company: user.company || 'MISSING',
        jobTitle: user.jobTitle || 'MISSING'
      });

      setProfileData({
        firstName: user.firstName || '',
        lastName: user.lastName || '',
        email: user.email || '',
        phone: user.phone || '',
        company: user.company || '',
        jobTitle: user.jobTitle || ''
      });
      
      
      setNotifications({
        emailNotifications: user.preferences?.emailNotifications ?? true,
        pushNotifications: user.preferences?.pushNotifications ?? false,
        weeklyReports: user.preferences?.weeklyReports ?? true,
        securityAlerts: user.preferences?.securityAlerts ?? true,
        marketingEmails: user.preferences?.marketingEmails ?? false
      });
    }
  }, [user]);

  const tabs = [
    { id: 'profile', label: 'Profile' },
    { id: 'security', label: 'Security' },
    { id: 'notifications', label: 'Notifications' },
    { id: 'billing', label: 'Billing' }
  ];

  // Clear messages after 5 seconds
  useEffect(() => {
    if (message.text) {
      const timer = setTimeout(() => {
        setMessage({ type: '', text: '' });
      }, 5000);
      return () => clearTimeout(timer);
    }
  }, [message.text]);

  const validatePassword = (password) => {
    if (password.length < 8) {
      return 'Password must be at least 8 characters long';
    }
    if (!/(?=.*[a-z])(?=.*[A-Z])(?=.*\d)/.test(password)) {
      return 'Password must contain at least one uppercase letter, one lowercase letter, and one number';
    }
    return null;
  };

  const handleProfileUpdate = async (e) => {
    e.preventDefault();
    setLoading(true);
    setMessage({ type: '', text: '' });

    try {
      await updateProfile(profileData);
      setMessage({ type: 'success', text: 'Profile updated successfully!' });
    } catch (error) {
      console.error('Profile update error:', error);
      setMessage({ 
        type: 'error', 
        text: error.message || 'Failed to update profile. Please try again.' 
      });
    } finally {
      setLoading(false);
    }
  };

  const handlePasswordChange = async (e) => {
    e.preventDefault();
    setLoading(true);
    setMessage({ type: '', text: '' });

    // Validation
    if (passwordData.newPassword !== passwordData.confirmPassword) {
      setMessage({ type: 'error', text: 'New passwords do not match.' });
      setLoading(false);
      return;
    }

    const passwordError = validatePassword(passwordData.newPassword);
    if (passwordError) {
      setMessage({ type: 'error', text: passwordError });
      setLoading(false);
      return;
    }

    try {
      await changePassword(
        passwordData.currentPassword,  // First parameter
        passwordData.newPassword       // Second parameter
      );

      setMessage({ type: 'success', text: 'Password changed successfully!' });
      setPasswordData({ currentPassword: '', newPassword: '', confirmPassword: '' });
    } catch (error) {
      console.error('Password change error:', error);
      setMessage({ 
        type: 'error', 
        text: error.message || 'Failed to change password. Please check your current password and try again.' 
      });
    } finally {
      setLoading(false);
    }
  };

  const handleNotificationUpdate = async (key, value) => {
    const oldValue = notifications[key];
    
    // Optimistically update UI
    setNotifications(prev => ({ ...prev, [key]: value }));

    try {
      // Fixed: Actually make API call to update notification preferences
      await updateProfile({ 
        preferences: { 
          ...notifications, 
          [key]: value 
        } 
      });
    } catch (error) {
      console.error('Notification update error:', error);
      // Revert on error
      setNotifications(prev => ({ ...prev, [key]: oldValue }));
      setMessage({ 
        type: 'error', 
        text: 'Failed to update notification preferences. Please try again.' 
      });
    }
  };

  const renderTabContent = () => {
    switch (activeTab) {
      case 'profile':
        return (
          <form onSubmit={handleProfileUpdate} className="space-y-6">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div>
                <label htmlFor="firstName" className="block text-sm font-medium text-gray-700 mb-1">
                  First Name
                </label>
                <Input
                  id="firstName"
                  value={profileData.firstName}
                  onChange={(e) => setProfileData(prev => ({ ...prev, firstName: e.target.value }))}
                  required
                  disabled={loading}
                />
              </div>
              <div>
                <label htmlFor="lastName" className="block text-sm font-medium text-gray-700 mb-1">
                  Last Name
                </label>
                <Input
                  id="lastName"
                  value={profileData.lastName}
                  onChange={(e) => setProfileData(prev => ({ ...prev, lastName: e.target.value }))}
                  required
                  disabled={loading}
                />
              </div>
              <div>
                <label htmlFor="email" className="block text-sm font-medium text-gray-700 mb-1">
                  Email
                </label>
                <Input
                  id="email"
                  type="email"
                  value={profileData.email}
                  onChange={(e) => setProfileData(prev => ({ ...prev, email: e.target.value }))}
                  required
                  disabled={loading}
                />
              </div>
              <div>
                <label htmlFor="phone" className="block text-sm font-medium text-gray-700 mb-1">
                  Phone
                </label>
                <Input
                  id="phone"
                  type="tel"
                  value={profileData.phone}
                  onChange={(e) => setProfileData(prev => ({ ...prev, phone: e.target.value }))}
                  disabled={loading}
                />
              </div>
              <div>
                <label htmlFor="company" className="block text-sm font-medium text-gray-700 mb-1">
                  Company
                </label>
                <Input
                  id="company"
                  value={profileData.company}
                  onChange={(e) => setProfileData(prev => ({ ...prev, company: e.target.value }))}
                  disabled={loading}
                />
              </div>
              <div>
                <label htmlFor="jobTitle" className="block text-sm font-medium text-gray-700 mb-1">
                  Job Title
                </label>
                <Input
                  id="jobTitle"
                  value={profileData.jobTitle}
                  onChange={(e) => setProfileData(prev => ({ ...prev, jobTitle: e.target.value }))}
                  disabled={loading}
                />
              </div>
            </div>
            <Button type="submit" loading={loading} disabled={loading}>
              Update Profile
            </Button>
          </form>
        );

      case 'security':
        return (
          <div className="space-y-8">
            <form onSubmit={handlePasswordChange} className="space-y-6">
              <h3 className="text-lg font-medium">Change Password</h3>
              <div className="space-y-4 max-w-md">
                <div>
                  <label htmlFor="currentPassword" className="block text-sm font-medium text-gray-700 mb-1">
                    Current Password
                  </label>
                  <Input
                    id="currentPassword"
                    type="password"
                    value={passwordData.currentPassword}
                    onChange={(e) => setPasswordData(prev => ({ ...prev, currentPassword: e.target.value }))}
                    required
                    disabled={loading}
                  />
                </div>
                <div>
                  <label htmlFor="newPassword" className="block text-sm font-medium text-gray-700 mb-1">
                    New Password
                  </label>
                  <Input
                    id="newPassword"
                    type="password"
                    value={passwordData.newPassword}
                    onChange={(e) => setPasswordData(prev => ({ ...prev, newPassword: e.target.value }))}
                    required
                    disabled={loading}
                    placeholder="At least 8 characters with uppercase, lowercase, and number"
                  />
                </div>
                <div>
                  <label htmlFor="confirmPassword" className="block text-sm font-medium text-gray-700 mb-1">
                    Confirm New Password
                  </label>
                  <Input
                    id="confirmPassword"
                    type="password"
                    value={passwordData.confirmPassword}
                    onChange={(e) => setPasswordData(prev => ({ ...prev, confirmPassword: e.target.value }))}
                    required
                    disabled={loading}
                  />
                </div>
              </div>
              <Button type="submit" loading={loading} disabled={loading}>
                Change Password
              </Button>
            </form>
            
            <div className="border-t pt-8">
              <h3 className="text-lg font-medium mb-4">Two-Factor Authentication</h3>
              <p className="text-gray-600 mb-4">Add an extra layer of security to your account</p>
              <Button variant="outline" disabled={loading}>
                Setup 2FA
              </Button>
            </div>
          </div>
        );

      case 'notifications':
        return (
          <div className="space-y-6">
            <h3 className="text-lg font-medium">Notification Preferences</h3>
            <div className="space-y-4">
              {Object.entries(notifications).map(([key, value]) => (
                <div key={key} className="flex items-center justify-between py-3">
                  <div>
                    <label className="text-sm font-medium text-gray-900">
                      {getNotificationLabel(key)}
                    </label>
                    <p className="text-sm text-gray-500">
                      {getNotificationDescription(key)}
                    </p>
                  </div>
                  <Toggle
                    checked={value}
                    onChange={(checked) => handleNotificationUpdate(key, checked)}
                    disabled={loading}
                  />
                </div>
              ))}
            </div>
          </div>
        );

      case 'billing':
        return (
          <div className="space-y-6">
            <h3 className="text-lg font-medium">Billing Information</h3>
            <p className="text-gray-600">
              Manage your subscription and billing details in the{' '}
              <a href="/subscription" className="text-blue-600 hover:underline">
                Subscription Management
              </a>{' '}
              section.
            </p>
            <div className="bg-gray-50 p-4 rounded-lg">
              <h4 className="font-medium mb-2">Current Plan</h4>
              <p className="text-sm text-gray-600">
                {user?.subscription?.plan || 'Professional Plan'} - 
                ${user?.subscription?.price || '29'}/month
              </p>
            </div>
          </div>
        );

      default:
        return null;
    }
  };

  // Fixed: Better labeling for notification types
  const getNotificationLabel = (key) => {
    const labels = {
      emailNotifications: 'Email Notifications',
      pushNotifications: 'Push Notifications',
      weeklyReports: 'Weekly Reports',
      securityAlerts: 'Security Alerts',
      marketingEmails: 'Marketing Emails'
    };
    return labels[key] || key;
  };

  const getNotificationDescription = (key) => {
    const descriptions = {
      emailNotifications: 'Receive email notifications for important updates',
      pushNotifications: 'Get push notifications on your devices',
      weeklyReports: 'Receive weekly summary reports',
      securityAlerts: 'Get notified about security-related activities',
      marketingEmails: 'Receive product updates and marketing content'
    };
    return descriptions[key] || '';
  };

  return (
    <Layout>
      
      <div className="max-w-10xl mx-auto">

        <div className="mb-8">
          <h1 className="text-2xl font-bold text-gray-900">Settings</h1>
          <p className="text-gray-600 mt-1">Manage your account settings and preferences</p>
        </div>

        {message.text && (
          <div className="mb-6">
            {message.type === 'success' ? (
              <SuccessMessage message={message.text} />
            ) : (
              <ErrorMessage message={message.text} />
            )}
          </div>
        )}

        <div className="grid grid-cols-1 lg:grid-cols-6 gap-8">
          {/* Sidebar Navigation */}
          <div className="lg:col-span-1">
            <nav className="space-y-1" role="tablist">
              {tabs.map((tab) => (
                <button
                  key={tab.id}
                  onClick={() => setActiveTab(tab.id)}
                  role="tab"
                  aria-selected={activeTab === tab.id}
                  aria-controls={`${tab.id}-panel`}
                  className={`w-full text-left px-3 py-2 text-sm font-medium rounded-md transition-colors ${
                    activeTab === tab.id
                      ? 'bg-blue-50 text-blue-700 border-blue-200'
                      : 'text-gray-600 hover:text-gray-900 hover:bg-gray-50'
                  }`}
                >
                  {tab.label}
                </button>
              ))}
            </nav>
          </div>

          {/* Main Content */}
          <div className="lg:col-span-3">
            <Card className="p-6">
              <div role="tabpanel" id={`${activeTab}-panel`}>
                {renderTabContent()}
              </div>
            </Card>
          </div>
        </div>
      </div>
    </Layout>
  );
};

export default Settings;