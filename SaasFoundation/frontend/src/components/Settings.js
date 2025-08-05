// frontend/src/components/Settings.js
import React, { useState, useEffect } from 'react';
import { useAuth } from '../contexts/AuthContext';
import api from '../services/api';

import { API_ENDPOINTS } from '../utils/constants';

function Settings() {
  const { user, logout } = useAuth();
  const [activeTab, setActiveTab] = useState('profile');
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState({ type: '', text: '' });
  
  // Profile form state
  const [profileForm, setProfileForm] = useState({
    first_name: '',
    last_name: '',
    email: ''
  });
  
  // Password form state
  const [passwordForm, setPasswordForm] = useState({
    current_password: '',
    new_password: '',
    confirm_password: ''
  });
  
  // Preferences state
  const [preferences, setPreferences] = useState({
    email_notifications: true,
    marketing_emails: false,
    security_alerts: true,
    product_updates: true,
    billing_notifications: true,
    theme: 'light',
    language: 'en',
    timezone: 'UTC'
  });
  
  // Security settings state
  const [securitySettings, setSecuritySettings] = useState({
    two_factor_enabled: false,
    login_notifications: true,
    session_timeout: 30
  });

  useEffect(() => {
    if (user) {
      setProfileForm({
        first_name: user.first_name,
        last_name: user.last_name,
        email: user.email
      });
    }
    fetchUserPreferences();
  }, [user]);

  const fetchUserPreferences = async () => {
    try {
      const response = await api.get('/api/v1/user/preferences');
      setPreferences(prev => ({ ...prev, ...response.data }));
    } catch (error) {
      console.error('Failed to fetch preferences:', error);
    }
  };

  const showMessage = (type, text) => {
    setMessage({ type, text });
    setTimeout(() => setMessage({ type: '', text: '' }), 5000);
  };

  const handleProfileUpdate = async (e) => {
    e.preventDefault();
    setLoading(true);
    
    try {
      await api.put(API_ENDPOINTS.AUTH.PROFILE, profileForm);
      showMessage('success', 'Profile updated successfully!');
    } catch (error) {
      showMessage('error', error.response?.data?.detail || 'Failed to update profile');
    } finally {
      setLoading(false);
    }
  };

  const handlePasswordChange = async (e) => {
    e.preventDefault();
    
    if (passwordForm.new_password !== passwordForm.confirm_password) {
      showMessage('error', 'New passwords do not match');
      return;
    }
    
    if (passwordForm.new_password.length < 8) {
      showMessage('error', 'Password must be at least 8 characters long');
      return;
    }
    
    setLoading(true);
    
    try {
      await api.put('/api/v1/user/password', {
        current_password: passwordForm.current_password,
        new_password: passwordForm.new_password
      });
      showMessage('success', 'Password changed successfully!');
      setPasswordForm({ current_password: '', new_password: '', confirm_password: '' });
    } catch (error) {
      showMessage('error', error.response?.data?.detail || 'Failed to change password');
    } finally {
      setLoading(false);
    }
  };

  const handlePreferencesUpdate = async () => {
    setLoading(true);
    
    try {
      await api.put('/api/v1/user/preferences', preferences);
      showMessage('success', 'Preferences updated successfully!');
    } catch (error) {
      showMessage('error', 'Failed to update preferences');
    } finally {
      setLoading(false);
    }
  };

  const handleResendVerification = async () => {
    setLoading(true);
    
    try {
      await api.post('/api/v1/auth/resend-verification');
      showMessage('success', 'Verification email sent! Check your inbox.');
    } catch (error) {
      showMessage('error', 'Failed to send verification email');
    } finally {
      setLoading(false);
    }
  };

  const handleDeleteAccount = async () => {
    const confirmation = window.prompt(
      'This action cannot be undone. Type "DELETE" to confirm account deletion:'
    );
    
    if (confirmation !== 'DELETE') {
      return;
    }
    
    setLoading(true);
    
    try {
      await api.delete('/api/v1/user/account');
      showMessage('success', 'Account deleted successfully');
      logout();
    } catch (error) {
      showMessage('error', 'Failed to delete account');
    } finally {
      setLoading(false);
    }
  };

  const handleExportData = async () => {
    try {
      const response = await api.get('/api/v1/user/export', { responseType: 'blob' });
      const url = window.URL.createObjectURL(new Blob([response.data]));
      const link = document.createElement('a');
      link.href = url;
      link.setAttribute('download', 'user_data.json');
      document.body.appendChild(link);
      link.click();
      link.remove();
      showMessage('success', 'Data export started');
    } catch (error) {
      showMessage('error', 'Failed to export data');
    }
  };

  return (
    <div className="settings-container">
      <div className="settings-header">
        <h1>Settings</h1>
        <p>Manage your account settings and preferences</p>
      </div>

      {message.text && (
        <div className={`message ${message.type}`}>
          {message.text}
        </div>
      )}

      <div className="settings-layout">
        <div className="settings-sidebar">
          <nav className="settings-nav">
            <button
              className={`nav-item ${activeTab === 'profile' ? 'active' : ''}`}
              onClick={() => setActiveTab('profile')}
            >
              <span className="nav-icon">👤</span>
              Profile
            </button>
            <button
              className={`nav-item ${activeTab === 'security' ? 'active' : ''}`}
              onClick={() => setActiveTab('security')}
            >
              <span className="nav-icon">🔒</span>
              Security
            </button>
            <button
              className={`nav-item ${activeTab === 'preferences' ? 'active' : ''}`}
              onClick={() => setActiveTab('preferences')}
            >
              <span className="nav-icon">⚙️</span>
              Preferences
            </button>
            <button
              className={`nav-item ${activeTab === 'notifications' ? 'active' : ''}`}
              onClick={() => setActiveTab('notifications')}
            >
              <span className="nav-icon">🔔</span>
              Notifications
            </button>
            <button
              className={`nav-item ${activeTab === 'privacy' ? 'active' : ''}`}
              onClick={() => setActiveTab('privacy')}
            >
              <span className="nav-icon">🛡️</span>
              Privacy
            </button>
            <button
              className={`nav-item ${activeTab === 'account' ? 'active' : ''}`}
              onClick={() => setActiveTab('account')}
            >
              <span className="nav-icon">⚠️</span>
              Account
            </button>
          </nav>
        </div>

        <div className="settings-content">
          {activeTab === 'profile' && (
            <div className="settings-section">
              <h2>Profile Information</h2>
              <p className="section-description">
                Update your personal information and profile details.
              </p>

              <div className="profile-section">
                <div className="avatar-section">
                  <div className="avatar-placeholder">
                    {user.first_name.charAt(0)}{user.last_name.charAt(0)}
                  </div>
                  <div className="avatar-info">
                    <h3>{user.first_name} {user.last_name}</h3>
                    <p>{user.email}</p>
                    <button className="btn-secondary">Change Avatar</button>
                  </div>
                </div>

                <form onSubmit={handleProfileUpdate} className="profile-form">
                  <div className="form-row">
                    <div className="form-group">
                      <label>First Name</label>
                      <input
                        type="text"
                        value={profileForm.first_name}
                        onChange={(e) => setProfileForm(prev => ({
                          ...prev,
                          first_name: e.target.value
                        }))}
                        className="form-input"
                        required
                      />
                    </div>
                    <div className="form-group">
                      <label>Last Name</label>
                      <input
                        type="text"
                        value={profileForm.last_name}
                        onChange={(e) => setProfileForm(prev => ({
                          ...prev,
                          last_name: e.target.value
                        }))}
                        className="form-input"
                        required
                      />
                    </div>
                  </div>

                  <div className="form-group">
                    <label>Email Address</label>
                    <input
                      type="email"
                      value={profileForm.email}
                      onChange={(e) => setProfileForm(prev => ({
                        ...prev,
                        email: e.target.value
                      }))}
                      className="form-input"
                      required
                    />
                    {!user.is_verified && (
                      <div className="email-verification">
                        <p className="unverified-notice">
                          ⚠️ Email not verified
                        </p>
                        <button
                          type="button"
                          onClick={handleResendVerification}
                          className="btn-link"
                        >
                          Resend verification email
                        </button>
                      </div>
                    )}
                  </div>

                  <button
                    type="submit"
                    disabled={loading}
                    className="btn-primary"
                  >
                    {loading ? 'Updating...' : 'Update Profile'}
                  </button>
                </form>
              </div>
            </div>
          )}

          {activeTab === 'security' && (
            <div className="settings-section">
              <h2>Security Settings</h2>
              <p className="section-description">
                Manage your password and security preferences.
              </p>

              <div className="security-section">
                <div className="security-item">
                  <h3>Change Password</h3>
                  <form onSubmit={handlePasswordChange} className="password-form">
                    <div className="form-group">
                      <label>Current Password</label>
                      <input
                        type="password"
                        value={passwordForm.current_password}
                        onChange={(e) => setPasswordForm(prev => ({
                          ...prev,
                          current_password: e.target.value
                        }))}
                        className="form-input"
                        required
                      />
                    </div>
                    <div className="form-group">
                      <label>New Password</label>
                      <input
                        type="password"
                        value={passwordForm.new_password}
                        onChange={(e) => setPasswordForm(prev => ({
                          ...prev,
                          new_password: e.target.value
                        }))}
                        className="form-input"
                        required
                      />
                    </div>
                    <div className="form-group">
                      <label>Confirm New Password</label>
                      <input
                        type="password"
                        value={passwordForm.confirm_password}
                        onChange={(e) => setPasswordForm(prev => ({
                          ...prev,
                          confirm_password: e.target.value
                        }))}
                        className="form-input"
                        required
                      />
                    </div>
                    <button
                      type="submit"
                      disabled={loading}
                      className="btn-primary"
                    >
                      {loading ? 'Changing...' : 'Change Password'}
                    </button>
                  </form>
                </div>

                <div className="security-item">
                  <h3>Two-Factor Authentication</h3>
                  <p>Add an extra layer of security to your account.</p>
                  <div className="toggle-setting">
                    <label className="toggle">
                      <input
                        type="checkbox"
                        checked={securitySettings.two_factor_enabled}
                        onChange={(e) => setSecuritySettings(prev => ({
                          ...prev,
                          two_factor_enabled: e.target.checked
                        }))}
                      />
                      <span className="toggle-slider"></span>
                    </label>
                    <span>Enable Two-Factor Authentication</span>
                  </div>
                </div>

                <div className="security-item">
                  <h3>Active Sessions</h3>
                  <p>Manage your active login sessions across devices.</p>
                  <div className="sessions-list">
                    <div className="session-item">
                      <div className="session-info">
                        <strong>Current Session</strong>
                        <p>Chrome on Windows • Active now</p>
                      </div>
                      <span className="session-status current">Current</span>
                    </div>
                  </div>
                  <button className="btn-secondary">Logout All Other Sessions</button>
                </div>
              </div>
            </div>
          )}

          {activeTab === 'preferences' && (
            <div className="settings-section">
              <h2>Preferences</h2>
              <p className="section-description">
                Customize your application experience.
              </p>

              <div className="preferences-section">
                <div className="preference-group">
                  <h3>Appearance</h3>
                  <div className="form-group">
                    <label>Theme</label>
                    <select
                      value={preferences.theme}
                      onChange={(e) => setPreferences(prev => ({
                        ...prev,
                        theme: e.target.value
                      }))}
                      className="form-select"
                    >
                      <option value="light">Light</option>
                      <option value="dark">Dark</option>
                      <option value="auto">Auto</option>
                    </select>
                  </div>
                </div>

                <div className="preference-group">
                  <h3>Localization</h3>
                  <div className="form-row">
                    <div className="form-group">
                      <label>Language</label>
                      <select
                        value={preferences.language}
                        onChange={(e) => setPreferences(prev => ({
                          ...prev,
                          language: e.target.value
                        }))}
                        className="form-select"
                      >
                        <option value="en">English</option>
                        <option value="es">Spanish</option>
                        <option value="fr">French</option>
                        <option value="de">German</option>
                      </select>
                    </div>
                    <div className="form-group">
                      <label>Timezone</label>
                      <select
                        value={preferences.timezone}
                        onChange={(e) => setPreferences(prev => ({
                          ...prev,
                          timezone: e.target.value
                        }))}
                        className="form-select"
                      >
                        <option value="UTC">UTC</option>
                        <option value="America/New_York">Eastern Time</option>
                        <option value="America/Chicago">Central Time</option>
                        <option value="America/Denver">Mountain Time</option>
                        <option value="America/Los_Angeles">Pacific Time</option>
                      </select>
                    </div>
                  </div>
                </div>

                <button
                  onClick={handlePreferencesUpdate}
                  disabled={loading}
                  className="btn-primary"
                >
                  {loading ? 'Saving...' : 'Save Preferences'}
                </button>
              </div>
            </div>
          )}

          {activeTab === 'notifications' && (
            <div className="settings-section">
              <h2>Notification Settings</h2>
              <p className="section-description">
                Choose how you want to be notified about account activity.
              </p>

              <div className="notifications-section">
                <div className="notification-group">
                  <h3>Email Notifications</h3>
                  
                  <div className="notification-item">
                    <div className="notification-info">
                      <strong>Security Alerts</strong>
                      <p>Get notified about security events and login attempts</p>
                    </div>
                    <label className="toggle">
                      <input
                        type="checkbox"
                        checked={preferences.security_alerts}
                        onChange={(e) => setPreferences(prev => ({
                          ...prev,
                          security_alerts: e.target.checked
                        }))}
                      />
                      <span className="toggle-slider"></span>
                    </label>
                  </div>

                  <div className="notification-item">
                    <div className="notification-info">
                      <strong>Billing Notifications</strong>
                      <p>Receive updates about payments, invoices, and billing</p>
                    </div>
                    <label className="toggle">
                      <input
                        type="checkbox"
                        checked={preferences.billing_notifications}
                        onChange={(e) => setPreferences(prev => ({
                          ...prev,
                          billing_notifications: e.target.checked
                        }))}
                      />
                      <span className="toggle-slider"></span>
                    </label>
                  </div>

                  <div className="notification-item">
                    <div className="notification-info">
                      <strong>Product Updates</strong>
                      <p>Stay informed about new features and improvements</p>
                    </div>
                    <label className="toggle">
                      <input
                        type="checkbox"
                        checked={preferences.product_updates}
                        onChange={(e) => setPreferences(prev => ({
                          ...prev,
                          product_updates: e.target.checked
                        }))}
                      />
                      <span className="toggle-slider"></span>
                    </label>
                  </div>

                  <div className="notification-item">
                    <div className="notification-info">
                      <strong>Marketing Emails</strong>
                      <p>Receive promotional content and special offers</p>
                    </div>
                    <label className="toggle">
                      <input
                        type="checkbox"
                        checked={preferences.marketing_emails}
                        onChange={(e) => setPreferences(prev => ({
                          ...prev,
                          marketing_emails: e.target.checked
                        }))}
                      />
                      <span className="toggle-slider"></span>
                    </label>
                  </div>
                </div>

                <button
                  onClick={handlePreferencesUpdate}
                  disabled={loading}
                  className="btn-primary"
                >
                  {loading ? 'Saving...' : 'Save Notification Settings'}
                </button>
              </div>
            </div>
          )}

          {activeTab === 'privacy' && (
            <div className="settings-section">
              <h2>Privacy & Data</h2>
              <p className="section-description">
                Manage your privacy settings and data usage.
              </p>

              <div className="privacy-section">
                <div className="privacy-item">
                  <h3>Data Export</h3>
                  <p>Download a copy of your data</p>
                  <button onClick={handleExportData} className="btn-secondary">
                    Export My Data
                  </button>
                </div>

                <div className="privacy-item">
                  <h3>Data Usage</h3>
                  <p>See how your data is being used and processed</p>
                  <button className="btn-secondary">View Data Usage Report</button>
                </div>

                <div className="privacy-item">
                  <h3>Third-party Access</h3>
                  <p>Manage applications that have access to your account</p>
                  <button className="btn-secondary">Manage Connected Apps</button>
                </div>
              </div>
            </div>
          )}

          {activeTab === 'account' && (
            <div className="settings-section">
              <h2>Account Management</h2>
              <p className="section-description">
                Manage your account settings and danger zone actions.
              </p>

              <div className="account-section">
                <div className="account-info">
                  <h3>Account Information</h3>
                  <div className="info-grid">
                    <div className="info-item">
                      <span className="info-label">Account ID:</span>
                      <span className="info-value">{user.id}</span>
                    </div>
                    <div className="info-item">
                      <span className="info-label">Member Since:</span>
                      <span className="info-value">
                        {new Date(user.created_at).toLocaleDateString()}
                      </span>
                    </div>
                    <div className="info-item">
                      <span className="info-label">Account Status:</span>
                      <span className={`status-badge ${user.is_verified ? 'verified' : 'unverified'}`}>
                        {user.is_verified ? 'Verified' : 'Unverified'}
                      </span>
                    </div>
                  </div>
                </div>

                <div className="danger-zone">
                  <h3>Danger Zone</h3>
                  <div className="danger-actions">
                    <div className="danger-item">
                      <div className="danger-info">
                        <strong>Delete Account</strong>
                        <p>Permanently delete your account and all associated data. This action cannot be undone.</p>
                      </div>
                      <button onClick={handleDeleteAccount} className="btn-danger">
                        Delete Account
                      </button>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

export default Settings;
