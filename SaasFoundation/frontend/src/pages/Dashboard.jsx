import { Link } from 'react-router-dom';
import { Badge } from '../components/ui';
import { 
  DashboardCard, 
  StatusCard, 
  QuickActions 
} from '../components/dashboard/';
import Layout from '../components/layout/Layout';

import { LoadingState} from '../components/common';
import { useAuth } from '../hooks/useAuth';
import { useApi } from '../hooks/useApi';



import { formatCurrency,formatDate } from '../utils/formatters';

import { API_ENDPOINTS } from '../utils/constants';


const Dashboard = () => {
  const { user } = useAuth();
  const { data: subscriptionData, loading } = useApi(API_ENDPOINTS.SUBSCRIPTIONS.CURRENT);

  if (loading) {
    return <LoadingState message="Loading dashboard..." />;
  }

  return (
    <Layout>
    <div className="space-y-8">
      <div className="text-center">
        <h1 className="text-3xl font-bold text-gray-900">Welcome back, {user.first_name}!</h1>
        <p className="mt-2 text-lg text-gray-600">
          Here's your account overview and current subscription status.
        </p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {/* Account Status */}
        <StatusCard user={user} />

        {/* Subscription Card */}
        <DashboardCard title="Subscription">
          {subscriptionData ? (
            <div className="space-y-4">
              <div>
                <h4 className="text-lg font-semibold text-blue-600">
                  {subscriptionData.subscription.plan.display_name}
                </h4>
                <p className="text-xl font-bold text-gray-900">
                  {formatCurrency(
                    subscriptionData.subscription.billing_cycle === 'yearly'
                      ? subscriptionData.subscription.plan.price_yearly
                      : subscriptionData.subscription.plan.price_monthly
                  )}
                  <span className="text-sm font-normal text-gray-600">
                    /{subscriptionData.subscription.billing_cycle === 'yearly' ? 'year' : 'month'}
                  </span>
                </p>
              </div>
              
              <div className="space-y-2">
                <div className="flex justify-between items-center">
                  <span className="text-sm text-gray-600">Status:</span>
                  <Badge variant={subscriptionData.subscription.status === 'active' ? 'success' : 'warning'}>
                    {subscriptionData.subscription.status.toUpperCase()}
                  </Badge>
                </div>
                <div className="flex justify-between items-center">
                  <span className="text-sm text-gray-600">Period ends:</span>
                  <span className="text-sm text-gray-900">
                    {formatDate(subscriptionData.subscription.current_period_end)}
                  </span>
                </div>
              </div>

              {subscriptionData.subscription.cancel_at_period_end && (
                <div className="p-3 bg-red-50 border border-red-200 rounded-md">
                  <p className="text-sm text-red-800">
                    ⚠️ Subscription will cancel at period end
                  </p>
                </div>
              )}

              <div className="flex space-x-2">
                <Link to="/subscription" className="btn btn-primary flex-1">
                  Manage
                </Link>
                <Link to="/pricing" className="btn btn-secondary flex-1">
                  View Plans
                </Link>
              </div>
            </div>
          ) : (
            <div className="text-center py-4">
              <p className="text-gray-600 mb-4">No active subscription found.</p>
              <Link to="/pricing" className="btn btn-primary">
                View Plans
              </Link>
            </div>
          )}
        </DashboardCard>

        {/* Quick Actions */}
        <QuickActions />

        {/* Usage Overview */}
        {subscriptionData?.usage_metrics?.length > 0 && (
          <DashboardCard title="Usage Overview" className="md:col-span-2 lg:col-span-1">
            <div className="space-y-4">
              {subscriptionData.usage_metrics.slice(0, 3).map((metric, index) => (
                <div key={index} className="flex justify-between items-center">
                  <div className="text-sm font-medium text-gray-700">
                    {metric.metric_name.replace('_', ' ').toUpperCase()}
                  </div>
                  <div className="text-sm text-gray-900">
                    {metric.metric_value.toLocaleString()}
                    {subscriptionData.subscription.plan.limits[metric.metric_name] &&
                     subscriptionData.subscription.plan.limits[metric.metric_name] !== -1 && (
                      <span className="text-gray-500">
                        / {subscriptionData.subscription.plan.limits[metric.metric_name].toLocaleString()}
                      </span>
                    )}
                  </div>
                </div>
              ))}
              <Link to="/subscription" className="text-blue-600 hover:text-blue-700 text-sm font-medium">
                View detailed usage →
              </Link>
            </div>
          </DashboardCard>
        )}

        {/* Recent Activity */}
        <DashboardCard title="Recent Activity" className="md:col-span-2 lg:col-span-1">
          <div className="space-y-4">
            <div className="flex items-start space-x-3">
              <div className="w-2 h-2 bg-gray-400 rounded-full mt-2 flex-shrink-0"></div>
              <div>
                <p className="text-sm font-medium text-gray-900">Account created</p>
                <p className="text-sm text-gray-600">{formatDate(user.created_at)}</p>
              </div>
            </div>
            
            {user.is_verified && (
              <div className="flex items-start space-x-3">
                <div className="w-2 h-2 bg-green-500 rounded-full mt-2 flex-shrink-0"></div>
                <div>
                  <p className="text-sm font-medium text-gray-900">Email verified</p>
                  <p className="text-sm text-gray-600">Recently</p>
                </div>
              </div>
            )}
            
            {subscriptionData && (
              <div className="flex items-start space-x-3">
                <div className="w-2 h-2 bg-blue-500 rounded-full mt-2 flex-shrink-0"></div>
                <div>
                  <p className="text-sm font-medium text-gray-900">
                    Subscription: {subscriptionData.subscription.plan.display_name}
                  </p>
                  <p className="text-sm text-gray-600">
                    {formatDate(subscriptionData.subscription.created_at)}
                  </p>
                </div>
              </div>
            )}
          </div>
        </DashboardCard>
      </div>
    </div>
    </Layout>
  );
};

export default Dashboard;
