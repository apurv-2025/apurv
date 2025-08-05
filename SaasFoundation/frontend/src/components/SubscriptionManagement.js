// frontend/src/components/SubscriptionManagement.js
import React, { useState, useEffect } from 'react';
import { useAuth } from '../contexts/AuthContext';
import api from '../services/api';
import Pricing from './Pricing';

import { API_ENDPOINTS } from '../utils/constants';

function SubscriptionManagement() {
  const [subscriptionData, setSubscriptionData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [activeTab, setActiveTab] = useState('overview');
  const [showPricing, setShowPricing] = useState(false);
  const { user } = useAuth();

  useEffect(() => {
    if (user) {
      fetchSubscriptionData();
    }
  }, [user]);

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

  const handlePlanChange = async (plan, billingCycle) => {
    try {
      await api.put(API_ENDPOINTS.SUBSCRIPTIONS.UPDATE, {
        plan_id: plan.id,
        billing_cycle: billingCycle
      });
      
      // Refresh subscription data
      await fetchSubscriptionData();
      setShowPricing(false);
      
      alert(`Successfully upgraded to ${plan.display_name}!`);
    } catch (error) {
      console.error('Failed to change plan:', error);
      alert('Failed to change plan. Please try again.');
    }
  };

  const handleCancelSubscription = async () => {
    if (!window.confirm('Are you sure you want to cancel your subscription? It will remain active until the end of your current billing period.')) {
      return;
    }

    try {
      await api.delete(`${API_ENDPOINTS.SUBSCRIPTIONS.CANCEL}/${subscriptionData.subscription.id}`);
      await fetchSubscriptionData();
      alert('Subscription cancelled. It will remain active until the end of your current period.');
    } catch (error) {
      console.error('Failed to cancel subscription:', error);
      alert('Failed to cancel subscription. Please try again.');
    }
  };

  const handlePayInvoice = async (invoiceId) => {
    try {
      await api.post(`/api/invoices/${invoiceId}/pay`);
      await fetchSubscriptionData();
      alert('Invoice paid successfully!');
    } catch (error) {
      console.error('Failed to pay invoice:', error);
      alert('Failed to pay invoice. Please try again.');
    }
  };

  const formatDate = (dateString) => {
    return new Date(dateString).toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'long',
      day: 'numeric'
    });
  };

  const formatCurrency = (amount) => {
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'USD'
    }).format(amount);
  };

  if (loading) {
    return <div className="loading">Loading subscription data...</div>;
  }

  if (!subscriptionData) {
    return (
      <div className="subscription-container">
        <div className="no-subscription">
          <h2>No Active Subscription</h2>
          <p>You don't have an active subscription. Choose a plan to get started!</p>
          <button className="btn-primary" onClick={() => setShowPricing(true)}>
            View Pricing Plans
          </button>
        </div>
        {showPricing && (
          <Pricing onSelectPlan={handlePlanChange} />
        )}
      </div>
    );
  }

  const { subscription, usage_metrics, recent_invoices, payment_methods } = subscriptionData;

  if (showPricing) {
    return (
      <div className="subscription-container">
        <div className="pricing-header">
          <button className="back-btn" onClick={() => setShowPricing(false)}>
            ← Back to Subscription
          </button>
        </div>
        <Pricing 
          onSelectPlan={handlePlanChange} 
          currentPlanId={subscription.plan.id}
        />
      </div>
    );
  }

  return (
    <div className="subscription-container">
      <div className="subscription-header">
        <h1>Subscription Management</h1>
        <div className="header-actions">
          <button className="btn-secondary" onClick={() => setShowPricing(true)}>
            Change Plan
          </button>
        </div>
      </div>

      <div className="subscription-tabs">
        <button
          className={`tab ${activeTab === 'overview' ? 'active' : ''}`}
          onClick={() => setActiveTab('overview')}
        >
          Overview
        </button>
        <button
          className={`tab ${activeTab === 'usage' ? 'active' : ''}`}
          onClick={() => setActiveTab('usage')}
        >
          Usage
        </button>
        <button
          className={`tab ${activeTab === 'billing' ? 'active' : ''}`}
          onClick={() => setActiveTab('billing')}
        >
          Billing
        </button>
        <button
          className={`tab ${activeTab === 'payment' ? 'active' : ''}`}
          onClick={() => setActiveTab('payment')}
        >
          Payment Methods
        </button>
      </div>

      <div className="tab-content">
        {activeTab === 'overview' && (
          <div className="overview-tab">
            <div className="subscription-summary">
              <div className="summary-card">
                <h3>Current Plan</h3>
                <div className="plan-info">
                  <div className="plan-name">{subscription.plan.display_name}</div>
                  <div className="plan-price">
                    {formatCurrency(
                      subscription.billing_cycle === 'yearly' 
                        ? subscription.plan.price_yearly 
                        : subscription.plan.price_monthly
                    )}
                    <span className="billing-cycle">/{subscription.billing_cycle === 'yearly' ? 'year' : 'month'}</span>
                  </div>
                  <div className="plan-status">
                    <span className={`status-badge ${subscription.status}`}>
                      {subscription.status.toUpperCase()}
                    </span>
                    {subscription.cancel_at_period_end && (
                      <span className="cancellation-notice">
                        Cancels on {formatDate(subscription.current_period_end)}
                      </span>
                    )}
                  </div>
                </div>
              </div>

              <div className="summary-card">
                <h3>Billing Period</h3>
                <div className="period-info">
                  <div className="period-dates">
                    <div>Started: {formatDate(subscription.current_period_start)}</div>
                    <div>Ends: {formatDate(subscription.current_period_end)}</div>
                  </div>
                  <div className="period-progress">
                    <div className="progress-bar">
                      <div 
                        className="progress-fill"
                        style={{
                          width: `${Math.min(100, Math.max(0, 
                            ((new Date() - new Date(subscription.current_period_start)) / 
                            (new Date(subscription.current_period_end) - new Date(subscription.current_period_start))) * 100
                          ))}%`
                        }}
                      ></div>
                    </div>
                  </div>
                </div>
              </div>

              <div className="summary-card">
                <h3>Plan Features</h3>
                <ul className="features-list">
                  {subscription.plan.features.map((feature, index) => (
                    <li key={index}>
                      <span className="feature-icon">✓</span>
                      {feature}
                    </li>
                  ))}
                </ul>
              </div>

              <div className="summary-card">
                <h3>Plan Limits</h3>
                <div className="limits-grid">
                  {Object.entries(subscription.plan.limits).map(([key, value]) => (
                    <div key={key} className="limit-item">
                      <span className="limit-label">
                        {key.replace('_', ' ').toUpperCase()}
                      </span>
                      <span className="limit-value">
                        {value === -1 ? 'Unlimited' : value.toLocaleString()}
                      </span>
                    </div>
                  ))}
                </div>
              </div>
            </div>

            <div className="subscription-actions">
              {!subscription.cancel_at_period_end && subscription.plan.name !== 'free' && (
                <button className="btn-danger" onClick={handleCancelSubscription}>
                  Cancel Subscription
                </button>
              )}
              <button className="btn-primary" onClick={() => setShowPricing(true)}>
                {subscription.plan.name === 'free' ? 'Upgrade Plan' : 'Change Plan'}
              </button>
            </div>
          </div>
        )}

        {activeTab === 'usage' && (
          <div className="usage-tab">
            <h3>Current Usage</h3>
            {usage_metrics.length > 0 ? (
              <div className="usage-metrics">
                {usage_metrics.map((metric, index) => (
                  <div key={index} className="metric-card">
                    <div className="metric-header">
                      <h4>{metric.metric_name.replace('_', ' ').toUpperCase()}</h4>
                      <span className="metric-value">{metric.metric_value.toLocaleString()}</span>
                    </div>
                    <div className="metric-period">
                      {formatDate(metric.period_start)} - {formatDate(metric.period_end)}
                    </div>
                    
                    {subscription.plan.limits[metric.metric_name] && 
                     subscription.plan.limits[metric.metric_name] !== -1 && (
                      <div className="usage-progress">
                        <div className="progress-bar">
                          <div 
                            className="progress-fill"
                            style={{
                              width: `${Math.min(100, 
                                (metric.metric_value / subscription.plan.limits[metric.metric_name]) * 100
                              )}%`
                            }}
                          ></div>
                        </div>
                        <div className="usage-text">
                          {metric.metric_value} / {subscription.plan.limits[metric.metric_name]} 
                          ({Math.round((metric.metric_value / subscription.plan.limits[metric.metric_name]) * 100)}%)
                        </div>
                      </div>
                    )}
                  </div>
                ))}
              </div>
            ) : (
              <div className="no-usage">
                <p>No usage data available for the current billing period.</p>
              </div>
            )}
          </div>
        )}

        {activeTab === 'billing' && (
          <div className="billing-tab">
            <h3>Recent Invoices</h3>
            {recent_invoices.length > 0 ? (
              <div className="invoices-list">
                {recent_invoices.map((invoice) => (
                  <div key={invoice.id} className="invoice-card">
                    <div className="invoice-header">
                      <div className="invoice-amount">
                        {formatCurrency(invoice.total_amount)}
                      </div>
                      <div className={`invoice-status ${invoice.status}`}>
                        {invoice.status.toUpperCase()}
                      </div>
                    </div>
                    <div className="invoice-details">
                      <div>Amount: {formatCurrency(invoice.amount)}</div>
                      <div>Tax: {formatCurrency(invoice.tax_amount)}</div>
                      <div>Due Date: {formatDate(invoice.due_date)}</div>
                      {invoice.paid_at && (
                        <div>Paid: {formatDate(invoice.paid_at)}</div>
                      )}
                    </div>
                    {invoice.status === 'pending' && (
                      <div className="invoice-actions">
                        <button 
                          className="btn-primary"
                          onClick={() => handlePayInvoice(invoice.id)}
                        >
                          Pay Now
                        </button>
                      </div>
                    )}
                  </div>
                ))}
              </div>
            ) : (
              <div className="no-invoices">
                <p>No invoices found.</p>
              </div>
            )}
          </div>
        )}

        {activeTab === 'payment' && (
          <div className="payment-tab">
            <h3>Payment Methods</h3>
            {payment_methods.length > 0 ? (
              <div className="payment-methods">
                {payment_methods.map((method) => (
                  <div key={method.id} className="payment-method-card">
                    <div className="method-info">
                      <div className="method-type">
                        {method.brand.toUpperCase()} •••• {method.last_four}
                      </div>
                      <div className="method-expiry">
                        Expires {method.exp_month}/{method.exp_year}
                      </div>
                      {method.is_default && (
                        <span className="default-badge">Default</span>
                      )}
                    </div>
                    <div className="method-actions">
                      <button className="btn-secondary">Edit</button>
                      <button className="btn-danger">Remove</button>
                    </div>
                  </div>
                ))}
                <button className="btn-primary add-payment-method">
                  Add Payment Method
                </button>
              </div>
            ) : (
              <div className="no-payment-methods">
                <p>No payment methods added.</p>
                <button className="btn-primary">Add Payment Method</button>
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
}

export default SubscriptionManagement;
