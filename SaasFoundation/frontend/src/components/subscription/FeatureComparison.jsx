/ src/components/subscription/FeatureComparison.jsx
import React from 'react';
import { CheckIcon, XMarkIcon } from '@heroicons/react/20/solid';
import { Card, CardContent, CardHeader, CardTitle } from '../ui/Card';
import Badge from '../ui/Badge';
import { cn } from '../../utils/helpers';

const FeatureComparison = ({ plans = [], className }) => {
  // Comprehensive feature categories
  const featureCategories = [
    {
      name: 'Core Limits',
      features: [
        {
          key: 'projects',
          name: 'Projects',
          description: 'Number of projects you can create and manage'
        },
        {
          key: 'api_calls',
          name: 'API Calls per Month',
          description: 'Monthly limit for API requests'
        },
        {
          key: 'storage_gb',
          name: 'Storage Space',
          description: 'File storage space in gigabytes'
        },
        {
          key: 'team_members',
          name: 'Team Members',
          description: 'Number of users that can access your account'
        },
        {
          key: 'bandwidth_gb',
          name: 'Bandwidth per Month',
          description: 'Monthly data transfer limit'
        }
      ]
    },
    {
      name: 'Features & Functionality',
      features: [
        {
          key: 'custom_domains',
          name: 'Custom Domains',
          description: 'Use your own domain name'
        },
        {
          key: 'ssl_certificates',
          name: 'SSL Certificates',
          description: 'Secure HTTPS connections'
        },
        {
          key: 'advanced_analytics',
          name: 'Advanced Analytics',
          description: 'Detailed usage and performance metrics'
        },
        {
          key: 'real_time_monitoring',
          name: 'Real-time Monitoring',
          description: 'Live system monitoring and alerts'
        },
        {
          key: 'automated_backups',
          name: 'Automated Backups',
          description: 'Automatic data backup and recovery'
        },
        {
          key: 'version_control',
          name: 'Version Control',
          description: 'Track and manage code versions'
        }
      ]
    },
    {
      name: 'Integrations & API',
      features: [
        {
          key: 'rest_api',
          name: 'REST API Access',
          description: 'Full REST API functionality'
        },
        {
          key: 'webhooks',
          name: 'Webhooks',
          description: 'Real-time event notifications'
        },
        {
          key: 'third_party_integrations',
          name: 'Third-party Integrations',
          description: 'Connect with external services'
        },
        {
          key: 'zapier_integration',
          name: 'Zapier Integration',
          description: 'Automate workflows with 5000+ apps'
        },
        {
          key: 'api_rate_limits',
          name: 'Higher API Rate Limits',
          description: 'Increased request rate limits'
        },
        {
          key: 'custom_integrations',
          name: 'Custom Integrations',
          description: 'Build your own integrations'
        }
      ]
    },
    {
      name: 'Security & Compliance',
      features: [
        {
          key: 'two_factor_auth',
          name: 'Two-Factor Authentication',
          description: 'Enhanced account security'
        },
        {
          key: 'sso_integration',
          name: 'SSO Integration',
          description: 'Single Sign-On support'
        },
        {
          key: 'audit_logs',
          name: 'Audit Logs',
          description: 'Detailed activity logging'
        },
        {
          key: 'gdpr_compliance',
          name: 'GDPR Compliance',
          description: 'European data protection compliance'
        },
        {
          key: 'hipaa_compliance',
          name: 'HIPAA Compliance',
          description: 'Healthcare data protection'
        },
        {
          key: 'soc2_compliance',
          name: 'SOC 2 Compliance',
          description: 'Security and availability controls'
        }
      ]
    },
    {
      name: 'Support & SLA',
      features: [
        {
          key: 'email_support',
          name: 'Email Support',
          description: '24/7 email support'
        },
        {
          key: 'priority_support',
          name: 'Priority Support',
          description: 'Faster response times'
        },
        {
          key: 'phone_support',
          name: 'Phone Support',
          description: 'Direct phone line access'
        },
        {
          key: 'dedicated_manager',
          name: 'Dedicated Account Manager',
          description: 'Personal account manager'
        },
        {
          key: 'sla_99_9',
          name: '99.9% Uptime SLA',
          description: 'Guaranteed service availability'
        },
        {
          key: 'onboarding_support',
          name: 'Onboarding Support',
          description: 'Guided setup and training'
        }
      ]
    },
    {
      name: 'Advanced Features',
      features: [
        {
          key: 'white_labeling',
          name: 'White Labeling',
          description: 'Remove our branding, add yours'
        },
        {
          key: 'custom_branding',
          name: 'Custom Branding',
          description: 'Fully customizable interface'
        },
        {
          key: 'advanced_reporting',
          name: 'Advanced Reporting',
          description: 'Comprehensive business reports'
        },
        {
          key: 'multi_environment',
          name: 'Multiple Environments',
          description: 'Dev, staging, and production environments'
        },
        {
          key: 'load_balancing',
          name: 'Load Balancing',
          description: 'Distribute traffic across servers'
        },
        {
          key: 'cdn_access',
          name: 'CDN Access',
          description: 'Global content delivery network'
        }
      ]
    }
  ];

  // Get feature value for a plan
  const getFeatureValue = (plan, featureKey) => {
    // Check if it's a limit-based feature
    if (plan.limits && plan.limits[featureKey] !== undefined) {
      const value = plan.limits[featureKey];
      if (value === -1) return '∞';
      if (featureKey === 'storage_gb' || featureKey === 'bandwidth_gb') {
        return `${value} GB`;
      }
      return value.toLocaleString();
    }

    // Boolean features based on plan type
    const planTier = plan.name; // 'free', 'starter', 'professional', 'enterprise'
    
    switch (featureKey) {
      // Core features
      case 'custom_domains':
        return ['professional', 'enterprise'].includes(planTier);
      case 'ssl_certificates':
        return planTier !== 'free';
      case 'advanced_analytics':
        return ['professional', 'enterprise'].includes(planTier);
      case 'real_time_monitoring':
        return ['professional', 'enterprise'].includes(planTier);
      case 'automated_backups':
        return planTier !== 'free';
      case 'version_control':
        return planTier !== 'free';

      // Integration features
      case 'rest_api':
        return planTier !== 'free';
      case 'webhooks':
        return ['professional', 'enterprise'].includes(planTier);
      case 'third_party_integrations':
        return planTier !== 'free';
      case 'zapier_integration':
        return ['professional', 'enterprise'].includes(planTier);
      case 'api_rate_limits':
        return ['professional', 'enterprise'].includes(planTier);
      case 'custom_integrations':
        return planTier === 'enterprise';

      // Security features
      case 'two_factor_auth':
        return planTier !== 'free';
      case 'sso_integration':
        return ['professional', 'enterprise'].includes(planTier);
      case 'audit_logs':
        return ['professional', 'enterprise'].includes(planTier);
      case 'gdpr_compliance':
        return true; // All plans
      case 'hipaa_compliance':
        return planTier === 'enterprise';
      case 'soc2_compliance':
        return planTier === 'enterprise';

      // Support features
      case 'email_support':
        return true; // All plans
      case 'priority_support':
        return ['professional', 'enterprise'].includes(planTier);
      case 'phone_support':
        return planTier === 'enterprise';
      case 'dedicated_manager':
        return planTier === 'enterprise';
      case 'sla_99_9':
        return planTier === 'enterprise';
      case 'onboarding_support':
        return ['professional', 'enterprise'].includes(planTier);

      // Advanced features
      case 'white_labeling':
        return planTier === 'enterprise';
      case 'custom_branding':
        return planTier === 'enterprise';
      case 'advanced_reporting':
        return ['professional', 'enterprise'].includes(planTier);
      case 'multi_environment':
        return ['professional', 'enterprise'].includes(planTier);
      case 'load_balancing':
        return planTier === 'enterprise';
      case 'cdn_access':
        return ['professional', 'enterprise'].includes(planTier);

      default:
        return false;
    }
  };

  // Render feature value
  const renderFeatureValue = (plan, featureKey) => {
    const value = getFeatureValue(plan, featureKey);

    if (typeof value === 'boolean') {
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

    return (
      <div className="text-center">
        <span className="font-medium text-gray-900">{value}</span>
      </div>
    );
  };

  // Get plan badge color
  const getPlanBadgeVariant = (planName) => {
    switch (planName) {
      case 'free': return 'secondary';
      case 'starter': return 'info';
      case 'professional': return 'success';
      case 'enterprise': return 'warning';
      default: return 'secondary';
    }
  };

  if (!plans || plans.length === 0) {
    return (
      <Card className={className}>
        <CardContent className="text-center py-8">
          <p className="text-gray-500">No plans available for comparison.</p>
        </CardContent>
      </Card>
    );
  }

  return (
    <Card className={className}>
      <CardHeader>
        <CardTitle className="text-center">Complete Feature Comparison</CardTitle>
        <p className="text-center text-gray-600">
          Compare all features across our plans to find the perfect fit
        </p>
      </CardHeader>
      <CardContent>
        <div className="overflow-x-auto">
          <table className="min-w-full">
            {/* Table Header */}
            <thead className="bg-gray-50">
              <tr>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider sticky left-0 bg-gray-50 z-10">
                  Features
                </th>
                {plans.map((plan) => (
                  <th
                    key={plan.id}
                    className="px-6 py-3 text-center text-xs font-medium text-gray-500 uppercase tracking-wider"
                  >
                    <div className="space-y-2">
                      <div className="font-semibold text-gray-900">
                        {plan.display_name}
                      </div>
                      <Badge variant={getPlanBadgeVariant(plan.name)}>
                        {plan.name.charAt(0).toUpperCase() + plan.name.slice(1)}
                      </Badge>
                    </div>
                  </th>
                ))}
              </tr>
            </thead>

            <tbody className="bg-white divide-y divide-gray-200">
              {featureCategories.map((category, categoryIndex) => (
                <React.Fragment key={category.name}>
                  {/* Category Header */}
                  <tr className="bg-gray-100">
                    <td
                      className="px-6 py-4 font-bold text-gray-900 sticky left-0 bg-gray-100 z-10"
                      colSpan={plans.length + 1}
                    >
                      {category.name}
                    </td>
                  </tr>

                  {/* Category Features */}
                  {category.features.map((feature, featureIndex) => (
                    <tr
                      key={feature.key}
                      className={cn(
                        "hover:bg-gray-50 transition-colors",
                        featureIndex % 2 === 0 ? 'bg-white' : 'bg-gray-50'
                      )}
                    >
                      <td className="px-6 py-4 sticky left-0 bg-inherit z-10">
                        <div>
                          <div className="font-medium text-gray-900">
                            {feature.name}
                          </div>
                          <div className="text-sm text-gray-500">
                            {feature.description}
                          </div>
                        </div>
                      </td>
                      {plans.map((plan) => (
                        <td key={plan.id} className="px-6 py-4 text-center">
                          {renderFeatureValue(plan, feature.key)}
                        </td>
                      ))}
                    </tr>
                  ))}
                </React.Fragment>
              ))}
            </tbody>
          </table>
        </div>

        {/* Footer Note */}
        <div className="mt-8 p-4 bg-gray-50 rounded-lg">
          <p className="text-sm text-gray-600 text-center">
            <strong>Note:</strong> All plans include our core platform features. 
            Contact our sales team for custom enterprise solutions and volume discounts.
          </p>
        </div>
      </CardContent>
    </Card>
  );
};

export default FeatureComparison;
