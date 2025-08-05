// frontend/src/components/Dashboard.js
import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';
import api from '../services/api';

import { API_ENDPOINTS } from '../utils/constants';

function Dashboard() {
  const { user } = useAuth();
  const [subscriptionData, setSubscriptionData] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchSubscriptionData = async () => {
      try {
        const response = await api.get(API_ENDPOINTS.SUBSCRIPTIONS.CURRENT);
        setSubscriptionData(response.data);
      } catch (error) {
        console.error('Failed to fetch subscription data:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchSubscriptionData();
  }, []);

  const formatCurrency = (amount) => {
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'USD'
    }).format(amount);
  };

  const formatDate = (dateString) => {
    return new Date(dateString).toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'long',
      day: 'numeric'
    });
  };

  if (loading) {
    return <div className="loading">Loading dashboard...</div>;
  }

  return (
    <div className="dashboard">
      <div className="dashboard-header">
        <h1>Welcome back, {user.first_name}!</h1>
        <p className="dashboard-subtitle">
          Here's your account overview and current subscription status.
        </p>
      </div>

      <div className="dashboard-grid">
        {/* Account Status Card */}
        <div className="dashboard-card">
          <h3>Account Status</h3>
          <div className="status-items">
            <div className="status-item">
              <span className="status-label">Email:</span>
              <span className="status-value">{user.email}</span>
            </div>
            <div className="status-item">
              <span className="status-label">Verification:</span>
              <span className={`status-badge ${user.is_verified ? 'verified' : 'unverified'}`}>
                {user.is_verified ? 'Verified' : 'Unverified'}
              </span>
            </div>
            <div className="status-item">
              <span className="status-label">Member since:</span>
              <span className="status-value">
                {formatDate(user.created_at)}
              </span>
            </div>
          </div>
          
          {!user.is_verified && (
            <div className="verification-notice">
              <p>⚠️ Please verify your email address to access all features.</p>
              <p>Check your inbox for the verification email.</p>
            </div>
          )}
        </div>

        {/* Subscription Card */}
        <div className="dashboard-card">
          <h3>Subscription</h3>
          {subscriptionData ? (
            <div className="subscription-info">
              <div className="plan-name">
                {subscriptionData.subscription.plan.display_name}
              </div>
              <div className="plan-price">
                {formatCurrency(
                  subscriptionData.subscription.billing_cycle === 'yearly'
                    ? subscriptionData.subscription.plan.price_yearly
                    : subscriptionData.subscription.plan.price_monthly
                )}
                <span className="billing-cycle">
                  /{subscriptionData.subscription.billing_cycle === 'yearly' ? 'year' : 'month'}
                </span>
              </div>
              <div className="plan-status">
                Status: <span className={`status-badge ${subscriptionData.subscription.status}`}>
                  {subscriptionData.subscription.status}
                </span>
              </div>
              <div className="plan-period">
                Current period ends: {formatDate(subscriptionData.subscription.current_period_end)}
              </div>
              {subscriptionData.subscription.cancel_at_period_end && (
                <div className="cancellation-notice">
                  ⚠️ Subscription will cancel at period end
                </div>
              )}
            </div>
          ) : (
            <div className="no-subscription">
              <p>No active subscription found.</p>
            </div>
          )}
          
          <div className="subscription-actions">
            <Link to="/subscription" className="btn-primary">
              Manage Subscription
            </Link>
            <Link to="/pricing" className="btn-secondary">
              View Plans
            </Link>
          </div>
        </div>

        {/* Usage Overview */}
        {subscriptionData?.usage_metrics?.length > 0 && (
          <div className="dashboard-card">
            <h3>Usage Overview</h3>
            <div className="usage-summary">
              {subscriptionData.usage_metrics.slice(0, 3).map((metric, index) => (
                <div key={index} className="usage-item">
                  <div className="usage-metric">
                    {metric.metric_name.replace('_', ' ').toUpperCase()}
                  </div>
                  <div className="usage-value">
                    {metric.metric_value.toLocaleString()}
                  </div>
                  {subscriptionData.subscription.plan.limits[metric.metric_name] && 
                   subscriptionData.subscription.plan.limits[metric.metric_name] !== -1 && (
                    <div className="usage-limit">
                      / {subscriptionData.subscription.plan.limits[metric.metric_name].toLocaleString()}
                    </div>
                  )}
                </div>
              ))}
            </div>
            <Link to="/subscription" className="view-details-link">
              View detailed usage →
            </Link>
          </div>
        )}

        {/* Recent Invoices */}
        {subscriptionData?.recent_invoices?.length > 0 && (
          <div className="dashboard-card">
            <h3>Recent Invoices</h3>
            <div className="invoices-summary">
              {subscriptionData.recent_invoices.slice(0, 3).map((invoice) => (
                <div key={invoice.id} className="invoice-item">
                  <div className="invoice-amount">
                    {formatCurrency(invoice.total_amount)}
                  </div>
                  <div className="invoice-date">
                    {formatDate(invoice.created_at)}
                  </div>
                  <div className={`invoice-status ${invoice.status}`}>
                    {invoice.status.toUpperCase()}
                  </div>
                </div>
              ))}
            </div>
            <Link to="/subscription" className="view-details-link">
              View all invoices →
            </Link>
          </div>
        )}

        {/* Quick Actions Card */}
        <div className="dashboard-card">
          <h3>Quick Actions</h3>
          <div className="action-buttons">
            <Link to="/subscription" className="action-btn">
              <span className="action-icon">💳</span>
              <span>Manage Subscription</span>
            </Link>
            <Link to="/pricing" className="action-btn">
              <span className="action-icon">📊</span>
              <span>View Pricing</span>
            </Link>
            <Link to="/settings" className="action-btn">
              <span className="action-icon">🔧</span>
              <span>Settings</span>
            </Link>
            <button className="action-btn">
              <span className="action-icon">💬</span>
              <span>Support</span>
            </button>
          </div>
        </div>

        {/* Recent Activity Card */}
        <div className="dashboard-card">
          <h3>Recent Activity</h3>
          <div className="activity-list">
            <div className="activity-item">
              <div className="activity-dot"></div>
              <div className="activity-content">
                <p>Account created</p>
                <span className="activity-time">
                  {formatDate(user.created_at)}
                </span>
              </div>
            </div>
            {user.is_verified && (
              <div className="activity-item">
                <div className="activity-dot verified"></div>
                <div className="activity-content">
                  <p>Email verified</p>
                  <span className="activity-time">Recently</span>
                </div>
              </div>
            )}
            {subscriptionData && (
              <div className="activity-item">
                <div className="activity-dot"></div>
                <div className="activity-content">
                  <p>Subscription: {subscriptionData.subscription.plan.display_name}</p>
                  <span className="activity-time">
                    {formatDate(subscriptionData.subscription.created_at)}
                  </span>
                </div>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}

export default Dashboard;
