// src/components/dashboard/ActivityCard.jsx
import React from 'react';
import DashboardCard from './DashboardCard';
import { formatDate } from '../../utils/formatters';

const ActivityCard = ({ user, subscription }) => {
  const activities = [
    {
      type: 'account_created',
      message: 'Account created',
      date: user.created_at,
      status: 'completed'
    },
    ...(user.is_verified ? [{
      type: 'email_verified',
      message: 'Email verified',
      date: user.updated_at || user.created_at,
      status: 'verified'
    }] : []),
    ...(subscription ? [{
      type: 'subscription_created',
      message: `Subscription: ${subscription.plan.display_name}`,
      date: subscription.created_at,
      status: 'active'
    }] : [])
  ];

  return (
    <DashboardCard title="Recent Activity">
      <div className="space-y-4">
        {activities.map((activity, index) => (
          <div key={index} className="flex items-start space-x-3">
            <div className={`w-2 h-2 rounded-full mt-2 flex-shrink-0 ${
              activity.status === 'verified' ? 'bg-green-500' :
              activity.status === 'active' ? 'bg-blue-500' :
              'bg-gray-400'
            }`} />
            <div className="flex-1 min-w-0">
              <p className="text-sm font-medium text-gray-900">{activity.message}</p>
              <p className="text-sm text-gray-600">{formatDate(activity.date)}</p>
            </div>
          </div>
        ))}
      </div>
    </DashboardCard>
  );
};

export default ActivityCard;
