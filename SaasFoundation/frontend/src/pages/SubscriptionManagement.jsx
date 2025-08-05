// src/pages/SubscriptionManagement.jsx
import React, { useState } from 'react';
import { useAuth } from '../hooks/useAuth';
import { useApi } from '../hooks/useApi';
import api from '../services/api';
import LoadingState from '../components/common/LoadingState';
import Button from '../components/ui/Button';
import Badge from '../components/ui/Badge';
import { Card, CardContent, CardHeader, CardTitle } from '../components/ui/Card';
import UsageMetrics from '../components/subscription/UsageMetrics';
import InvoiceList from '../components/subscription/InvoiceList';
import Pricing from './Pricing';
import { formatCurrency, formatDate } from '../utils/formatters';

import { API_ENDPOINTS } from '../utils/constants';

const SubscriptionManagement = () => {
  const [activeTab, setActiveTab] = useState('overview');
  const [showPricing, setShowPricing] = useState(false);
  const { user } = useAuth();
  const { data: subscriptionData, loading, refetch } = useApi(API_ENDPOINTS.SUBSCRIPTIONS.CURRENT);


  const handlePlanChange = async (plan, billingCycle) => {
    try {
      await api.post(API_ENDPOINTS.SUBSCRIPTIONS.UPDATE, {
        plan_id: plan.id,
        billing_cycle: billingCycle
      });
      
      await refetch();
      setShowPricing(false);
      alert(`Successfully upgraded to ${plan.display_name}!`);
    } catch (error) {
      console.error('Failed to change plan:', error);
      alert('Failed to change plan. Please try again.');
    }
  };

  const handleCancelSubscription = async () => {
    if (!window.confirm('Are you sure you want to cancel your subscription?')) {
      return;
    }

    try {
      await api.delete(`${API_ENDPOINTS.SUBSCRIPTIONS.CANCEL}/${subscriptionData.subscription.id}`);
      await refetch();
      alert('Subscription cancelled. It will remain active until the end of your current period.');
    } catch (error) {
      console.error('Failed to cancel subscription:', error);
      alert('Failed to cancel subscription. Please try again.');
    }
  };

  const handlePayInvoice = async (invoiceId) => {
    try {
      await api.post(`/api/invoices/${invoiceId}/pay`);
      await refetch();
      alert('Invoice paid successfully!');
    } catch (error) {
      console.error('Failed to pay invoice:', error);
      alert('Failed to pay invoice. Please try again.');
    }
  };

  if (loading) {
    return <LoadingState message="Loading subscription data..." />;
  }

  if (!subscriptionData) {
    return (
      <div className="text-center py-12">
        <h2 className="text-2xl font-bold text-gray-900 mb-4">No Active Subscription</h2>
        <p className="text-gray-600 mb-8">You don't have an active subscription. Choose a plan to get started!</p>
        <Button onClick={() => setShowPricing(true)}>
          View Pricing Plans
        </Button>
        {showPricing && (
          <div className="mt-8">
            <Pricing onSelectPlan={handlePlanChange} />
          </div>
        )}
      </div>
    );
  }

  if (showPricing) {
    return (
      <div className="space-y-6">
        <div className="flex items-center space-x-4">
          <Button variant="secondary" onClick={() => setShowPricing(false)}>
            ← Back to Subscription
          </Button>
        </div>
        <Pricing 
          onSelectPlan={handlePlanChange} 
          currentPlanId={subscriptionData.subscription.plan.id}
        />
      </div>
    );
  }

  const { subscription, usage_metrics, recent_invoices, payment_methods } = subscriptionData;

  const tabs = [
    { id: 'overview', label: 'Overview' },
    { id: 'usage', label: 'Usage' },
    { id: 'billing', label: 'Billing' },
    { id: 'payment', label: 'Payment Methods' }
  ];

  return (
    <div className="space-y-8">
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">Subscription Management</h1>
          <p className="text-gray-600 mt-2">Manage your subscription and billing</p>
        </div>
        <Button onClick={() => setShowPricing(true)}>
          Change Plan
        </Button>
      </div>

      {/* Tab Navigation */}
      <div className="border-b border-gray-200">
        <nav className="-mb-px flex space-x-8">
          {tabs.map((tab) => (
            <button
              key={tab.id}
              onClick={() => setActiveTab(tab.id)}
              className={`py-2 px-1 border-b-2 font-medium text-sm ${
                activeTab === tab.id
                  ? 'border-blue-500 text-blue-600'
                  : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
              }`}
            >
              {tab.label}
            </button>
          ))}
        </nav>
      </div>

      {/* Tab Content */}
      <div className="mt-8">
        {activeTab === 'overview' && (
          <div className="space-y-8">
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {/* Current Plan */}
              <Card>
                <CardHeader>
                  <CardTitle>Current Plan</CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="space-y-4">
                    <div>
                      <h4 className="text-lg font-semibold text-blue-600">
                        {subscription.plan.display_name}
                      </h4>
                      <p className="text-2xl font-bold text-gray-900">
                        {formatCurrency(
                          subscription.billing_cycle === 'yearly' 
                            ? subscription.plan.price_yearly 
                            : subscription.plan.price_monthly
                        )}
                        <span className="text-sm font-normal text-gray-600">
                          /{subscription.billing_cycle === 'yearly' ? 'year' : 'month'}
                        </span>
                      </p>
                    </div>
                    
                    <div className="space-y-2">
                      <div className="flex justify-between">
                        <span className="text-sm text-gray-600">Status:</span>
                        <Badge variant={subscription.status === 'active' ? 'success' : 'warning'}>
                          {subscription.status.toUpperCase()}
                        </Badge>
                      </div>
                      
                      {subscription.cancel_at_period_end && (
                        <div className="p-3 bg-red-50 border border-red-200 rounded-md">
                          <p className="text-sm text-red-800">
                            Cancels on {formatDate(subscription.current_period_end)}
                          </p>
                        </div>
                      )}
                    </div>
                  </div>
                </CardContent>
              </Card>

              {/* Billing Period */}
              <Card>
                <CardHeader>
                  <CardTitle>Billing Period</CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="space-y-4">
                    <div className="space-y-2">
                      <div className="flex justify-between text-sm">
                        <span className="text-gray-600">Started:</span>
                        <span>{formatDate(subscription.current_period_start)}</span>
                      </div>
                      <div className="flex justify-between text-sm">
                        <span className="text-gray-600">Ends:</span>
                        <span>{formatDate(subscription.current_period_end)}</span>
                      </div>
                    </div>
                    
                    <div className="w-full bg-gray-200 rounded-full h-2">
                      <div 
                        className="bg-blue-600 h-2 rounded-full transition-all duration-300"
                        style={{
                          width: `${Math.min(100, Math.max(0, 
                            ((new Date() - new Date(subscription.current_period_start)) / 
                            (new Date(subscription.current_period_end) - new Date(subscription.current_period_start))) * 100
                          ))}%`
                        }}
                      />
                    </div>
                  </div>
                </CardContent>
              </Card>

              {/* Plan Features */}
              <Card>
                <CardHeader>
                  <CardTitle>Plan Features</CardTitle>
                </CardHeader>
                <CardContent>
                  <ul className="space-y-2">
                    {subscription.plan.features.map((feature, index) => (
                      <li key={index} className="flex items-center text-sm">
                        <span className="text-green-500 mr-2">✓</span>
                        {feature}
                      </li>
                    ))}
                  </ul>
                </CardContent>
              </Card>
            </div>

            {/* Action Buttons */}
            <div className="flex space-x-4">
              {!subscription.cancel_at_period_end && subscription.plan.name !== 'free' && (
                <Button variant="danger" onClick={handleCancelSubscription}>
                  Cancel Subscription
                </Button>
              )}
              <Button onClick={() => setShowPricing(true)}>
                {subscription.plan.name === 'free' ? 'Upgrade Plan' : 'Change Plan'}
              </Button>
            </div>
          </div>
        )}

        {activeTab === 'usage' && (
          <div>
            <h3 className="text-xl font-semibold text-gray-900 mb-6">Current Usage</h3>
            <UsageMetrics 
              usageMetrics={usage_metrics} 
              planLimits={subscription.plan.limits} 
            />
          </div>
        )}

        {activeTab === 'billing' && (
          <div>
            <h3 className="text-xl font-semibold text-gray-900 mb-6">Recent Invoices</h3>
            <InvoiceList 
              invoices={recent_invoices} 
              onPayInvoice={handlePayInvoice} 
            />
          </div>
        )}

        {activeTab === 'payment' && (
          <div>
            <h3 className="text-xl font-semibold text-gray-900 mb-6">Payment Methods</h3>
            {payment_methods?.length > 0 ? (
              <div className="space-y-4">
                {payment_methods.map((method) => (
                  <Card key={method.id}>
                    <CardContent className="pt-6">
                      <div className="flex justify-between items-center">
                        <div>
                          <p className="font-medium">
                            {method.brand.toUpperCase()} •••• {method.last_four}
                          </p>
                          <p className="text-sm text-gray-600">
                            Expires {method.exp_month}/{method.exp_year}
                          </p>
                          {method.is_default && (
                            <Badge variant="success" className="mt-1">Default</Badge>
                          )}
                        </div>
                        <div className="flex space-x-2">
                          <Button variant="secondary" size="sm">Edit</Button>
                          <Button variant="danger" size="sm">Remove</Button>
                        </div>
                      </div>
                    </CardContent>
                  </Card>
                ))}
                <Button className="w-full">Add Payment Method</Button>
              </div>
            ) : (
              <div className="text-center py-8">
                <p className="text-gray-600 mb-4">No payment methods added.</p>
                <Button>Add Payment Method</Button>
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
};

export default SubscriptionManagement;
