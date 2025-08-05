// src/components/subscription/SimplePlanComparison.jsx
import React from 'react';
import { CheckIcon, XMarkIcon } from '@heroicons/react/20/solid';
import Button from '../ui/Button';
import Badge from '../ui/Badge';
import { cn } from '../../utils/helpers';
import { formatCurrency } from '../../utils/formatters';

const SimplePlanComparison = ({ 
  plans = [], 
  currentPlanId, 
  billingCycle = 'monthly', 
  onSelectPlan,
  user,
  className 
}) => {
  // Core features to compare
  const coreFeatures = [
    { key: 'projects', name: 'Projects', type: 'limit' },
    { key: 'api_calls', name: 'API Calls/month', type: 'limit' },
    { key: 'storage_gb', name: 'Storage (GB)', type: 'limit' },
    { key: 'team_members', name: 'Team Members', type: 'limit' },
    { key: 'support', name: 'Support', type: 'text' },
    { key: 'analytics', name: 'Analytics', type: 'boolean' }
  ];

  const getFeatureValue = (plan, feature) => {
    if (plan.limits && plan.limits[feature.key] !== undefined) {
      const value = plan.limits[feature.key];
      return value === -1 ? '∞' : value.toLocaleString();
    }

    switch (feature.key) {
      case 'support':
        if (plan.name === 'enterprise') return 'Phone + Email';
        if (plan.name === 'professional') return 'Priority Email';
        return 'Email';
      case 'analytics':
        return ['professional', 'enterprise'].includes(plan.name);
      default:
        return false;
    }
  };

  const renderFeatureValue = (plan, feature) => {
    const value = getFeatureValue(plan, feature);

    if (feature.type === 'boolean') {
      return (
        <div className="flex justify-center">
          {value ? (
            <CheckIcon className="h-4 w-4 text-green-500" />
          ) : (
            <XMarkIcon className="h-4 w-4 text-gray-300" />
          )}
        </div>
      );
    }

    return (
      <div className="text-center text-sm font-medium text-gray-900">
        {value}
      </div>
    );
  };

  const getPlanPrice = (plan) => {
    return billingCycle === 'yearly' ? plan.price_yearly : plan.price_monthly;
  };

  const isPopularPlan = (plan) => plan.name === 'professional';
  const isCurrentPlan = (plan) => currentPlanId === plan.id;

  return (
    <div className={cn("bg-white rounded-lg shadow overflow-hidden", className)}>
      <div className="overflow-x-auto">
        <table className="min-w-full">
          {/* Header with Plan Names and Prices */}
          <thead>
            <tr className="border-b border-gray-200">
              <th className="px-4 py-6 text-left">
                <span className="text-lg font-semibold text-gray-900">Features</span>
              </th>
              {plans.map((plan) => {
                const price = getPlanPrice(plan);
                const isPopular = isPopularPlan(plan);
                const isCurrent = isCurrentPlan(plan);

                return (
                  <th key={plan.id} className="px-4 py-6 text-center relative">
                    {isPopular && (
                      <Badge className="absolute -top-2 left-1/2 transform -translate-x-1/2 bg-blue-600 text-white">
                        Popular
                      </Badge>
                    )}
                    
                    <div className="space-y-2">
                      <div className="font-semibold text-gray-900">{plan.display_name}</div>
                      <div className="text-2xl font-bold text-gray-900">
                        {formatCurrency(price)}
                        {price > 0 && (
                          <span className="text-sm font-normal text-gray-600">
                            /{billingCycle === 'yearly' ? 'year' : 'month'}
                          </span>
                        )}
                      </div>
                      
                      {user ? (
                        <Button
                          size="sm"
                          variant={isCurrent ? 'secondary' : isPopular ? 'primary' : 'secondary'}
                          onClick={() => !isCurrent && onSelectPlan?.(plan)}
                          disabled={isCurrent}
                          className="w-full"
                        >
                          {isCurrent ? 'Current' : 'Choose'}
                        </Button>
                      ) : (
                        <Button 
                          size="sm"
                          className="w-full"
                          onClick={() => window.location.href = '/register'}
                        >
                          Sign Up
                        </Button>
                      )}
                    </div>
                  </th>
                );
              })}
            </tr>
          </thead>

          {/* Feature Rows */}
          <tbody className="divide-y divide-gray-200">
            {coreFeatures.map((feature, index) => (
              <tr key={feature.key} className={index % 2 === 0 ? 'bg-white' : 'bg-gray-50'}>
                <td className="px-4 py-3 text-sm font-medium text-gray-900">
                  {feature.name}
                </td>
                {plans.map((plan) => (
                  <td key={plan.id} className="px-4 py-3">
                    {renderFeatureValue(plan, feature)}
                  </td>
                ))}
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default SimplePlanComparison;
