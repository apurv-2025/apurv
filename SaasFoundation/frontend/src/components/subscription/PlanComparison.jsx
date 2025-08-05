// src/components/subscription/PlanComparison.jsx
import React, { useState } from 'react';
import { CheckIcon, XMarkIcon } from '@heroicons/react/20/solid';
import { StarIcon } from '@heroicons/react/24/outline';
import { StarIcon as StarIconSolid } from '@heroicons/react/24/solid';
import Button from '../ui/Button';
import Badge from '../ui/Badge';
import { cn } from '../../utils/helpers';
import { formatCurrency } from '../../utils/formatters';

const PlanComparison = ({ 
  plans = [], 
  currentPlanId, 
  billingCycle = 'monthly', 
  onSelectPlan,
  user,
  loading = false,
  processingPlan = null 
}) => {
  const [expandedCategories, setExpandedCategories] = useState(new Set(['core', 'limits', 'support']));

  const toggleCategory = (category) => {
    const newExpanded = new Set(expandedCategories);
    if (newExpanded.has(category)) {
      newExpanded.delete(category);
    } else {
      newExpanded.add(category);
    }
    setExpandedCategories(newExpanded);
  };

  // Define feature categories and their features
  const featureCategories = [
    {
      id: 'core',
      name: 'Core Features',
      features: [
        {
          key: 'projects',
          name: 'Projects',
          type: 'limit',
          description: 'Number of projects you can create'
        },
        {
          key: 'api_calls',
          name: 'API Calls per Month',
          type: 'limit',
          description: 'Monthly API request limit'
        },
        {
          key: 'storage_gb',
          name: 'Storage',
          type: 'limit',
          description: 'File storage space in GB'
        },
        {
          key: 'team_members',
          name: 'Team Members',
          type: 'limit',
          description: 'Number of team members allowed'
        }
      ]
    },
    {
      id: 'advanced',
      name: 'Advanced Features',
      features: [
        {
          key: 'custom_domains',
          name: 'Custom Domains',
          type: 'boolean',
          description: 'Use your own domain'
        },
        {
          key: 'advanced_analytics',
          name: 'Advanced Analytics',
          type: 'boolean',
          description: 'Detailed usage and performance analytics'
        },
        {
          key: 'webhooks',
          name: 'Webhooks',
          type: 'boolean',
          description: 'Real-time event notifications'
        },
        {
          key: 'api_access',
          name: 'Full API Access',
          type: 'boolean',
          description: 'Complete API functionality'
        },
        {
          key: 'white_labeling',
          name: 'White Labeling',
          type: 'boolean',
          description: 'Remove branding and add your own'
        }
      ]
    },
    {
      id: 'integrations',
      name: 'Integrations',
      features: [
        {
          key: 'basic_integrations',
          name: 'Basic Integrations',
          type: 'boolean',
          description: 'Connect with popular tools'
        },
        {
          key: 'premium_integrations',
          name: 'Premium Integrations',
          type: 'boolean',
          description: 'Enterprise-grade integrations'
        },
        {
          key: 'custom_integrations',
          name: 'Custom Integrations',
          type: 'boolean',
          description: 'Build your own integrations'
        },
        {
          key: 'zapier_integration',
          name: 'Zapier Integration',
          type: 'boolean',
          description: 'Automate workflows with Zapier'
        }
      ]
    },
    {
      id: 'support',
      name: 'Support & Security',
      features: [
        {
          key: 'email_support',
          name: 'Email Support',
          type: 'boolean',
          description: '24/7 email support'
        },
        {
          key: 'priority_support',
          name: 'Priority Support',
          type: 'boolean',
          description: 'Faster response times'
        },
        {
          key: 'phone_support',
          name: 'Phone Support',
          type: 'boolean',
          description: 'Direct phone line access'
        },
        {
          key: 'dedicated_manager',
          name: 'Dedicated Account Manager',
          type: 'boolean',
          description: 'Personal account manager'
        },
        {
          key: 'sla_guarantee',
          name: 'SLA Guarantee',
          type: 'text',
          description: 'Uptime guarantee'
        },
        {
          key: 'security_compliance',
          name: 'Security Compliance',
          type: 'text',
          description: 'Security certifications'
        }
      ]
    }
  ];

  // Get feature value for a specific plan
  const getFeatureValue = (plan, feature) => {
    // Check plan limits first
    if (plan.limits && plan.limits[feature.key] !== undefined) {
      const value = plan.limits[feature.key];
      if (value === -1) return '∞';
      if (feature.key === 'storage_gb') return `${value} GB`;
      if (feature.key === 'api_calls') return value.toLocaleString();
      return value.toLocaleString();
    }

    // Handle boolean and text features based on plan type
    switch (feature.key) {
      case 'custom_domains':
        return ['professional', 'enterprise'].includes(plan.name);
      case 'advanced_analytics':
        return ['professional', 'enterprise'].includes(plan.name);
      case 'webhooks':
        return ['professional', 'enterprise'].includes(plan.name);
      case 'api_access':
        return plan.name !== 'free';
      case 'white_labeling':
        return plan.name === 'enterprise';
      case 'basic_integrations':
        return plan.name !== 'free';
      case 'premium_integrations':
        return ['professional', 'enterprise'].includes(plan.name);
      case 'custom_integrations':
        return plan.name === 'enterprise';
      case 'zapier_integration':
        return ['professional', 'enterprise'].includes(plan.name);
      case 'email_support':
        return true; // All plans have email support
      case 'priority_support':
        return ['professional', 'enterprise'].includes(plan.name);
      case 'phone_support':
        return plan.name === 'enterprise';
      case 'dedicated_manager':
        return plan.name === 'enterprise';
      case 'sla_guarantee':
        if (plan.name === 'enterprise') return '99.9%';
        if (plan.name === 'professional') return '99.5%';
        return '99%';
      case 'security_compliance':
        if (plan.name === 'enterprise') return 'SOC 2, GDPR, HIPAA';
        if (plan.name === 'professional') return 'SOC 2, GDPR';
        return 'GDPR';
      default:
        return false;
    }
  };

  // Render feature value
  const renderFeatureValue = (plan, feature) => {
    const value = getFeatureValue(plan, feature);

    if (feature.type === 'boolean') {
      return (
        <div className="flex justify-center">
          {value ? (
            <CheckIcon className="h-5 w-5 text-green-500" />
          ) : (
            <XMarkIcon className="h-5 w-5 text-gray-300" />
          )}
        </div>
      );
    }

    if (feature.type === 'limit') {
      return (
        <div className="text-center">
          <span className="font-semibold text-gray-900">{value}</span>
        </div>
      );
    }

    if (feature.type === 'text') {
      return (
        <div className="text-center">
          <span className="text-sm text-gray-700">{value}</span>
        </div>
      );
    }

    return null;
  };

  // Get plan pricing
  const getPlanPrice = (plan) => {
    return billingCycle === 'yearly' ? plan.price_yearly : plan.price_monthly;
  };

  // Check if plan is popular
  const isPopularPlan = (plan) => {
    return plan.name === 'professional';
  };

  // Check if plan is current
  const isCurrentPlan = (plan) => {
    return currentPlanId === plan.id;
  };

  if (!plans || plans.length === 0) {
    return (
      <div className="text-center py-12">
        <p className="text-gray-500">No plans available for comparison.</p>
      </div>
    );
  }

  return (
    <div className="space-y-8">
      {/* Header */}
      <div className="text-center">
        <h2 className="text-3xl font-bold text-gray-900 mb-4">
          Choose the Perfect Plan
        </h2>
        <p className="text-lg text-gray-600 max-w-3xl mx-auto">
          Compare our plans side by side to find the perfect fit for your needs. 
          All plans include our core features with varying limits and additional capabilities.
        </p>
      </div>

      {/* Plans Overview Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-12">
        {plans.map((plan) => {
          const price = getPlanPrice(plan);
          const isPopular = isPopularPlan(plan);
          const isCurrent = isCurrentPlan(plan);
          const isProcessing = processingPlan === plan.id;

          return (
            <div
              key={plan.id}
              className={cn(
                "relative bg-white rounded-lg shadow-sm border-2 p-6 transition-all duration-200",
                isPopular ? "border-blue-500 shadow-lg scale-105" : "border-gray-200",
                isCurrent ? "border-green-500" : ""
              )}
            >
              {isPopular && (
                <div className="absolute -top-3 left-1/2 transform -translate-x-1/2">
                  <Badge className="bg-blue-600 text-white flex items-center space-x-1">
                    <StarIconSolid className="h-3 w-3" />
                    <span>Most Popular</span>
                  </Badge>
                </div>
              )}

              {isCurrent && (
                <div className="absolute -top-3 right-4">
                  <Badge variant="success">Current Plan</Badge>
                </div>
              )}

              <div className="text-center">
                <h3 className="text-xl font-semibold text-gray-900 mb-2">
                  {plan.display_name}
                </h3>
                
                <div className="mb-4">
                  <span className="text-4xl font-bold text-gray-900">
                    {formatCurrency(price)}
                  </span>
                  {price > 0 && (
                    <span className="text-gray-600">
                      /{billingCycle === 'yearly' ? 'year' : 'month'}
                    </span>
                  )}
                </div>

                <p className="text-gray-600 text-sm mb-6">
                  {plan.description}
                </p>

                {user ? (
                  <Button
                    className="w-full"
                    variant={isCurrent ? 'secondary' : isPopular ? 'primary' : 'secondary'}
                    onClick={() => !isCurrent && onSelectPlan?.(plan)}
                    disabled={isCurrent || isProcessing || loading}
                    loading={isProcessing}
                  >
                    {isCurrent ? 'Current Plan' : `Choose ${plan.display_name}`}
                  </Button>
                ) : (
                  <Button 
                    className="w-full" 
                    onClick={() => window.location.href = '/register'}
                  >
                    Get Started
                  </Button>
                )}
              </div>
            </div>
          );
        })}
      </div>

      {/* Detailed Comparison Table */}
      <div className="bg-white rounded-lg shadow overflow-hidden">
        <div className="px-6 py-4 border-b border-gray-200">
          <h3 className="text-lg font-semibold text-gray-900">
            Detailed Feature Comparison
          </h3>
          <p className="text-sm text-gray-600 mt-1">
            Click on categories below to expand and see all features
          </p>
        </div>

        <div className="overflow-x-auto">
          <table className="min-w-full">
            {/* Table Header */}
            <thead className="bg-gray-50">
              <tr>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Features
                </th>
                {plans.map((plan) => (
                  <th
                    key={plan.id}
                    className="px-6 py-3 text-center text-xs font-medium text-gray-500 uppercase tracking-wider relative"
                  >
                    {plan.display_name}
                    {isPopularPlan(plan) && (
                      <StarIcon className="h-4 w-4 text-yellow-500 absolute -top-1 -right-1" />
                    )}
                  </th>
                ))}
              </tr>
            </thead>

            <tbody className="bg-white divide-y divide-gray-200">
              {featureCategories.map((category, categoryIndex) => (
                <React.Fragment key={category.id}>
                  {/* Category Header */}
                  <tr className="bg-gray-50">
                    <td 
                      className="px-6 py-3 cursor-pointer hover:bg-gray-100 transition-colors"
                      onClick={() => toggleCategory(category.id)}
                    >
                      <div className="flex items-center space-x-2">
                        <svg
                          className={cn(
                            "h-4 w-4 transform transition-transform",
                            expandedCategories.has(category.id) ? "rotate-90" : ""
                          )}
                          fill="none"
                          viewBox="0 0 24 24"
                          stroke="currentColor"
                        >
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
                        </svg>
                        <span className="font-medium text-gray-900">{category.name}</span>
                      </div>
                    </td>
                    {plans.map((plan) => (
                      <td key={plan.id} className="px-6 py-3 text-center">
                        <span className="text-xs text-gray-500">
                          {formatCurrency(getPlanPrice(plan))}
                          {getPlanPrice(plan) > 0 && `/${billingCycle === 'yearly' ? 'yr' : 'mo'}`}
                        </span>
                      </td>
                    ))}
                  </tr>

                  {/* Category Features */}
                  {expandedCategories.has(category.id) && category.features.map((feature, featureIndex) => (
                    <tr
                      key={feature.key}
                      className={featureIndex % 2 === 0 ? 'bg-white' : 'bg-gray-50'}
                    >
                      <td className="px-6 py-4">
                        <div>
                          <div className="font-medium text-gray-900">{feature.name}</div>
                          <div className="text-sm text-gray-500">{feature.description}</div>
                        </div>
                      </td>
                      {plans.map((plan) => (
                        <td key={plan.id} className="px-6 py-4">
                          {renderFeatureValue(plan, feature)}
                        </td>
                      ))}
                    </tr>
                  ))}
                </React.Fragment>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      {/* Call to Action */}
      <div className="text-center bg-gray-50 rounded-lg p-8">
        <h3 className="text-xl font-semibold text-gray-900 mb-4">
          Need Help Choosing?
        </h3>
        <p className="text-gray-600 mb-6 max-w-2xl mx-auto">
          Not sure which plan is right for you? Our team is here to help you find the perfect solution for your needs.
        </p>
        <div className="flex justify-center space-x-4">
          <Button variant="secondary">
            Contact Sales
          </Button>
          <Button>
            Start Free Trial
          </Button>
        </div>
      </div>
    </div>
  );
};

export default PlanComparison;
