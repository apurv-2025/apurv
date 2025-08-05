// src/pages/Pricing.jsx
import React, { useState } from 'react';
import { useAuth } from '../hooks/useAuth';
import { useApi } from '../hooks/useApi';
import LoadingState from '../components/common/LoadingState';
import PricingCard from '../components/subscription/PricingCard';
import BillingToggle from '../components/subscription/BillingToggle';

import { API_ENDPOINTS } from '../utils/constants';

const Pricing = ({ onSelectPlan, currentPlanId }) => {
  const [billingCycle, setBillingCycle] = useState('monthly');
  const [processingPlan, setProcessingPlan] = useState(null);
  const { user } = useAuth();
  const { data: plans, loading } = useApi(API_ENDPOINTS.PRICING.PLANS);

  const handleSelectPlan = async (plan) => {
    if (!user || !onSelectPlan) return;
    
    setProcessingPlan(plan.id);
    try {
      await onSelectPlan(plan, billingCycle);
    } catch (error) {
      console.error('Failed to select plan:', error);
    } finally {
      setProcessingPlan(null);
    }
  };

  if (loading) {
    return <LoadingState message="Loading pricing plans..." />;
  }

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div className="text-center mb-12">
        <h2 className="text-4xl font-bold text-gray-900 mb-4">Choose Your Plan</h2>
        <p className="text-xl text-gray-600 mb-8">Select the perfect plan for your needs</p>
        
        <BillingToggle 
          billingCycle={billingCycle} 
          onBillingCycleChange={setBillingCycle} 
        />
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8 mb-16">
        {plans?.map((plan) => (
          <PricingCard
            key={plan.id}
            plan={plan}
            billingCycle={billingCycle}
            isCurrentPlan={currentPlanId === plan.id}
            isProcessing={processingPlan === plan.id}
            onSelectPlan={handleSelectPlan}
            user={user}
          />
        ))}
      </div>

      {/* Feature Comparison Table */}
      <div className="mt-16">
        <h3 className="text-2xl font-bold text-center text-gray-900 mb-8">Feature Comparison</h3>
        <div className="bg-white rounded-lg shadow overflow-hidden">
          <table className="min-w-full divide-y divide-gray-200">
            <thead className="bg-gray-50">
              <tr>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Feature
                </th>
                {plans?.map(plan => (
                  <th key={plan.id} className="px-6 py-3 text-center text-xs font-medium text-gray-500 uppercase tracking-wider">
                    {plan.display_name}
                  </th>
                ))}
              </tr>
            </thead>
            <tbody className="bg-white divide-y divide-gray-200">
              <tr>
                <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
                  Projects
                </td>
                {plans?.map(plan => (
                  <td key={plan.id} className="px-6 py-4 whitespace-nowrap text-sm text-center text-gray-900">
                    {plan.limits.projects === -1 ? '∞' : plan.limits.projects}
                  </td>
                ))}
              </tr>
              <tr className="bg-gray-50">
                <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
                  API Calls/month
                </td>
                {plans?.map(plan => (
                  <td key={plan.id} className="px-6 py-4 whitespace-nowrap text-sm text-center text-gray-900">
                    {plan.limits.api_calls === -1 ? '∞' : plan.limits.api_calls.toLocaleString()}
                  </td>
                ))}
              </tr>
              <tr>
                <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
                  Storage
                </td>
                {plans?.map(plan => (
                  <td key={plan.id} className="px-6 py-4 whitespace-nowrap text-sm text-center text-gray-900">
                    {plan.limits.storage_gb === -1 ? '∞' : `${plan.limits.storage_gb} GB`}
                  </td>
                ))}
              </tr>
              <tr className="bg-gray-50">
                <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
                  Team Members
                </td>
                {plans?.map(plan => (
                  <td key={plan.id} className="px-6 py-4 whitespace-nowrap text-sm text-center text-gray-900">
                    {plan.limits.team_members === -1 ? '∞' : plan.limits.team_members}
                  </td>
                ))}
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
};

export default Pricing;
